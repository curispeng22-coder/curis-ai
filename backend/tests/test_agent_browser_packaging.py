"""Relocatable assets and release evidence, without executing a browser."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import pytest
from app import agent_browser_runtime as runtime


def packager():
    path = Path(__file__).resolve().parents[2] / 'desktop/scripts/package-agent-browser.py'
    spec = importlib.util.spec_from_file_location('browser_packager', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assets_fixture(tmp_path):
    inputs = tmp_path / 'inputs'; inputs.mkdir()
    cli = inputs / 'cli'; cli.write_bytes(b'synthetic executable'); cli.chmod(0o755)
    bundle = inputs / 'Fixture.app'
    chrome = bundle / 'Contents/MacOS/Google Chrome for Testing'; chrome.parent.mkdir(parents=True)
    chrome.write_bytes(b'synthetic chrome executable'); chrome.chmod(0o755)
    framework = bundle / 'Contents/Frameworks'; framework.mkdir()
    (framework / 'real').write_bytes(b'framework bytes')
    (framework / 'current').symlink_to('real')
    evidence = inputs / 'evidence.json'; evidence.write_text('{"fixture":"normal-close"}')
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    profile = {**runtime.BROWSER_BUNDLE_PATHS, 'cliSha256': sha(cli), 'chromeSha256': sha(chrome),
        'chromeBundleSha256': runtime.browser_bundle_digest(bundle), 'stopEvidenceSha256': sha(evidence),
        'boundary': 'FIXED_COMMANDS_FRESH_PROFILE_PUBLIC_READ_PROXY', 'methods': ['GET', 'HEAD']}
    lock = {'schemaVersion': 1, 'mode': 'PUBLIC_READ_ONLY_READER', 'complete': True, 'executionAuthorized': True,
        'runtimeKind': 'NATIVE_AGENT_BROWSER', 'agentBrowser': profile}
    raw = (json.dumps(lock) + '\n').encode(); lock_path = inputs / 'lock.json'; lock_path.write_bytes(raw)
    return lock, lock_path, cli, bundle, evidence


def install_fixture(root, values):
    lock, lock_path, cli, bundle, evidence = values
    target = root / 'backend/app/reader_runtime_lock.json'; target.parent.mkdir(parents=True)
    target.write_bytes(lock_path.read_bytes())
    expected = hashlib.sha256(lock_path.read_bytes()).hexdigest()
    result = packager().package_browser(root, lock_path, cli=cli, chrome_bundle=bundle, evidence=evidence,
        expected_lock_sha=expected)
    assert result['state'] == 'PINNED_BUNDLE_VERIFIED'
    return expected


def activate_fixture(monkeypatch, root, expected):
    monkeypatch.setattr(sys, 'frozen', True, raising=False)
    monkeypatch.setattr(sys, '_MEIPASS', str(root), raising=False)
    monkeypatch.setattr(runtime, '__file__', str(root / 'backend/app/agent_browser_runtime.py'))
    monkeypatch.setattr(runtime, 'READER_LOCK_SHA256', expected)


def test_two_cold_install_roots_resolve_same_pinned_assets_and_evidence(tmp_path, monkeypatch):
    values = assets_fixture(tmp_path)
    releases = []
    for name in ('First install', 'Other relocated installation'):
        root = tmp_path / name
        expected = install_fixture(root, values)
        activate_fixture(monkeypatch, root, expected)
        release = runtime.agent_browser_release()
        assert Path(release['cliPath']).is_relative_to(root)
        assert Path(release['stopEvidenceRef']).is_relative_to(root)
        assert (root / 'vendor/agent-browser/Google Chrome for Testing.app/Contents/Frameworks/current').is_symlink()
        releases.append(release)
    assert releases[0]['cliPath'] != releases[1]['cliPath']
    assert releases[0]['releaseSha256'] == releases[1]['releaseSha256']
    assert releases[0]['temporaryRoot'] == releases[1]['temporaryRoot']
    assert releases[0]['temporaryRoot'].endswith(releases[0]['releaseSha256'][:12])


@pytest.mark.parametrize('damage', ['missing-cli', 'changed-cli', 'changed-framework', 'changed-proof', 'empty-proof',
    'vendor-link', 'executable-link', 'escaped-framework-link', 'changed-packaged-lock'])
def test_packaged_missing_changed_or_escaping_resource_is_rejected(tmp_path, monkeypatch, damage):
    values = assets_fixture(tmp_path); root = tmp_path / 'installed'; expected = install_fixture(root, values)
    activate_fixture(monkeypatch, root, expected)
    cli = root / runtime.BROWSER_BUNDLE_PATHS['cliPath']
    evidence = root / runtime.BROWSER_BUNDLE_PATHS['stopEvidenceRef']
    framework = root / 'vendor/agent-browser/Google Chrome for Testing.app/Contents/Frameworks'
    if damage == 'missing-cli': cli.unlink()
    elif damage == 'changed-cli': cli.write_bytes(b'changed')
    elif damage == 'changed-framework': (framework / 'real').write_bytes(b'changed')
    elif damage == 'changed-proof': evidence.write_bytes(b'changed')
    elif damage == 'empty-proof': evidence.write_bytes(b'')
    elif damage == 'vendor-link':
        (root / 'vendor').rename(root / 'other-vendor'); (root / 'vendor').symlink_to('other-vendor')
    elif damage == 'executable-link':
        cli.unlink(); cli.symlink_to(values[2])
    elif damage == 'escaped-framework-link':
        (framework / 'current').unlink(); (framework / 'current').symlink_to(values[2])
    else: (root / 'backend/app/reader_runtime_lock.json').write_text('{}')
    with pytest.raises((ValueError, OSError)): runtime.agent_browser_release()
    with pytest.raises((ValueError, OSError)):
        packager().package_browser(root, values[1], verify_only=True, expected_lock_sha=expected)
    if damage in {'changed-proof', 'empty-proof'}:
        with pytest.raises(ValueError): runtime.agent_browser_release(verify_assets=False)


@pytest.mark.parametrize('path', ['/machine/private/browser', '../outside', 'vendor/agent-browser/../browser',
    'vendor/agent-browser/alternate', 'vendor\\agent-browser\\agent-browser'])
def test_release_rejects_absolute_or_noncanonical_paths(tmp_path, path):
    lock, *_ = assets_fixture(tmp_path)
    lock['agentBrowser']['cliPath'] = path
    with pytest.raises(ValueError): runtime.browser_release_profile(lock)


def test_packager_rejects_changed_input_before_creating_assets(tmp_path):
    values = assets_fixture(tmp_path); lock, lock_path, cli, bundle, evidence = values
    root = tmp_path / 'installed'; target = root / 'backend/app/reader_runtime_lock.json'; target.parent.mkdir(parents=True)
    target.write_bytes(lock_path.read_bytes()); evidence.write_text('changed')
    with pytest.raises(ValueError, match='evidence changed'):
        packager().package_browser(root, lock_path, cli=cli, chrome_bundle=bundle, evidence=evidence,
            expected_lock_sha=hashlib.sha256(lock_path.read_bytes()).hexdigest())
    assert not (root / 'vendor/agent-browser').exists()


def test_pending_release_still_checks_packaged_lock_and_never_needs_browser_assets(tmp_path):
    source = Path(__file__).resolve().parents[1] / 'app/reader_runtime_lock.json'
    root = tmp_path / 'pending'; packaged = root / 'backend/app/reader_runtime_lock.json'
    packaged.parent.mkdir(parents=True); packaged.write_bytes(source.read_bytes())
    expected = hashlib.sha256(source.read_bytes()).hexdigest()
    result = packager().package_browser(root, source, verify_only=True, expected_lock_sha=expected)
    assert result['state'] == 'NO_AGENT_BROWSER_RELEASE'
    assert not (root / 'vendor').exists()
    packaged.write_text('{"complete":true}')
    with pytest.raises(ValueError, match='Packaged reader lock'):
        packager().package_browser(root, source, verify_only=True, expected_lock_sha=expected)
