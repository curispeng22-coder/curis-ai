"""Unwired Linux guest candidate; platform verification is not implemented."""
from .agent_browser_guest import ReaderGuest, serve_reader
from .agent_browser_runtime import load_trusted_reader_lock
from .reader_linux_driver import LinuxReaderDriver


def _open_verified_environment(identity, runtime, nonce, lock):
    # No caller-supplied flag, PID, or socket path can establish ownership.
    raise PermissionError("Linux guest ownership and egress have not been independently verified")


def serve_linux_reader(identity, nonce, runtime, policy, read_fd, write_fd, *, handoff=None):
    """Serve one original Work only after the separate platform gate is implemented."""
    lock = load_trusted_reader_lock()
    if (not isinstance(runtime, dict) or runtime.get("complete") is not True
            or runtime.get("executionAuthorized") is not True
            or not lock.get("browserImageDigest")
            or runtime.get("image_digest") != lock["browserImageDigest"]):
        raise PermissionError("fixed Reader runtime is not authorized")
    environment = _open_verified_environment(identity, runtime, nonce, lock)
    if environment.verify() is not True:
        raise PermissionError("Linux guest environment is not verified")
    driver = LinuxReaderDriver(environment, policy)
    guest = ReaderGuest(identity, nonce, runtime, policy, driver)
    serve_reader(guest, read_fd, write_fd, alive=environment.verify, handoff=handoff)
