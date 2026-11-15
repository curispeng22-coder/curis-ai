"""Bounded original-Work Reader lease protocol; execution requires a separately accepted runtime."""
from __future__ import annotations

import base64
import json
import secrets
import time

MAX_FRAME = 262144
MAX_IMAGE = 8 * 1024 * 1024


READER_LOCK_SHA256 = "c4e90e387378cfc6b266f20f11eaee74891ffe4cf65420b533b72f5840b89d34"


def load_trusted_reader_lock():
    """Load only the bundled, compile-time pinned resource; unreleased locks fail closed."""
    import hashlib
    import os
    import stat
    from pathlib import Path
    path = Path(__file__).resolve().with_name("reader_runtime_lock.json")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_size > 65536:
            raise ValueError("Reader lock resource is invalid")
        with os.fdopen(fd, "rb", closefd=False) as stream:
            raw = stream.read(65537)
    finally:
        os.close(fd)
    if hashlib.sha256(raw).hexdigest() != READER_LOCK_SHA256:
        raise ValueError("Reader lock resource does not match the pinned build")
    lock = json.loads(raw)
    if (not isinstance(lock, dict) or lock.get("schemaVersion") != 1
            or lock.get("mode") != "PUBLIC_READ_ONLY_READER"
            or lock.get("complete") is not True or lock.get("executionAuthorized") is not True):
        raise ValueError("Reader runtime is not released")
    return lock


def _unique_json_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Reader response contains a duplicate key")
        result[key] = value
    return result


def _invalid_json_constant(_value):
    raise ValueError("Reader response contains a non-finite value")


def _finite_json_float(value):
    import math
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("Reader response contains a non-finite value")
    return number


class BoundedPipeTransport:
    """Own private pipe duplicates; callers retain their original descriptors.

    Nonblocking status is shared with the original open file descriptions.
    Callers must not concurrently change those flags. No process is spawned or signalled.
    """
    def __init__(self, read_fd, write_fd, *, alive=lambda: True, clock=time.monotonic, timeout=5):
        import fcntl
        import os
        import stat
        import threading
        if (type(read_fd) is not int or type(write_fd) is not int or read_fd == write_fd
                or not 0 < timeout <= 90):
            raise ValueError("Reader pipe configuration invalid")
        owned_read = os.dup(read_fd)
        try:
            owned_write = os.dup(write_fd)
            try:
                read_info, write_info = os.fstat(owned_read), os.fstat(owned_write)
                read_mode = fcntl.fcntl(owned_read, fcntl.F_GETFL) & os.O_ACCMODE
                write_mode = fcntl.fcntl(owned_write, fcntl.F_GETFL) & os.O_ACCMODE
                if (not stat.S_ISFIFO(read_info.st_mode) or not stat.S_ISFIFO(write_info.st_mode)
                        or (read_info.st_dev, read_info.st_ino) == (write_info.st_dev, write_info.st_ino)
                        or read_mode != os.O_RDONLY or write_mode != os.O_WRONLY):
                    raise ValueError("Reader transport requires distinct directional pipes")
                os.set_blocking(owned_read, False)
                os.set_blocking(owned_write, False)
            except BaseException:
                os.close(owned_write)
                raise
        except BaseException:
            os.close(owned_read)
            raise
        self._read_fd, self._write_fd = owned_read, owned_write
        self._alive, self._clock, self._timeout = alive, clock, timeout
        self._closed, self._fds_closed, self._lock = False, False, threading.RLock()

    @classmethod
    def create_pipe_pair(cls, **options):
        """Create distinct pipes and return transport plus caller-owned guest ends."""
        import os
        opened = []
        transport = None
        try:
            guest_read, host_write = os.pipe()
            opened.extend((guest_read, host_write))
            host_read, guest_write = os.pipe()
            opened.extend((host_read, guest_write))
            transport = cls(host_read, host_write, **options)
            os.close(host_read)
            opened.remove(host_read)
            os.close(host_write)
            opened.remove(host_write)
            return transport, guest_read, guest_write
        except BaseException:
            if transport is not None:
                transport.close()
            for fd in opened:
                try:
                    os.close(fd)
                except OSError:
                    pass
            raise

    def _wait(self, fd, *, writing, deadline):
        import select
        while True:
            if self._closed or not self._alive():
                raise PermissionError("Reader transport is closed or authorization revoked")
            remaining = deadline - self._clock()
            if remaining <= 0:
                raise TimeoutError("Reader transport deadline exceeded")
            ready = select.select([] if writing else [fd], [fd] if writing else [], [], min(remaining, 0.05))
            if ready[1 if writing else 0]:
                return

    def request(self, frame):
        import os
        if not isinstance(frame, dict) or "result" in frame:
            raise ValueError("Reader request must not contain a result")
        data = (json.dumps(frame, ensure_ascii=False, separators=(",", ":"), allow_nan=False) + chr(10)).encode()
        if len(data) > MAX_FRAME:
            raise ValueError("Reader request frame too large")
        with self._lock:
            deadline = self._clock() + self._timeout
            try:
                sent = 0
                while sent < len(data):
                    self._wait(self._write_fd, writing=True, deadline=deadline)
                    try:
                        count = os.write(self._write_fd, data[sent:])
                    except BlockingIOError:
                        continue
                    if count <= 0:
                        raise ValueError("Reader pipe closed during request")
                    sent += count
                response = bytearray()
                while True:
                    self._wait(self._read_fd, writing=False, deadline=deadline)
                    try:
                        chunk = os.read(self._read_fd, 65536)
                    except BlockingIOError:
                        continue
                    if not chunk:
                        raise ValueError("Reader pipe closed before reply")
                    response.extend(chunk)
                    if len(response) > MAX_IMAGE * 2:
                        raise ValueError("Reader response frame too large")
                    if bytes([10]) in response:
                        line, tail = bytes(response).split(bytes([10]), 1)
                        if tail:
                            raise ValueError("Reader response contains unexpected extra data")
                        result = json.loads(line.decode("utf-8"), object_pairs_hook=_unique_json_object,
                                            parse_constant=_invalid_json_constant, parse_float=_finite_json_float)
                        if not isinstance(result, dict) or "result" not in result:
                            raise ValueError("Reader response must contain a result")
                        return result
            except BaseException:
                self.close()
                raise

    def close(self):
        import os
        self._closed = True
        with self._lock:
            if self._fds_closed:
                return
            self._fds_closed = True
            for fd in (self._read_fd, self._write_fd):
                try:
                    os.close(fd)
                except OSError:
                    pass


