"""Small packaged supervisor that prevents orphaned Desktop sidecars."""

from __future__ import annotations

import argparse
import fcntl
import os
import select
import signal
import stat
import subprocess
import sys
import time
import traceback


def parent_channel(expected: int) -> int:
    """The spawner owns the sole write end; bootloaders inherit only this reader."""
    fd = sys.stdin.fileno()
    if expected <= 1 or not stat.S_ISFIFO(os.fstat(fd).st_mode):
        raise ValueError("parent lifecycle channel must be a pipe")
    fcntl.fcntl(fd, fcntl.F_SETFL, fcntl.fcntl(fd, fcntl.F_GETFL) | os.O_NONBLOCK)
    deadline = time.monotonic() + 3
    handshake = b""
    while b"\n" not in handshake:
        remaining = deadline - time.monotonic()
        if remaining <= 0 or not select.select([fd], [], [], remaining)[0]:
            raise ValueError("parent lifecycle handshake timed out")
        chunk = os.read(fd, 64)
        if not chunk:
            raise ValueError("parent lifecycle channel closed before startup")
        handshake += chunk
        if len(handshake) > 64:
            raise ValueError("parent lifecycle handshake too long")
    if handshake != f"curis-guardian/v1 {expected}\n".encode("ascii"):
        raise ValueError("parent lifecycle handshake mismatch")
    if select.select([fd], [], [], 0)[0]:
        raise ValueError("parent lifecycle channel changed before startup")
    return fd


def parent_alive(fd: int) -> bool:
    # No further bytes are legal. EOF, unexpected data and IO errors fail closed.
    try:
        return not select.select([fd], [], [], 0.25)[0]
    except (OSError, ValueError):
        return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--parent-pid", type=int, required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = [args.target, *args.command]
    if command[len([args.target]) :] and command[1] == "--":
        command.pop(1)

    try:
        channel = parent_channel(args.parent_pid)
    except (OSError, ValueError):
        print("guardian: invalid parent lifecycle channel; target not started", file=sys.stderr)
        return 2

    child = None
    spawning = False
    pending_stop = False

    def reap_child() -> None:
        if child is not None and child.poll() is None:
            child.terminate()
            try:
                child.wait(timeout=3)
            except subprocess.TimeoutExpired:
                child.kill()
                child.wait()

    def stop(_signum: int, _frame: object) -> None:
        nonlocal pending_stop
        # Defer during Popen instead of masking signals inherited by the target.
        if spawning:
            pending_stop = True
            return
        reap_child()
        raise SystemExit(0)

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    try:
        spawning = True
        try:
            child = subprocess.Popen(command, stdin=subprocess.DEVNULL)
        finally:
            spawning = False
        if pending_stop:
            stop(signal.SIGTERM, None)
        while child.poll() is None:
            if not parent_alive(channel):
                print("guardian: parent lifecycle channel lost; stopping target", file=sys.stderr)
                stop(signal.SIGTERM, None)
        return int(child.returncode or 0)
    except Exception:
        traceback.print_exc()
        raise
    finally:
        reap_child()


if __name__ == "__main__":
    raise SystemExit(main())
