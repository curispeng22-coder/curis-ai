"""Unwired per-Work egress candidate; platform ownership is not implemented.

The existing PublicReadProxy handler enforces HTTP policy, but it is not a VM
identity verifier or a guest network boundary. Its host TCP listener must not
be exposed to an unverified guest. The production factory below always rejects.
"""
import re
import threading

from .agent_browser_policy import PublicReadProxy
from .agent_browser_runtime import load_trusted_reader_lock


def _open_verified_egress(identity, nonce, runtime, policy, lock):
    raise PermissionError("VM peer, guest isolation and controlled egress are not verified")


class _WorkEgress:
    """Delegate atomic peer admission and independent revocation to the owner.

    The owner must authenticate the actual VM and stream, bind both to the
    original Work and nonce, enforce atomic admission against revocation, and
    interrupt all owned DNS and proxy connections. These guarantees are not
    implemented by checking method names or by the PublicReadProxy itself.
    """

    def __init__(self, identity, nonce, owner, proxy, policy):
        if (not isinstance(proxy, PublicReadProxy) or proxy.policy is not policy
                or not callable(getattr(owner, "dispatch_authenticated", None))
                or not callable(getattr(owner, "revoke_and_stop", None))):
            raise ValueError("controlled egress owner or proxy is invalid")
        self._identity, self._nonce = dict(identity), nonce
        self._owner, self._proxy = owner, proxy
        self._lock = threading.Lock()
        self._closed = self._stop_error = False
        self._stop_pending = False
        self.stop_state = "UNKNOWN"

    def serve(self, stream):
        with self._lock:
            if self._closed:
                raise PermissionError("Work egress is revoked")
            handler = self._serve_authenticated
        # Authentication, admission and revocation must share the platform gate.
        return self._owner.dispatch_authenticated(self._identity.copy(), self._nonce, stream, handler)

    def _serve_authenticated(self, stream):
        # Match PublicReadProxy's handler limit without closing an unproven stream.
        if not self._proxy.permits.acquire(blocking=False):
            raise PermissionError("Work egress connection limit reached")
        try:
            return self._proxy.serve(stream)
        finally:
            self._proxy.permits.release()

    def close(self):
        with self._lock:
            if self._closed:
                if self._stop_error:
                    raise RuntimeError("egress stop request failed; resources remain UNKNOWN")
                if self._stop_pending:
                    raise RuntimeError("egress stop request is pending; resources remain UNKNOWN")
                return
            self._closed = True
            self._stop_pending = True
        try:
            # The owner must not wait on proxy.close before requesting VM stop.
            self._owner.revoke_and_stop(self._identity.copy(), self._nonce)
        except BaseException:
            with self._lock:
                self._stop_error = True
            raise
        finally:
            with self._lock:
                self._stop_pending = False


def open_work_egress(identity, nonce, runtime, policy):
    """Open no listener or connection until the separate platform gate exists."""
    required = {"tenant_id", "company_id", "work_ref", "task_id", "employee_id", "binding_ref"}
    if type(identity) is not dict or type(runtime) is not dict:
        raise ValueError("original Work identity or runtime is invalid")
    identity, runtime = identity.copy(), runtime.copy()
    if (set(identity) != required
            or any(type(value) is not str or not value for value in identity.values())
            or not isinstance(nonce, str) or re.fullmatch(r"[0-9a-f]{48}", nonce) is None):
        raise ValueError("original Work identity or nonce is invalid")
    lock = load_trusted_reader_lock()
    if (set(runtime) != {"complete", "executionAuthorized", "boot_id", "container_id", "image_digest"}
            or runtime.get("complete") is not True
            or runtime.get("executionAuthorized") is not True
            or any(type(runtime.get(k)) is not str or not runtime[k]
                   for k in ("boot_id", "container_id", "image_digest"))
            or not lock.get("browserImageDigest")
            or runtime["image_digest"] != lock["browserImageDigest"]):
        raise PermissionError("fixed Reader runtime is not authorized")
    try:
        owner, proxy = _open_verified_egress(dict(identity), nonce, dict(runtime), policy, lock)
    except BaseException as error:
        error.add_note("Partially created egress resources, if any, remain UNKNOWN")
        raise
    try:
        return _WorkEgress(identity, nonce, owner, proxy, policy)
    except BaseException as error:
        # A rejected object is not safe to close or signal without ownership proof.
        error.add_note("Rejected egress resources and their ownership remain UNKNOWN")
        raise