class ReaderHostRegistry:
    """Offline host ownership contract; not a production process or identity verifier.

    The injected factory must be host controlled. Its process/exit assertions require
    independent verification by a future authorized platform adapter. Object identity
    checks do not establish unique underlying OS handles or real process termination.
    Deadlines are
    observed on registry calls; this class has no watchdog or hard-kill guarantee.
    """
    def __init__(self, factory, *, clock=time.monotonic, seconds=90):
        import threading
        if not callable(factory) or not 0 < seconds <= 90:
            raise ValueError("Reader host registry configuration invalid")
        self._factory, self._clock, self._seconds = factory, clock, seconds
        self._records, self._lock = {}, threading.RLock()

    def start(self, identity):
        import threading
        required = ("tenant_id", "company_id", "work_ref", "task_id", "employee_id", "binding_ref")
        if type(identity) is not dict:
            raise ValueError("Reader host requires complete Work identity")
        identity_snapshot = identity.copy()
        if (any(type(k) is not str for k in identity_snapshot) or set(identity_snapshot) != set(required)
                or any(type(identity_snapshot[k]) is not str or not identity_snapshot[k] for k in required)):
            raise ValueError("Reader host requires complete Work identity")
        process, transport, runtime = self._factory(identity_snapshot.copy())
        valid = (callable(getattr(process, "terminate", None))
                 and callable(getattr(process, "has_exited", None))
                 and callable(getattr(transport, "close", None))
                 and isinstance(runtime, dict)
                 and all(isinstance(runtime.get(k), str) and runtime[k] for k in ("boot_id", "container_id", "image_digest")))
        if not valid:
            # Ownership is unproven; closing may affect another in-flight Work.
            raise ValueError("Reader host factory returned invalid handles; cleanup is unknown")
        runtime_snapshot = dict(runtime)
        deadline = self._clock() + self._seconds
        with self._lock:
            if any(process is record["process"] or transport is record["transport"] for record in self._records.values()):
                # Never terminate a reused or potentially shared handle.
                raise ValueError("Reader host handle reuse; cleanup is unknown")
            token = object()
            self._records[token] = {"identity":identity_snapshot, "process":process, "transport":transport,
                                    "runtime":runtime_snapshot, "deadline":deadline,
                                    "claimed":False, "stop_state":None, "lock":threading.RLock()}
            return token

    def _record(self, token, identity):
        required = ("tenant_id", "company_id", "work_ref", "task_id", "employee_id", "binding_ref")
        if type(token) is not object or type(identity) is not dict:
            raise PermissionError("Reader host registration or Work identity mismatch")
        identity_snapshot = identity.copy()
        if (any(type(k) is not str for k in identity_snapshot) or set(identity_snapshot) != set(required)
                or any(type(identity_snapshot[k]) is not str or not identity_snapshot[k] for k in required)):
            raise PermissionError("Reader host registration or Work identity mismatch")
        with self._lock:
            record = self._records.get(token)
        if record is None or record["identity"] != identity_snapshot:
            raise PermissionError("Reader host registration or Work identity mismatch")
        return record

    def claim(self, token, identity):
        record = self._record(token, identity)
        with record["lock"]:
            if record["stop_state"] is not None or record["claimed"]:
                raise PermissionError("Reader host registration unavailable")
            if self._clock() >= record["deadline"]:
                self._stop(record)
                raise PermissionError("Reader host registration expired")
            record["claimed"] = True
            return record["transport"], dict(record["runtime"])

    def stop(self, token, identity):
        record = self._record(token, identity)
        with record["lock"]:
            return self._stop(record)

    @staticmethod
    def _stop(record):
        if record["stop_state"] is not None:
            return record["stop_state"]
        record["stop_state"] = "UNKNOWN"
        closed = terminated = False
        try:
            record["transport"].close()
            closed = True
        except Exception:
            pass
        try:
            record["process"].terminate()
            terminated = True
        except Exception:
            pass
        try:
            exited = record["process"].has_exited() is True
        except Exception:
            exited = False
        if closed and terminated and exited:
            record["stop_state"] = "GONE"
        return record["stop_state"]


