#!/usr/bin/env python3
"""Stage pinned browser assets in the existing PyInstaller onedir resource tree."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys

REPOSITORY = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY))
from backend.app.agent_browser_runtime import (BROWSER_BUNDLE_PATHS, READER_LOCK_SHA256,
    _pinned_browser_asset, browser_bundle_digest, browser_release_profile, verify_browser_package)


def package_browser(resource_root, lock_path, *, cli=None, chrome_bundle=None, evidence=None,
                    verify_only=False, expected_lock_sha=READER_LOCK_SHA256):
    raw = Path(lock_path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected_lock_sha:
        raise ValueError("Reader lock differs from the compiled build")
    lock = json.loads(raw)
    root = Path(resource_root).resolve(strict=True)
    packaged_lock = root / "backend/app/reader_runtime_lock.json"
    if packaged_lock.is_symlink() or packaged_lock.read_bytes() != raw:
        raise ValueError("Packaged reader lock differs from the compiled build input")
    if lock.get("runtimeKind") != "NATIVE_AGENT_BROWSER":
        return {"state": "NO_AGENT_BROWSER_RELEASE"}
    profile = browser_release_profile(lock)
    target = root / "vendor/agent-browser"
    if not verify_only:
        if not all((cli, chrome_bundle, evidence)):
            raise ValueError("Reviewed CLI, full Chrome bundle and evidence build inputs are required")
        cli, chrome_bundle, evidence = Path(cli), Path(chrome_bundle), Path(evidence)
        chrome_relative = Path(BROWSER_BUNDLE_PATHS["chromePath"]).relative_to("vendor/agent-browser")
        chrome = chrome_bundle / Path(*chrome_relative.parts[1:])
        _pinned_browser_asset(cli, profile["cliSha256"])
        _pinned_browser_asset(chrome, profile["chromeSha256"])
        if chrome_bundle.is_symlink() or browser_bundle_digest(chrome_bundle) != profile["chromeBundleSha256"]:
            raise ValueError("Reviewed Chrome bundle changed before packaging")
        if evidence.is_symlink() or not evidence.is_file() or not 0 < evidence.stat().st_size <= 1024 * 1024:
            raise ValueError("Reviewed browser evidence is not a bounded regular file")
        if hashlib.sha256(evidence.read_bytes()).hexdigest() != profile["stopEvidenceSha256"]:
            raise ValueError("Reviewed browser evidence changed before packaging")
        vendor = root / "vendor"
        if vendor.is_symlink():
            raise ValueError("Browser package parent is not an owned resource directory")
        vendor.mkdir(exist_ok=True)
        # Never overwrite/adopt a partial or previously built asset directory.
        target.mkdir()
        shutil.copy2(cli, root / BROWSER_BUNDLE_PATHS["cliPath"], follow_symlinks=False)
        shutil.copytree(chrome_bundle, target / chrome_relative.parts[0], symlinks=True)
        shutil.copy2(evidence, root / BROWSER_BUNDLE_PATHS["stopEvidenceRef"], follow_symlinks=False)
    verify_browser_package(profile, root)
    return {"state": "PINNED_BUNDLE_VERIFIED", "readerLockSha256": expected_lock_sha,
        "cliSha256": profile["cliSha256"], "chromeBundleSha256": profile["chromeBundleSha256"],
        "stopEvidenceSha256": profile["stopEvidenceSha256"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resource-root", required=True)
    parser.add_argument("--lock", required=True)
    parser.add_argument("--cli")
    parser.add_argument("--chrome-bundle")
    parser.add_argument("--evidence")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    result = package_browser(args.resource_root, args.lock, cli=args.cli, chrome_bundle=args.chrome_bundle,
        evidence=args.evidence, verify_only=args.verify_only)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
