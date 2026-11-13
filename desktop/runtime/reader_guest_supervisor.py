"""Unreleased one-Work guest supervisor; the platform verifier is not wired."""
import os
import re
import threading


def _open_verified_guest_owner(identity, nonce, runtime):
    """No guest process, container, browser, extension, or peer is verified yet."""
    raise PermissionError("guest ownership and isolation are not independently verified")


def _canonical_entrypoints():
    # Packaging and identity of these exact modules remain a separate gate.
    from desktop.runtime.reader_guest_vsock_bridge import serve_bridge
    from app.reader_linux_service import serve_linux_reader
    return serve_bridge, serve_linux_reader


class _PipeGuestOwner:
    """Unwired pipe lifecycle; `platform` must independently own the peer.

    The platform must atomically admit the callback against revocation and
    retain/reclaim any untransferred peer. These properties are not established
    by this class and the production platform factory remains closed.
    """

    def __init__(self, platform):
        required = ("dispatch_if_active", "take_verified_peer", "policy_for_work",
                    "is_active", "revoke_and_stop")
        if any(not callable(getattr(platform, name, None)) for name in required):
            raise ValueError("owned guest platform is incomplete")
        self._platform = platform
        self._lock = threading.Lock()
        self._started = False
        self._stopped = threading.Event()
        self._workers = []
        self._unresolved = []

    def serve_if_active(self, identity, nonce, runtime, bridge, reader_service):
        with self._lock:
            if self._started or self._stopped.is_set():
                raise PermissionError("guest Work is already started or revoked")
            self._started = True
        return self._platform.dispatch_if_active(
            identity.copy(), nonce, lambda: self._serve_pair(identity, nonce, runtime, bridge, reader_service))

    def _serve_pair(self, identity, nonce, runtime, bridge, reader_service):
        bridge_taken, reader_taken = bytearray(1), bytearray(1)
        finished, errors = threading.Event(), []
        peer = self._platform.take_verified_peer(identity.copy(), nonce, runtime.copy())
        if type(peer) is not int or peer < 0:
            raise ValueError("verified guest peer unavailable")
        to_read = to_write = from_read = from_write = None
        launch_attempted = False
        try:
            to_read, to_write = os.pipe()
            from_read, from_write = os.pipe()
            def run_reader():
                try:
                    reader_service(identity.copy(), nonce, runtime.copy(),
                                   self._platform.policy_for_work(identity.copy()),
                                   to_read, from_write, handoff=reader_taken)
                except BaseException as error:
                    errors.append(error)
                    self._stopped.set()
                finally:
                    if reader_taken[0] == 0:
                        for fd in (to_read, from_write):
                            try:
                                os.close(fd)
                            except OSError:
                                pass
                    finished.set()
            worker = threading.Thread(target=run_reader, name="curis-guest-reader", daemon=True)
            self._workers.append(worker)
            # start() can raise after the thread actually started; after this
            # point only the worker may close its ends, even on an exception.
            launch_attempted = True
            worker.start()
            binding = {"identity": identity.copy(), "nonce": nonce,
                       **{key: runtime[key] for key in ("boot_id", "container_id", "image_digest")}}
            bridge(peer, to_write, from_read, binding,
                   alive=lambda: not self._stopped.is_set() and self._platform.is_active(),
                   handoff=bridge_taken)
            self._stopped.set()
            if not finished.wait(0.1):
                raise RuntimeError("guest reader shutdown remains UNKNOWN")
            if errors:
                raise RuntimeError("guest reader failed; state remains UNKNOWN") from errors[0]
        finally:
            self._stopped.set()
            if bridge_taken[0] == 0:
                for fd in (to_write, from_read):
                    if fd is not None:
                        try:
                            os.close(fd)
                        except OSError:
                            pass
                # Retain locally; do not wait on a potentially blocking cleanup
                # callback before the independent stop request can be made.
                self._unresolved.append(("peer", peer))
            if not launch_attempted:
                for fd in (to_read, from_write):
                    if fd is not None:
                        try:
                            os.close(fd)
                        except OSError:
                            pass
            elif not finished.is_set():
                # No blind close: start() may have launched the reader. These
                # descriptors are records only, not future close authorization.
                self._unresolved.append(("reader", to_read, from_write))

    def revoke_and_stop(self, identity, nonce):
        self._stopped.set()
        return self._platform.revoke_and_stop(identity.copy(), nonce)