def _open_verified_host_adapter(lock):
    """No production host adapter has passed its independent runtime gate."""
    raise ValueError("公开网页只读环境尚未完成独立验证，暂不能执行浏览。")


class FixedHostBridge:
    """Candidate control contract, unreachable without a verified production adapter.

    A future adapter must itself verify the executable hash, socket ownership, VM
    boot and container identity. This class does not authenticate those assertions,
    start a watchdog, or prove termination of an actual container.
    """
    _ROOT = "/Users/Shared/curis-exec-20261029-vm01"
    _IDENTITY = ("tenant_id", "company_id", "work_ref", "task_id", "employee_id", "binding_ref")

    def __init__(self, identity, should_stop):
        import threading
        if (not isinstance(identity, dict) or set(identity) != set(self._IDENTITY)
                or any(not isinstance(identity[k], str) or not identity[k] for k in self._IDENTITY)
                or not callable(should_stop)):
            raise ValueError("Reader bridge requires complete original Work identity")
        self._identity, self._should_stop = dict(identity), should_stop
        self._lock, self._state = threading.RLock(), "NEW"
        self._adapter = self._handle = self._container = None

    @staticmethod
    def _absolute(value):
        from pathlib import PurePosixPath
        return (isinstance(value, str) and value.startswith("/") and value != "/"
                and not any(ord(c) < 33 or ord(c) == 127 for c in value)
                and "//" not in value and all(p not in (".", "..") for p in value.split("/"))
                and str(PurePosixPath(value)) == value)

    @classmethod
    def _argv(cls, lock, snapshot):
        import re
        closure = lock.get("hostHelperClosure")
        if not isinstance(closure, dict) or not isinstance(snapshot, dict):
            raise ValueError("Reader host lock is incomplete")
        docker, socket_path, config, worker = (closure.get(k) for k in
            ("dockerCliPath", "dockerSocketPath", "dockerConfigDir", "guestWorkerPath"))
        if (not all(cls._absolute(x) for x in (docker, socket_path, config, worker))
                or not socket_path.startswith(cls._ROOT + "/") or not config.startswith(cls._ROOT + "/")
                or not re.fullmatch(r"[0-9a-f]{64}", str(closure.get("dockerCliSha256", "")))
                or not re.fullmatch(r"[0-9a-f]{64}", str(snapshot.get("container_id", "")))
                or not re.fullmatch(r"[0-9a-f-]{36}", str(snapshot.get("boot_id", "")))
                or not re.fullmatch(r"sha256:[0-9a-f]{64}", str(snapshot.get("image_digest", "")))
                or snapshot["image_digest"] != lock.get("browserImageDigest")):
            raise ValueError("Reader host identity or fixed command is invalid")
        return (docker, "--host", "unix://" + socket_path, "--config", config,
                "exec", "-i", snapshot["container_id"], worker)

    def start(self):
        with self._lock:
            if self._state != "NEW" or self._should_stop():
                raise PermissionError("Reader bridge cannot start")
            lock = load_trusted_reader_lock()
            adapter = _open_verified_host_adapter(lock)
            snapshot = adapter.verified_runtime()
            argv = self._argv(lock, snapshot)
            if self._should_stop():
                raise PermissionError("Original Work is stopped")
            self._adapter, self._container = adapter, snapshot["container_id"]
            self._state = "STARTING"
            try:
                self._handle = adapter.start_fixed_exec(argv, dict(self._identity))
                if not callable(getattr(self._handle, "close", None)) or self._should_stop():
                    raise PermissionError("Reader bridge failed to start safely")
                self._state = "RUNNING"
            except BaseException:
                self._stop_owned()
                raise

    def stop(self, identity):
        with self._lock:
            if identity != self._identity:
                raise PermissionError("Reader bridge Work identity mismatch")
            return self._stop_owned()

    def _stop_owned(self):
        if self._state in ("GONE", "UNKNOWN"):
            return self._state
        if self._state == "NEW":
            self._state = "GONE"
            return self._state
        self._state = "UNKNOWN"
        closed = self._handle is None
        try:
            if self._handle is not None:
                self._handle.close()
                closed = True
        except Exception:
            pass
        try:
            self._adapter.stop_owned_container(self._container)
            stopped = True
        except Exception:
            stopped = False
        try:
            exited = self._adapter.owned_container_exited(self._container) is True
        except Exception:
            exited = False
        if closed and stopped and exited:
            self._state = "GONE"
        return self._state


