import subprocess
from pathlib import Path


LAUNCHER = Path(__file__).parents[2] / "deploy/curis/启用本地 Owner 绑定.command"


def test_launcher_is_one_time_and_never_serializes_secrets() -> None:
    text = LAUNCHER.read_text()
    assert "mktemp /tmp/curis-local-oidc.XXXXXX)" in text
    assert "XXXXXX.yml" not in text
    assert '-T "" -w' in text
    assert "printf '%s\\n' \"$bootstrap_material\" | /usr/bin/expect -c" in text
    assert "log_user 0" in text
    assert '-exact "password data for new item:"' in text
    assert '-exact "retype password for new item:"' in text
    assert "set timeout 3" in text
    assert text.count("timeout {") >= 3
    assert "expect eof\n  set result [wait]" not in text
    assert text.count("delete-generic-password") >= 3
    assert "find-generic-password" in text
    assert "keychain_created=true" in text
    assert "keychain_created=false" in text
    assert text.index("unset bootstrap_material") < text.index(
        "inject_attempted=true"
    )
    assert 'reset_result=' in text
    assert '[ "$reset_result" = "OWNER_BINDING_RESET=true" ]' in text
    assert "reset 2>/dev/null || true" not in text
    assert text.index("inject_attempted=true") < text.index("docker exec -i")
    assert 'inject_result="$({' in text
    assert '[ "$inject_result" = "OWNER_BINDING_READY=true" ]' in text
    assert "python3 -c 'import json" not in text.split("docker exec -i", 1)[0]
    assert "printf '%s\\0%s\\0'" in text
    assert "-s com.curis.local.owner-bootstrap -w" in text
    assert "trap cleanup EXIT" in text
    assert "trap 'exit 1' HUP INT TERM" in text
    assert 'print("OWNER_BINDING_READY=true")' in text
    assert "/usr/bin/open http://127.0.0.1:3001/login" in text


def test_native_expect_delivers_hidden_input_to_a_tty() -> None:
    result = subprocess.run(
        [
            "/usr/bin/expect",
            "-c",
            """
                log_user 0
                set timeout 3
                gets stdin material
                spawn /bin/sh -c {printf "password data for new item:" >/dev/tty; IFS= read -r first </dev/tty; printf "retype password for new item:" >/dev/tty; IFS= read -r second </dev/tty; [ "$first" = sentinel-material ] && [ "$second" = sentinel-material ]}
                expect -exact "password data for new item:"
                send -- "$material\\r"
                expect -exact "retype password for new item:"
                send -- "$material\\r"
                unset material
                expect eof
                set result [wait]
                exit [lindex $result 3]
            """,
        ],
        input=b"sentinel-material\n",
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    assert result.returncode == 0


def test_macos_mktemp_template_creates_a_unique_file() -> None:
    result = subprocess.run(
        ["/usr/bin/mktemp", "/tmp/curis-local-oidc.XXXXXX"],
        capture_output=True,
        text=True,
        check=True,
    )
    path = Path(result.stdout.strip())
    try:
        assert path.is_file()
        assert "XXXXXX" not in path.name
    finally:
        path.unlink()