class GuestSupervisor:
    """Delegate owned bridge/service lifecycle to a future verified platform.

    The owner must authenticate the actual container, peer, browser and
    extension; atomically reject new work when revoked; and independently stop
    owned resources. Method names and mock callbacks do not establish that.
    """

    def __init__(self, identity, nonce, runtime, owner, bridge, reader_service):
        if (not callable(getattr(owner, "serve_if_active", None))
                or not callable(getattr(owner, "revoke_and_stop", None))
                or not callable(bridge) or not callable(reader_service)):
            raise ValueError("verified guest lifecycle is unavailable")
        self._identity, self._nonce, self._runtime = identity.copy(), nonce, runtime.copy()
        self._owner = owner
        self._bridge, self._reader_service = bridge, reader_service
        self._lock = threading.Lock()
        self._closed = self._stop_error = self._stop_pending = False
        self.stop_state = "UNKNOWN"

    def serve(self):
        with self._lock:
            if self._closed:
                raise PermissionError("guest Work has been revoked")
        try:
            # The platform must perform atomic admission and independently
            # bind the authenticated descriptors before calling either service.
            result = self._owner.serve_if_active(self._identity.copy(), self._nonce,
                                                 self._runtime.copy(), self._bridge, self._reader_service)
        except BaseException as error:
            try:
                self.close()
            except Exception:
                error.add_note("Guest stop request failed; resources remain UNKNOWN")
            if self.stop_state == "UNKNOWN":
                error.add_note("Guest stop and resource state remain UNKNOWN")
            raise
        try:
            self.close()
        except Exception as error:
            error.add_note("Guest stop and resource state remain UNKNOWN")
            raise
        return result

    def close(self):
        with self._lock:
            if self._closed:
                if self._stop_error or self._stop_pending:
                    raise RuntimeError("guest stop is unresolved; resources remain UNKNOWN")
                return
            self._closed = self._stop_pending = True
        try:
            self._owner.revoke_and_stop(self._identity.copy(), self._nonce)
        except BaseException:
            with self._lock:
                self._stop_error = True
            raise
        finally:
            with self._lock:
                self._stop_pending = False


def open_guest_supervisor(identity, nonce, runtime):
    required = {"tenant_id", "company_id", "work_ref", "task_id", "employee_id", "binding_ref"}
    if type(identity) is not dict or type(runtime) is not dict:
        raise ValueError("original Work or runtime is invalid")
    identity, runtime = identity.copy(), runtime.copy()
    if (set(identity) != required or any(type(v) is not str or not v for v in identity.values())
            or type(nonce) is not str or re.fullmatch(r"[0-9a-f]{48}", nonce) is None):
        raise ValueError("original Work binding is invalid")
    if (set(runtime) != {"complete", "executionAuthorized", "boot_id", "container_id", "image_digest"}
            or runtime["complete"] is not True or runtime["executionAuthorized"] is not True
            or any(type(runtime[k]) is not str or not runtime[k]
                   for k in ("boot_id", "container_id", "image_digest"))):
        raise PermissionError("guest runtime is not authorized")
    try:
        platform = _open_verified_guest_owner(identity.copy(), nonce, runtime.copy())
        owner = _PipeGuestOwner(platform)
        bridge, reader_service = _canonical_entrypoints()
    except BaseException as error:
        error.add_note("Partially created guest resources, if any, remain UNKNOWN")
        raise
    try:
        return GuestSupervisor(identity, nonce, runtime, owner, bridge, reader_service)
    except BaseException as error:
        error.add_note("Rejected guest resources and their ownership remain UNKNOWN")
        raise