def open_reader_for_work(identity, hosts, should_stop):
    """Single Work entrypoint; cannot accept a caller-provided runtime or adapter."""
    from .agent_browser_policy import PublicTargets
    required = ("tenant_id", "company_id", "work_ref", "task_id", "employee_id", "binding_ref")
    if not isinstance(identity, dict) or any(not isinstance(identity.get(k), str) or not identity[k] for k in required):
        raise ValueError("Reader requires the complete original execution identity")
    if not callable(should_stop) or should_stop():
        raise PermissionError("Original Work is stopped or cannot be verified")
    policy = PublicTargets(hosts)
    try:
        lock = load_trusted_reader_lock()
    except (ValueError, OSError) as error:
        raise ValueError("公开网页只读环境尚未完成独立验证，暂不能执行浏览。") from error
    if lock.get("runtimeKind") != "VM":
        raise ValueError("Reader VM runtime is not released")
    # Reuse the per-Work SSH owner, not the legacy shared Docker exec adapter.
    from .reader_vm_host import open_owned_reader
    return open_owned_reader(dict(identity), policy, should_stop)


def open_native_browser_for_work(identity, hosts, should_stop, *, root, metadata):
    """Thin Work-bound entry to the existing BrowserLease, never a VM adapter.

    The bundled production lock must explicitly release the native backend.
    Neither a Work payload nor binding metadata can grant that release.
    """
    import os
    from pathlib import Path
    from .agent_browser_policy import PublicTargets
    required={"tenant_id","company_id","work_ref","task_id","employee_id","binding_ref"}
    if (type(identity) is not dict or set(identity)!=required
            or any(type(v) is not str or not v for v in identity.values()) or not callable(should_stop)):
        raise ValueError("Native browser requires complete original Work identity")
    fixed=identity.copy()
    if should_stop(): raise PermissionError("Original Work is stopped")
    policy=PublicTargets(hosts)
    # Keep the existing production lock closed. VM acceptance cannot release native.
    try:
        lock=load_trusted_reader_lock()
    except (ValueError,OSError) as error:
        raise ValueError("公开网页只读环境尚未完成独立验证，暂不能执行浏览。") from error
    if lock.get("runtimeKind")!="NATIVE_BROWSERSKILL":
        raise ValueError("本机公开网页只读环境尚未通过独立验证，暂不能执行浏览。")
    if type(metadata) is not dict:
        raise ValueError("Native browser binding metadata is invalid")
    root=Path(root)
    if (not root.is_absolute() or root.name!="agent-browser" or any(p in {".",".."} for p in root.parts)
            or os.environ.get("CURIS_AGENT_BROWSER_PROFILE")):
        raise ValueError("Native browser requires its backend-owned profile directory")
    chrome="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    configured=metadata.get("browser_chrome_path")
    if configured is not None and (type(configured) is not str or configured not in {"",chrome}):
        raise ValueError("Native browser executable is outside the fixed Chrome path")
    # Do not forward model credentials or arbitrary capability metadata to a browser.
    binding={k:metadata[k] for k in ("browser_skill_path","browser_chrome_path") if metadata.get(k)}
    if should_stop(): raise PermissionError("Original Work is stopped")
    from .agent_browser import BrowserLease
    lease=BrowserLease(root,fixed.copy(),binding,sorted(policy.hosts),alive=lambda:not should_stop())
    try:
        if should_stop(): raise PermissionError("Original Work stopped during browser creation")
        started=lease.start()
        if (started is not lease or lease.identity!=fixed or lease.policy.hosts!=policy.hosts or should_stop()):
            raise PermissionError("Native browser is not bound to the original Work and public targets")
        return lease
    except BaseException as error:
        try: lease.close()
        except BaseException: error.add_note("Original native browser cleanup UNKNOWN")
        raise


class ReaderLease:
    def __init__(self, identity, policy, transport, runtime, *, nonce=None, alive=lambda: True, clock=time.monotonic):
        # A trusted owner may supply its already durably reserved nonce. This
        # validates its shape only; it never grants ownership or runtime release.
        if nonce is not None and (type(nonce) is not str or len(nonce) != 48
                or any(c not in "0123456789abcdef" for c in nonce)):
            raise ValueError("Reader reserved nonce is invalid")
        required = ("tenant_id", "company_id", "work_ref", "task_id", "employee_id", "binding_ref")
        if not isinstance(identity, dict) or any(not isinstance(identity.get(k), str) or not identity[k] for k in required):
            raise ValueError("Reader requires the complete original execution identity")
        if not isinstance(runtime, dict) or runtime.get("complete") is not True or runtime.get("executionAuthorized") is not True:
            raise ValueError("Reader runtime has not passed its separate execution gate")
        lock = load_trusted_reader_lock()
        if not lock.get("browserImageDigest") or runtime.get("image_digest") != lock["browserImageDigest"]:
            raise ValueError("Reader container is not bound to the pinned image")
        for key in ("boot_id", "container_id", "image_digest"):
            if not isinstance(runtime.get(key), str) or not runtime[key]:
                raise ValueError("Reader runtime identity is incomplete")
        self.identity = dict(identity)
        self.policy, self.transport, self.runtime = policy, transport, dict(runtime)
        self.stop_check, self.clock = alive, clock
        self.deadline = clock() + 90
        self.nonce = secrets.token_hex(24) if nonce is None else nonce
        self.sequence = 0
        import threading
        self._operation_lock = threading.Lock()
        self._close_lock = threading.Lock()
        self._close_pending = self._close_failed = False
        self.closed = False
        self.session = self.nonce
        self.browser_id = runtime["container_id"]
        self.tab = None
        self.url = None

    def _active(self):
        if self.closed or self.clock() >= self.deadline or not self.stop_check():
            raise PermissionError("Original Work is stopped or Reader lease expired")

    def _call(self, action, args):
        try:
            self._active()
            self.sequence += 1
            envelope = {"identity": self.identity.copy(), "nonce": self.nonce, "sequence": self.sequence,
                        "boot_id": self.runtime["boot_id"], "container_id": self.runtime["container_id"],
                        "image_digest": self.runtime["image_digest"], "action": action, "arguments": args}
            if len(json.dumps(envelope, ensure_ascii=False, allow_nan=False).encode()) > MAX_FRAME:
                raise ValueError("Reader request is too large")
            binding = {k: envelope[k] for k in ("nonce", "sequence", "boot_id", "container_id", "image_digest")}
            binding["identity"] = self.identity.copy()
            response = self.transport.request(envelope)
            self._active()
            if (not isinstance(response, dict) or type(response.get("sequence")) is not int
                    or any(response.get(k) != binding[k]
                           for k in ("identity", "nonce", "sequence", "boot_id", "container_id", "image_digest"))):
                raise ValueError("Reader response identity mismatch")
            value = response.get("result")
            if len(json.dumps(value, ensure_ascii=False, allow_nan=False).encode()) > MAX_IMAGE * 2:
                raise ValueError("Reader response is too large")
            return value
        except BaseException:
            try:
                self.close()
            except Exception:
                pass
            raise

    def start(self):
        if not self._operation_lock.acquire(blocking=False):
            raise PermissionError("Reader operation already in progress")
        try:
            try:
                return self._start_checked()
            except BaseException:
                try:
                    self.close()
                except Exception:
                    pass
                raise
        finally:
            self._operation_lock.release()

    def _start_checked(self):
        reply = self._call("start", {})
        if not isinstance(reply, dict) or reply.get("ready") is not True:
            raise ValueError("Reader connection is not verified")
        return self

    def call(self, arguments, resources):
        if not self._operation_lock.acquire(blocking=False):
            raise PermissionError("Reader operation already in progress")
        try:
            sequence_before = self.sequence
            try:
                return self._call_checked(arguments, resources)
            except BaseException:
                if self.sequence != sequence_before:
                    try:
                        self.close()
                    except Exception:
                        pass
                raise
        finally:
            self._operation_lock.release()

    def _call_checked(self, arguments, resources):
        if any(resources.identity.get(k) != self.identity.get(k) for k in resources.identity):
            raise ValueError("Reader Work or Task identity changed")
        if not isinstance(arguments, dict):
            raise ValueError("Reader action must be an object")
        action = arguments.get("action")
        if action == "navigate" and set(arguments) == {"action", "url"}:
            self.policy.url(arguments["url"])
            result = self._call(action, {"url": arguments["url"]})
            if not isinstance(result, dict) or not result.get("tab_id"):
                raise ValueError("Reader did not return the owned tab")
            self.policy.url(result.get("url", ""))
            self.tab, self.url = result["tab_id"], result["url"]
            return {"url": self.url, "tab_id": self.tab, "content_verification": "UNVERIFIED"}
        if self.tab is None or action not in {"observe", "extract", "screenshot"}:
            raise ValueError("Reader action is not authorized")
        allowed = {"action", "target_id"} if action == "extract" else {"action"}
        if set(arguments) - allowed:
            raise ValueError("Reader arguments are not authorized")
        result = self._call(action, {"tab_id": self.tab, **({"target_id": arguments["target_id"]} if "target_id" in arguments else {})})
        if not isinstance(result, dict) or result.get("tab_id") != self.tab or result.get("url") != self.url:
            raise ValueError("Reader result left its original tab or page")
        self.policy.url(result["url"])
        if action == "screenshot":
            from .agent_tool_server import write_output
            data = base64.b64decode(result.get("image_base64", ""), validate=True)
            from .agent_work_resources import validate_reader_png
            validate_reader_png(data)
            self._active()
            token = resources.begin_browser_capture()
            receipt = write_output(resources, "browser-" + str(self.sequence) + ".png", data, _capture_token=token)
            self._active()
            resources.register_browser_capture(receipt, url=self.url, session_id=self.session, tab_id=self.tab, _capture_token=token)
            return receipt
        if len(json.dumps(result, ensure_ascii=False).encode()) > MAX_FRAME:
            raise ValueError("Reader text result is too large")
        return {"result": result, "content_verification": "UNVERIFIED"}

    def close(self):
        with self._close_lock:
            if self.closed:
                if self._close_pending:
                    raise RuntimeError("Reader stop is pending; resources remain UNKNOWN")
                if self._close_failed:
                    raise RuntimeError("Reader stop failed; resources remain UNKNOWN")
                return
            self.closed = True
            self._close_pending = True
            self.stop_state = "UNKNOWN"
        try:
            self.transport.close()
        except BaseException:
            with self._close_lock:
                self._close_failed = True
            raise
        finally:
            with self._close_lock:
                self._close_pending = False


def _pinned_browser_asset(path, expected):
    import hashlib
    import os
    import stat
    from pathlib import Path
    path = Path(path)
    if not path.is_absolute() or not os.access(path, os.X_OK):
        raise ValueError("Browser asset is not an absolute executable")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise ValueError("Browser asset is not a regular file")
        with os.fdopen(fd, "rb", closefd=False) as stream:
            actual = hashlib.file_digest(stream, "sha256").hexdigest()
    finally:
        os.close(fd)
    if actual != expected:
        raise ValueError("Browser asset changed from the acceptance release")
    return str(path)


def read_browser_marker(path):
    import os
    import stat
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        info = os.fstat(fd)
        if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid()
                or info.st_size > 65536 or stat.S_IMODE(info.st_mode) & 0o022):
            raise ValueError("Browser ownership marker is not a private regular file")
        with os.fdopen(fd, "rb", closefd=False) as stream:
            return stream.read(65537).decode("utf-8")
    finally:
        os.close(fd)


def browser_bundle_digest(root):
    """Pin the complete Chrome bundle, including framework bytes and symlink targets."""
    import hashlib
    import os
    from pathlib import Path
    root = Path(root)
    result = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        relative = str(path.relative_to(root))
        if path.is_symlink():
            item = [relative, "link", os.readlink(path)]
        elif path.is_file():
            with path.open("rb") as stream:
                item = [relative, "file", hashlib.file_digest(stream, "sha256").hexdigest()]
        elif path.is_dir():
            continue
        else:
            raise ValueError("Unexpected browser bundle entry")
        result.update((json.dumps(item, ensure_ascii=False, separators=(",", ":")) + "\n").encode())
    return result.hexdigest()


def browser_environment(directory, session):
    from pathlib import Path
    root = Path(directory)
    return {"PATH": "/usr/bin:/bin", "HOME": str(root / "home"), "TMPDIR": str(root / "tmp"),
        "XDG_CONFIG_HOME": str(root / "config"), "XDG_CACHE_HOME": str(root / "cache"),
        "AGENT_BROWSER_SOCKET_DIR": str(root / "s"), "AGENT_BROWSER_DEFAULT_TIMEOUT": "12000",
        "AGENT_BROWSER_SESSION": session}


def agent_browser_release(*, verify_assets=True):
    """Existing bundled release authority; never a Work payload or private grant."""
    import hashlib
    import os
    import re
    from pathlib import Path
    lock = load_trusted_reader_lock()
    profile = lock.get("agentBrowser")
    fields = {"cliPath", "cliSha256", "chromePath", "chromeSha256", "chromeBundleSha256",
        "stopEvidenceRef", "stopEvidenceSha256", "boundary", "methods"}
    if (lock.get("runtimeKind") != "NATIVE_AGENT_BROWSER" or type(profile) is not dict
            or set(profile) != fields
            or profile["boundary"] != "FIXED_COMMANDS_FRESH_PROFILE_PUBLIC_READ_PROXY"
            or profile["methods"] != ["GET", "HEAD"]
            or not isinstance(profile["stopEvidenceRef"], str) or not profile["stopEvidenceRef"].strip()
            or any(not re.fullmatch(r"[0-9a-f]{64}", str(profile[k])) for k in
                ("cliSha256", "chromeSha256", "chromeBundleSha256", "stopEvidenceSha256"))):
        raise ValueError("受管 agent-browser 构建、边界与独立停止证据尚未发布。")
    release = {**profile, "temporaryRoot": "/private/tmp/curis-public-browser-" + str(os.getuid()),
        "releaseSha256": hashlib.sha256(json.dumps(lock, sort_keys=True, separators=(",", ":")).encode()).hexdigest()}
    if verify_assets:
        _pinned_browser_asset(release["cliPath"], release["cliSha256"])
        chrome = Path(_pinned_browser_asset(release["chromePath"], release["chromeSha256"]))
        bundle = chrome.parents[2]
        if bundle.suffix != ".app" or browser_bundle_digest(bundle) != release["chromeBundleSha256"]:
            raise ValueError("浏览器完整构建与固定发布版本不一致。")
    return release


def validate_browser_supervisor_request(request):
    import os
    import re
    import stat
    from pathlib import Path
    from .agent_work_resources import scope_key
    lock = agent_browser_release(verify_assets=False)
    _pinned_browser_asset(lock["cliPath"], lock["cliSha256"])
    directory = Path(request.get("cwd", ""))
    if directory.parent != Path(lock["temporaryRoot"]) or not re.fullmatch(r"[0-9a-f]{16}", directory.name):
        raise ValueError("Browser supervisor directory is outside its owned root")
    identity = json.loads(read_browser_marker(directory / "owner.json"))
    required = {"tenant_id", "company_id", "employee_id", "binding_ref", "work_ref", "task_id"}
    if (type(identity) is not dict or set(identity) != required
            or any(type(v) is not str or not v or len(v) > 256 for v in identity.values())
            or directory.name != scope_key(**{k: identity[k] for k in
                ("tenant_id", "company_id", "work_ref", "task_id")})[:16]):
        raise ValueError("Browser directory does not match its original Task")
    if json.loads(read_browser_marker(directory.parent / "release.json")) != {
            "runtimeKind": "NATIVE_AGENT_BROWSER", "releaseSha256": lock["releaseSha256"]}:
        raise ValueError("Browser root belongs to another release")
    session = request.get("environment", {}).get("AGENT_BROWSER_SESSION", "")
    if (not re.fullmatch(r"[0-9a-f]{12}", session) or request.get("command") != [lock["cliPath"]]
            or request.get("cwd") != str(directory) or request.get("prompt") != ""
            or request.get("environment") != {**browser_environment(directory, session), "AGENT_BROWSER_DAEMON": "1"}):
        raise ValueError("Browser supervisor permits only the fixed foreground daemon")
    for path in (directory.parent, directory, directory / "s", directory / "home", directory / "tmp", directory / "config", directory / "cache"):
        info = path.lstat()
        if (not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid()
                or stat.S_IMODE(info.st_mode) != 0o700 or str(path.resolve()) != str(path)):
            raise ValueError("Browser supervisor requires an owned private directory")
    if read_browser_marker(directory / "s" / (session + ".config")) != '{"debug":false}':
        raise ValueError("Browser daemon startup configuration changed")


def run_browser_supervisor():
    from .agent_adapter import _run_agent_supervisor_candidate
    try:
        agent_browser_release(verify_assets=False)
    except (ValueError, OSError, KeyError, TypeError):
        return 2
    return _run_agent_supervisor_candidate(request_validator=validate_browser_supervisor_request)


def open_agent_browser_for_work(identity, should_stop, *, hosts, source_url):
    from .agent_browser import AgentBrowserLease
    from .agent_browser_policy import PublicTargets
    required = {"tenant_id", "company_id", "employee_id", "binding_ref", "work_ref", "task_id"}
    if (type(identity) is not dict or set(identity) != required or not callable(should_stop)
            or any(type(v) is not str or not v or len(v) > 256 for v in identity.values())):
        raise ValueError("Browser requires the complete original Work identity")
    policy = PublicTargets(hosts)
    policy.url(source_url)
    if "#" in source_url:
        raise ValueError("Source URL cannot contain a fragment")
    if should_stop():
        raise PermissionError("Original research Task is stopped")
    release = agent_browser_release()
    if should_stop():
        raise PermissionError("Original research Task is stopped")
    return AgentBrowserLease({**release, "hosts": sorted(policy.hosts), "sourceUrl": source_url}, identity, should_stop)
