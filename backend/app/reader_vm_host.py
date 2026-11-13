"""Per-Work Reader owner; execution requires a separately released pinned VM lock."""
from __future__ import annotations

import hashlib
import threading
from contextvars import ContextVar

from .agent_browser_runtime import ReaderLease


# Process-local tombstones only. A released owner also needs a durable ledger and
# authenticated Docker/VM identity; restarting Python must never authorize reuse.
_HOLD_LOCK = threading.Lock()
_WORK_HOLDS = {}
_CONTAINER_HOLDS = {}
_WORK_OWNER_SCOPE = ContextVar("curis_original_work_owner", default=None)
_UNRESOLVED_WORK_OWNERS = []


def _hold_work(owner, identity):
    key = tuple(identity[k] for k in ("tenant_id", "company_id", "work_ref"))
    with _HOLD_LOCK:
        if key in _WORK_HOLDS:
            raise PermissionError("Reader Work has an unresolved owner; reuse is forbidden")
        hold = {"owner": owner, "identity": identity.copy(), "runtime": None, "nonce": None}
        _WORK_HOLDS[key] = hold
        return hold


def _hold_container(hold, snapshot):
    fixed = _snapshot(snapshot)
    # Image is deliberately excluded: changing an image must not evade the hold.
    key = (fixed["boot_id"], fixed["container_id"])
    with _HOLD_LOCK:
        if hold["runtime"] is not None or key in _CONTAINER_HOLDS:
            raise PermissionError("Reader container has an unresolved owner; reuse is forbidden")
        hold["runtime"] = fixed
        _CONTAINER_HOLDS[key] = hold



def _released_vm_image():
    import re
    from .agent_browser_runtime import load_trusted_reader_lock
    try:
        lock = load_trusted_reader_lock()
    except (ValueError, OSError) as error:
        raise PermissionError("Reader VM runtime is not released; Reader remains closed") from error
    closure = {"kind": "DEDICATED_DOCKER_SSH_V1", "root": _OWNER_ROOT,
               "alias": _OWNER_ALIAS, "hostKeySha256": _OWNER_HOST_KEY_SHA256,
               "seccompSha256": _PRIVATE_SECCOMP_SHA256}
    image = lock.get("browserImageDigest")
    if (lock.get("complete") is not True or lock.get("executionAuthorized") is not True
            or lock.get("runtimeKind") != "VM" or lock.get("hostHelperClosure") != closure
            or type(image) is not str or not re.fullmatch(r"sha256:[0-9a-f]{64}", image)
            or lock.get("proxyImageDigest") != image):
        raise PermissionError("Reader VM runtime is not released; Reader remains closed")
    return image


def _open_verified_vm_owner(identity):
    # Construction performs no allocation. The Work hold must precede prepare().
    try:
        image = _released_vm_image()
    except PermissionError as error:
        raise ValueError("Reader VM platform verification is not released") from error
    return _DedicatedDockerOwner(identity, image)


def _request_owned_stop(owner, identity, *, nonce=None, snapshot=None):
    """One bounded exact-generation stop; never fall back to identity-only stop."""
    if snapshot is None:
        raise PermissionError("Reader container identity is unverified; stop remains UNKNOWN")
    # Stopping an exact prepared generation does not authorize it to execute.
    fixed = _snapshot(snapshot, authorized=False)
    stop_bound = getattr(owner, "revoke_bound_and_stop", None)
    if not callable(stop_bound):
        raise ValueError("Reader owner lacks exact-generation stop")
    work = identity.copy()
    done, failure = threading.Event(), []
    def stop():
        try:
            stop_bound(work.copy(), nonce, fixed.copy())
        except BaseException as error:
            failure.append(error)
        finally:
            done.set()
    threading.Thread(target=stop, daemon=True).start()
    if not done.wait(timeout=1):
        raise TimeoutError("Reader stop request deadline exceeded; resources remain UNKNOWN")
    if failure:
        raise failure[0]


class _DeferredTransport:
    def __init__(self, owner, identity, snapshot, *, _hold=None):
        import threading
        if (not callable(getattr(owner, "dispatch_if_active", None))
                or not callable(getattr(owner, "revoke_bound_and_stop", None))):
            raise ValueError("Reader platform lacks atomic revocation and exact-generation independent stop")
        self._transport = None
        self._owner = owner
        self._identity = identity.copy()
        self._snapshot = _snapshot(snapshot)
        self._hold = _hold if _hold is not None else _hold_work(owner, identity)
        if self._hold["owner"] is not owner or self._hold["identity"] != identity:
            raise PermissionError("Reader owner hold mismatch")
        _hold_container(self._hold, self._snapshot)
        self._nonce = None
        self._sequence = 0
        self._request_lock = threading.Lock()
        self._closed = False
        self._stop_error = False
        self._stop_pending = False
        self.stop_state = "UNKNOWN"
        self._lock = threading.Lock()

    def bind(self, transport, nonce):
        if not callable(getattr(transport, "request", None)) or not callable(getattr(transport, "close", None)):
            raise ValueError("Reader transport is invalid")
        if (type(nonce) is not str or len(nonce) != 48
                or any(c not in "0123456789abcdef" for c in nonce)):
            raise ValueError("Reader session nonce is invalid")
        with self._lock:
            if self._closed or self._transport is not None:
                raise PermissionError("Reader transport is unavailable")
            self._transport = transport
            self._nonce = nonce
            with _HOLD_LOCK:
                if self._hold["nonce"] is not None:
                    raise PermissionError("Reader original nonce cannot be rebound")
                self._hold["nonce"] = nonce

    def request(self, frame):
        if not self._request_lock.acquire(blocking=False):
            raise PermissionError("Reader request already in progress")
        try:
            return self._request(frame)
        finally:
            self._request_lock.release()

    def _request(self, frame):
        # Snapshot caller data before trusting it or handing it to the owner.
        if type(frame) is not dict:
            raise PermissionError("Reader request binding mismatch")
        bound = {"identity": self._identity.copy(), "nonce": self._nonce,
                 **{k: self._snapshot[k] for k in ("boot_id", "container_id", "image_digest")}}
        if (any(frame.get(k) != v for k, v in bound.items())
                or type(frame.get("identity")) is not dict):
            raise PermissionError("Reader request binding mismatch")
        request = dict(frame, identity=self._identity.copy())
        with self._lock:
            if self._closed or self._transport is None:
                raise PermissionError("Reader transport is unavailable")
            if type(frame.get("sequence")) is not int or frame["sequence"] != self._sequence + 1:
                raise PermissionError("Reader request sequence mismatch")
            sequence = frame["sequence"]
            transport = self._transport
        if _snapshot(self._owner.verified_snapshot(self._identity.copy())) != self._snapshot:
            raise PermissionError("Reader runtime changed")
        with self._lock:
            if self._closed:
                raise PermissionError("Reader transport is unavailable")
            self._sequence = sequence  # Consume admission; never replay an uncertain request.
        # The verified platform must serialize remote admission against revocation.
        response = self._owner.dispatch_if_active(self._identity.copy(), transport, request)
        if _snapshot(self._owner.verified_snapshot(self._identity.copy())) != self._snapshot:
            raise PermissionError("Reader runtime changed")
        with self._lock:
            if self._closed:
                raise PermissionError("Reader response arrived after revocation")
            return response

    def close(self):
        with self._lock:
            if self._closed:
                if self._stop_error:
                    raise RuntimeError("Reader stop request failed; owned resources remain UNKNOWN")
                if self._stop_pending:
                    raise RuntimeError("Reader stop request is pending; owned resources remain UNKNOWN")
                return
            self._closed = True
            self._stop_pending = True
        # Stop runs independently of a blocked request or transport close.
        try:
            _request_owned_stop(self._owner, self._identity, nonce=self._nonce, snapshot=self._snapshot)
        except BaseException:
            with self._lock:
                self._stop_error = True
            raise
        finally:
            with self._lock:
                self._stop_pending = False
        # A completed owner call is not independent proof of process/egress exit.
        # Keep UNKNOWN even if a late worker or self-reported return says GONE.


def _snapshot(raw, *, authorized=True):
    if type(raw) is not dict:
        raise ValueError("Reader Work runtime is not verified")
    value = raw.copy()
    keys = {"complete", "executionAuthorized", "boot_id", "container_id", "image_digest"}
    if (any(type(key) is not str for key in value) or set(value) != keys
            or any(type(value[k]) is not bool for k in ("complete", "executionAuthorized"))
            or value["complete"] != value["executionAuthorized"]
            or (authorized and value["complete"] is not True)
            or any(type(value[key]) is not str or not value[key]
                   for key in ("boot_id", "container_id", "image_digest"))):
        raise ValueError("Reader Work runtime is not verified")
    return value


def open_owned_reader(identity, policy, should_stop):
    """Open one original Work through the existing owner and owned stop path.

    The bundled lock remains the release authority. Stops and all descendant
    effects remain UNKNOWN even after a successful original Docker stop request.
    """
    required = ("tenant_id", "company_id", "work_ref", "task_id", "employee_id", "binding_ref")
    if type(identity) is not dict or not callable(should_stop):
        raise ValueError("Reader Work identity is invalid")
    fixed = identity.copy()
    if (any(type(key) is not str for key in fixed) or set(fixed) != set(required)
            or any(type(fixed[key]) is not str or not fixed[key] for key in required)):
        raise ValueError("Reader Work identity is invalid")
    if should_stop():
        raise PermissionError("Original Work is stopped")
    owner = _open_verified_vm_owner(fixed.copy())
    parent = _WORK_OWNER_SCOPE.get()
    if parent is not None and isinstance(owner, _DedicatedDockerOwner):
        parent.bind(owner, "reader")
    # Claim once before any owner operation that could allocate or bind resources.
    # No automatic release, even after a successful stop or failed initialization.
    hold = _hold_work(owner, fixed)
    lease, snapshot = None, None
    try:
        if isinstance(owner, _DedicatedDockerOwner):
            import secrets
            if should_stop():
                raise PermissionError("Original Work is stopped")
            owner.prepare(secrets.token_hex(24), hosts=sorted(policy.hosts))
            if should_stop():
                raise PermissionError("Original Work stopped after preparation")
            owner.start_runtime()
        snapshot = _snapshot(owner.verified_snapshot(fixed.copy()))
        if should_stop():
            raise PermissionError("Original Work is stopped")
        transport = _DeferredTransport(owner, fixed, snapshot, _hold=hold)
        reserved_nonce = getattr(owner, "nonce", None)
        if isinstance(owner, _DedicatedDockerOwner) and reserved_nonce is None:
            raise PermissionError("Dedicated Reader owner has no durably reserved nonce")
        lease = ReaderLease(fixed, policy, transport, snapshot, nonce=reserved_nonce, alive=lambda: not should_stop())
        channel = owner.bind_session(fixed.copy(), lease.nonce, snapshot.copy())
        # Do not close a rejected channel without independently proven ownership.
        transport.bind(channel, lease.nonce)
        if should_stop() or _snapshot(owner.verified_snapshot(fixed.copy())) != snapshot:
            raise PermissionError("Original Work stopped or runtime changed")
        lease.start()
        return lease
    except BaseException as error:
        if lease is not None:
            try:
                lease.close()
            except BaseException:
                error.add_note("Owned Reader stop request failed; resources remain UNKNOWN")
            if transport.stop_state == "UNKNOWN":
                error.add_note("Owned Reader stop and resource state remain UNKNOWN")
        else:
            try:
                if isinstance(owner, _DedicatedDockerOwner):
                    if owner.stop_requested or not owner.container_id:
                        raise PermissionError("Original startup cleanup already requested or binding unknown; no retry")
                    _request_owned_stop(owner, fixed, nonce=owner.nonce, snapshot={
                        "complete": False, "executionAuthorized": False,
                        "boot_id": owner.boot_id, "container_id": owner.container_id,
                        "image_digest": owner.image_digest})
                else:
                    if hold["runtime"] is None:
                        raise PermissionError("Reader container was not exclusively held; no stop issued")
                    _request_owned_stop(owner, fixed, snapshot=hold["runtime"])
            except BaseException:
                error.add_note("Owned Reader stop request failed; resources remain UNKNOWN")
            error.add_note("Owned Reader stop and resource state remain UNKNOWN")
        raise


# Dedicated private owner primitives; the bundled release gate remains closed.
_OWNER_ROOT = "/Users/yy/.curis-browser-runtime-01"
_OWNER_ALIAS = "curis-browser"
_OWNER_HOST_KEY_SHA256 = "jm86bQdc4bmfo/u0cLn1zPTKjmwRRWho6rYzm4//4Vk"
_OWNER_KNOWN_HOSTS = "reader-owner-known_hosts-v2"
_OWNER_KNOWN_HOSTS_FILE_SHA256 = "314d9fc2d35aa139b4fa9061148e761e69db3b39339e11b22a2bf11bafcc3f6e"
_PRIVATE_SECCOMP_SHA256 = "ec8c5efc21c700fcfb255382287131ee9c6e1019bb226ad3d4a689d60bedded3"
# 13s navigate IPC + 5s owned-tab verification + 3s framing margin; original Work cancellation still applies.
_READER_ATTACH_TIMEOUT_SECONDS = 21


def _owner_directory():
    import os, stat, sys
    if sys.platform != "darwin" or os.getuid() != 501 or os.geteuid() != 501:
        raise PermissionError("Dedicated owner platform is not authorized")
    root = os.open(_OWNER_ROOT, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        info = os.fstat(root)
        if (info.st_dev, info.st_ino, info.st_uid, stat.S_IMODE(info.st_mode)) != (16777229, 93818520, 501, 0o700):
            raise PermissionError("Dedicated owner root identity changed")
        client = os.open("client", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=root)
        info = os.fstat(client)
        if info.st_uid != 501 or stat.S_IMODE(info.st_mode) != 0o700:
            os.close(client)
            raise PermissionError("Dedicated owner client directory is not private")
        return client
    finally:
        os.close(root)


def _owner_file(directory, name, flags):
    import os, stat
    fd = os.open(name, flags | os.O_NOFOLLOW | os.O_NONBLOCK, 0o600, dir_fd=directory)
    try:
        info = os.fstat(fd)
        if (not stat.S_ISREG(info.st_mode) or info.st_uid != 501 or info.st_nlink != 1
                or stat.S_IMODE(info.st_mode) != 0o600 or info.st_size > 1048576):
            raise PermissionError("Dedicated owner file identity or size invalid")
        return fd
    except BaseException:
        os.close(fd)
        raise


def _ssh_owner_inputs(config, known_hosts):
    """Parse only the new Owner-enrolled public files; never read a private key."""
    import base64, hashlib, re, shlex, struct
    if hashlib.sha256(known_hosts.encode("ascii")).hexdigest() != _OWNER_KNOWN_HOSTS_FILE_SHA256:
        raise PermissionError("Owner known_hosts-v2 file differs from accepted bytes")
    fields = {}
    for line in config.splitlines():
        parts = shlex.split(line, comments=True)
        if not parts:
            continue
        if len(parts) != 2 or parts[0].lower() in fields:
            raise PermissionError("Owner SSH configuration must be explicit and unique")
        fields[parts[0].lower()] = parts[1]
    if (set(fields) != {"host", "hostname", "port", "user", "identityfile"}
            or fields["host"] != _OWNER_ALIAS or fields["hostname"] != "127.0.0.1"
            or not re.fullmatch(r"[0-9]{1,5}", fields["port"]) or not 1 <= int(fields["port"]) <= 65535
            or not re.fullmatch(r"[a-z_][a-z0-9_-]{0,31}", fields["user"]) or fields["user"] == "root"
            or fields["identityfile"] != _OWNER_ROOT + "/lima/_config/user"):
        raise PermissionError("Owner SSH configuration is outside dedicated scope")
    parts = known_hosts.strip().split()
    if len(parts) != 3 or parts[:2] != [_OWNER_ALIAS, "ssh-ed25519"]:
        raise PermissionError("A single independently enrolled VM host key is required")
    try:
        key = base64.b64decode(parts[2], validate=True)
    except ValueError as error:
        raise PermissionError("Owner public host key is malformed") from error
    if key != struct.pack(">I", 11) + b"ssh-ed25519" + struct.pack(">I", 32) + key[-32:] or len(key) != 51:
        raise PermissionError("Owner public host key is not Ed25519")
    if base64.b64encode(hashlib.sha256(key).digest()).decode().rstrip("=") != _OWNER_HOST_KEY_SHA256:
        raise PermissionError("VM host key does not match independently enrolled fingerprint")
    return fields


# Same authenticated SSH session reads kernel boot ID before touching Docker.
_DOCKER_RPC_SOURCE = r"""
import http.client, json, re, socket, sys
from pathlib import Path
request = json.loads(sys.stdin.buffer.read(65537))
boot = Path('/proc/sys/kernel/random/boot_id').read_text().strip()
assert re.fullmatch(r'[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}', boot)
assert request['boot_id'] is None or request['boot_id'] == boot
class Docker(http.client.HTTPConnection):
    def connect(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.settimeout(3)
        self.sock.connect('/var/run/docker.sock')
connection = Docker('docker', timeout=3)
try:
    body = json.dumps(request['body']).encode() if request['body'] is not None else None
    connection.request(request['method'], '/v1.53' + request['path'], body, {'Content-Type':'application/json'})
    response = connection.getresponse()
    data = response.read(1048577)
    assert len(data) <= 1048576
    print(json.dumps({'boot_id':boot,'status':response.status,'body':json.loads(data) if data else None}, separators=(',',':')))
finally:
    connection.close()
"""


def _ssh_public_snapshot(fds):
    """Hold and recheck only the two public enrollment files, never the private key."""
    import os, stat
    if len(fds) != 2 or len(set(fds)) != 2:
        raise PermissionError("Owner public enrollment descriptors invalid")
    identities, texts = [], []
    def identity(info):
        return (info.st_dev,info.st_ino,info.st_uid,info.st_mode,info.st_nlink,
                info.st_size,info.st_mtime_ns,info.st_ctime_ns)
    for fd in fds:
        before = os.fstat(fd)
        if (not stat.S_ISREG(before.st_mode) or before.st_uid != os.geteuid()
                or stat.S_IMODE(before.st_mode) != 0o600 or before.st_nlink != 1
                or not 0 < before.st_size <= 65536):
            raise PermissionError("Owner public enrollment identity invalid")
        raw = os.pread(fd,65537,0)
        if len(raw) != before.st_size or identity(before) != identity(os.fstat(fd)):
            raise PermissionError("Owner public enrollment changed during read")
        identities.append(identity(before))
        texts.append(raw.decode("ascii"))
    _ssh_owner_inputs(*texts)
    return tuple(identities),tuple(texts)


def _ssh_owner_argv(config_fd, hosts_fd):
    _,texts = _ssh_public_snapshot((config_fd,hosts_fd))
    fields = _ssh_owner_inputs(*texts)
    import shlex
    # OpenSSH closes inherited FDs at startup. Serialize only verified public
    # values; the fixed pin command avoids reopening a mutable known_hosts path.
    options = {"StrictHostKeyChecking":"yes", "UserKnownHostsFile":"/dev/null",
        # OpenSSH expands %% to a literal % before executing its fixed argv.
        "KnownHostsCommand":shlex.join(["/usr/bin/printf",r"%%s\n"," ".join(texts[1].split())]),
        "HostName":fields["hostname"],"Port":fields["port"],"User":fields["user"],
        "IdentityFile":fields["identityfile"],"AddressFamily":"inet","CanonicalizeHostname":"no",
        "ProxyCommand":"none","ProxyJump":"none",
        "GlobalKnownHostsFile":"/dev/null", "HostKeyAlias":_OWNER_ALIAS, "HostKeyAlgorithms":"ssh-ed25519",
        "NoHostAuthenticationForLocalhost":"no", "UpdateHostKeys":"no", "VerifyHostKeyDNS":"no",
        "CheckHostIP":"no", "ControlMaster":"no", "ControlPath":"none", "BatchMode":"yes",
        "IdentityAgent":"none", "IdentitiesOnly":"yes", "UseKeychain":"no", "AddKeysToAgent":"no",
        "PKCS11Provider":"none", "GSSAPIAuthentication":"no", "PasswordAuthentication":"no",
        "KbdInteractiveAuthentication":"no", "ForwardAgent":"no", "ForwardX11":"no",
        "ClearAllForwardings":"yes", "PermitLocalCommand":"no", "ConnectTimeout":"3"}
    return ["/usr/bin/ssh", "-T", "-F", "/dev/null",
            *[arg for key,value in options.items() for arg in ("-o", key+"="+value)], _OWNER_ALIAS,
            "/usr/bin/python3 -I -B -c " + shlex.quote(_DOCKER_RPC_SOURCE)]


_FILTER_STAGES = {"input", "boot", "image", "container", "process", "namespace", "rules", "final",
    "enter", "precheck4", "precheck6", "restore4", "restore6", "verify4", "verify6"}
_FILTER_ERROR_KINDS = {"PermissionError", "TimeoutError", "ValueError", "OSError", "OTHER"}


def _filter_failure_diagnostic(raw):
    import json
    if not 0 < len(raw) <= 512: return None
    try:
        value = json.loads(raw)
        if (type(value) is not dict or set(value) != {"curis_filter_failure","stage","kind","exit_code"}
                or type(value["curis_filter_failure"]) is not int or value["curis_filter_failure"] != 1
                or value["stage"] not in _FILTER_STAGES or value["kind"] not in _FILTER_ERROR_KINDS
                or (value["exit_code"] is not None and (type(value["exit_code"]) is not int
                    or not -64 <= value["exit_code"] <= 255 or value["exit_code"] == 0))
                or raw != (json.dumps(value,sort_keys=True,separators=(",", ":"))+"\n").encode()):
            return None
        return value
    except (ValueError, TypeError): return None


def _bounded_ssh_exchange(argv, fds, payload, seconds):
    import os, select, subprocess, time
    if type(seconds) not in {int, float} or not 0 < seconds <= 5:
        raise TimeoutError("Owner SSH budget unavailable; no process started")
    public_before = _ssh_public_snapshot(fds)
    if argv[:-1] != _ssh_owner_argv(*fds)[:-1]:
        raise PermissionError("Owner SSH arguments differ from verified enrollment")
    deadline = time.monotonic() + seconds
    process = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        cwd=_OWNER_ROOT, env={"PATH":"/usr/bin:/bin", "LANG":"C.UTF-8", "HOME":_OWNER_ROOT+"/home"},
        close_fds=True, pass_fds=())
    output = bytearray()
    try:
        os.set_blocking(process.stdin.fileno(), False)
        os.set_blocking(process.stdout.fileno(), False)
        pending = memoryview(payload)
        while pending:
            remaining = deadline - time.monotonic()
            if remaining <= 0 or not select.select([], [process.stdin.fileno()], [], remaining)[1]:
                raise TimeoutError("Owner SSH write deadline expired; outcome UNKNOWN")
            try:
                written = os.write(process.stdin.fileno(), pending)
            except BlockingIOError:
                continue
            if written <= 0:
                raise OSError("Owner SSH stdin closed")
            pending = pending[written:]
        process.stdin.close()
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0 or not select.select([process.stdout.fileno()], [], [], remaining)[0]:
                raise TimeoutError("Owner SSH response deadline expired; outcome UNKNOWN")
            try:
                chunk = os.read(process.stdout.fileno(), 65536)
            except BlockingIOError:
                continue
            if not chunk:
                break
            output.extend(chunk)
            if len(output) > 2097152:
                raise ValueError("Owner SSH response oversized; outcome UNKNOWN")
        exit_code = process.wait(timeout=max(0, deadline-time.monotonic()))
        if _ssh_public_snapshot(fds) != public_before:
            raise PermissionError("Owner public enrollment changed during SSH; outcome UNKNOWN")
        if exit_code != 0:
            # Never include raw stderr, configuration, key material or remote output.
            import shlex
            diagnostic = (_filter_failure_diagnostic(bytes(output)) if argv[-1] ==
                "/usr/bin/sudo -n /usr/bin/python3 -I -S -B -c " + shlex.quote(_NETNS_ROOT_SOURCE+"\nmain()\n") else None)
            detail = (f", filter_stage={diagnostic['stage']}, kind={diagnostic['kind']}, child_exit={diagnostic['exit_code']}"
                if diagnostic else "")
            raise PermissionError(f"Owner SSH process failed (exit={exit_code}, stdout_bytes={len(output)}{detail}); outcome UNKNOWN")
        return bytes(output)
    finally:
        try:
            if process.poll() is None:
                process.terminate()  # Held direct child, never a discovered PID or group.
                try:
                    process.wait(timeout=0.2)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=0.2)
        finally:
            process.stdout.close()
            if not process.stdin.closed:
                process.stdin.close()


_NETNS_RULES_V4 = """*filter
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT DROP [0:0]
-A INPUT -s 127.0.0.1/32 -d 127.0.0.1/32 -i lo -p tcp -m tcp --dport 52800 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
-A INPUT -s 127.0.0.1/32 -d 127.0.0.1/32 -i lo -p tcp -m tcp --sport 52800 -m conntrack --ctstate ESTABLISHED -j ACCEPT
-A INPUT -s 172.30.253.2/32 -d 172.30.253.3/32 -i eth0 -p tcp -m tcp --sport 8443 -m conntrack --ctstate ESTABLISHED -j ACCEPT
-A OUTPUT -s 127.0.0.1/32 -d 127.0.0.1/32 -o lo -p tcp -m tcp --dport 52800 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
-A OUTPUT -s 127.0.0.1/32 -d 127.0.0.1/32 -o lo -p tcp -m tcp --sport 52800 -m conntrack --ctstate ESTABLISHED -j ACCEPT
-A OUTPUT -s 172.30.253.3/32 -d 172.30.253.2/32 -o eth0 -p tcp -m tcp --dport 8443 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
COMMIT
"""
_NETNS_RULES_V6 = """*filter
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT DROP [0:0]
COMMIT
"""
_NETNS_FILTER_SHA256 = hashlib.sha256((_NETNS_RULES_V4 + "\0" + _NETNS_RULES_V6).encode()).hexdigest()
_NETNS_PAIRED_RULES_V4 = _NETNS_RULES_V4.replace("172.30.253.", "172.30.251.")
_NETNS_PAIRED_FILTER_SHA256 = hashlib.sha256((_NETNS_PAIRED_RULES_V4 + "\0" + _NETNS_RULES_V6).encode()).hexdigest()

# Fixed code executed only by the authenticated guest helper. No command, PID,
# rule text or path is accepted from a Work. Only the owned netns filter table is touched.
_NETNS_COMMON_SOURCE = "RULES4 = " + repr(_NETNS_RULES_V4) + "\nRULES6 = " + repr(_NETNS_RULES_V6) + r'''
import hashlib, json, os, re, select, shlex, stat, subprocess, sys, time
RULE_HASH = hashlib.sha256((RULES4 + "\0" + RULES6).encode()).hexdigest()

def decode(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result: raise ValueError("duplicate helper field")
            result[key] = value
        return result
    def invalid(value): raise ValueError("nonfinite helper field")
    return json.loads(raw, object_pairs_hook=unique, parse_constant=invalid)

_filter_stage = "enter"

class FilterChildFailure(PermissionError):
    def __init__(self, stage, kind, code):
        super().__init__("fixed filter child failed")
        self.stage,self.kind,self.code = stage,kind,code

def child_diagnostic(raw):
    if not 0 < len(raw) <= 512: return None
    try:
        v=decode(raw)
        if (type(v) is not dict or set(v)!={"curis_filter_failure","stage","kind","exit_code"}
                or type(v["curis_filter_failure"]) is not int or v["curis_filter_failure"]!=1
                or v["stage"] not in {"enter","precheck4","precheck6","restore4","restore6","verify4","verify6"}
                or v["kind"] not in {"PermissionError","TimeoutError","ValueError","OSError","OTHER"}
                or (v["exit_code"] is not None and (type(v["exit_code"]) is not int
                    or not -64<=v["exit_code"]<=255 or v["exit_code"]==0))
                or raw!=(json.dumps(v,sort_keys=True,separators=(",", ":"))+"\n").encode()):return None
        return v
    except (ValueError,TypeError):return None

def emit_failure(error):
    kind=error.kind if isinstance(error,FilterChildFailure) else type(error).__name__
    if kind not in {"PermissionError","TimeoutError","ValueError","OSError"}:kind="OTHER"
    stage=error.stage if isinstance(error,FilterChildFailure) else _filter_stage
    code=error.code if isinstance(error,FilterChildFailure) else None
    print(json.dumps({"curis_filter_failure":1,"stage":stage,"kind":kind,"exit_code":code},
        sort_keys=True,separators=(",", ":")),flush=True)

def run(argv, deadline, data=None, pass_fds=(), seconds=1):
    # System-owned tools, fixed argv, bounded stdout; never a shell or process-group signal.
    tool = os.path.realpath(argv[0])
    info = os.stat(tool)
    if not tool.startswith("/usr/") or not stat.S_ISREG(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o022:
        raise PermissionError("system helper identity invalid")
    end = min(deadline, time.monotonic() + seconds)
    if end <= time.monotonic(): raise TimeoutError("filter budget expired")
    process = subprocess.Popen(argv, stdin=subprocess.PIPE if data is not None else subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, cwd="/", env={"PATH":"/usr/bin:/usr/sbin:/bin", "LANG":"C"},
        close_fds=True, pass_fds=pass_fds)
    output = bytearray()
    try:
        os.set_blocking(process.stdout.fileno(), False)
        pending = memoryview(data) if data is not None else memoryview(b"")
        if process.stdin is not None: os.set_blocking(process.stdin.fileno(), False)
        while True:
            if process.stdin is not None and not process.stdin.closed and not pending: process.stdin.close()
            remaining = end-time.monotonic()
            if remaining <= 0: raise TimeoutError("filter child timeout")
            readable, writable, _ = select.select([process.stdout],
                [process.stdin] if pending else [], [], remaining)
            if writable:
                try: count = os.write(process.stdin.fileno(), pending)
                except BlockingIOError: count = 0
                if count: pending = pending[count:]
            if readable:
                try: chunk = os.read(process.stdout.fileno(), 4096)
                except BlockingIOError: continue
                if not chunk:
                    if pending: raise OSError("filter stdin closed early")
                    break
                output.extend(chunk)
                if len(output) > 65536: raise ValueError("filter child output exceeded bound")
        code=process.wait(timeout=max(.001,end-time.monotonic()))
        if code != 0:
            diagnostic=(child_diagnostic(bytes(output)) if argv[0]=="/usr/bin/nsenter" and
                argv[-1]==globals().get("ENTER_SOURCE","")+"\nmain()\n" else None)
            if diagnostic is not None:
                raise FilterChildFailure(diagnostic["stage"],diagnostic["kind"],diagnostic["exit_code"])
            raise FilterChildFailure(_filter_stage,"PermissionError",code if type(code) is int and -64<=code<=255 else None)
        return bytes(output)
    finally:
        pending, errors = sys.exception(), []
        if process.poll() is None:
            try: process.terminate()
            except BaseException as error: errors.append(error)
            try: process.wait(timeout=.2)
            except subprocess.TimeoutExpired:
                try: process.kill()
                except BaseException as error: errors.append(error)
                try: process.wait(timeout=.2)
                except BaseException as error: errors.append(error)
            except BaseException as error: errors.append(error)
        for stream in (process.stdout,process.stdin):
            if stream is not None and not stream.closed:
                try: stream.close()
                except BaseException as error: errors.append(error)
        if errors:
            interrupt = next((error for error in errors if not isinstance(error,Exception)),None)
            if pending is not None and not isinstance(pending,Exception):
                pending.add_note("Filter child cleanup remains UNKNOWN")
            elif interrupt is not None: raise interrupt
            elif pending is not None: pending.add_note("Filter child cleanup remains UNKNOWN")
            else: raise errors[0]

def normal(raw):
    result = []
    for line in raw.decode("ascii").splitlines():
        if not line or line.startswith("#"): continue
        fields = shlex.split(line)
        if fields and fields[0].startswith(":"):
            if len(fields) != 3 or not re.fullmatch(r"\[\d+:\d+\]", fields[2]):
                raise ValueError("invalid filter counter")
            fields[2] = "[0:0]"
        result.append(tuple(fields))
    return result

def empty_filter(raw):
    rows = normal(raw)
    if not rows: return True
    if rows[0] != ("*filter",) or rows[-1] != ("COMMIT",) or len(rows) != 5: return False
    chains = {row[0]:row[1:] for row in rows[1:-1]}
    return (len(chains) == 3 and chains.get(":INPUT") == ("ACCEPT","[0:0]")
        and chains.get(":OUTPUT") == ("ACCEPT","[0:0]")
        and chains.get(":FORWARD") in {("ACCEPT","[0:0]"),("DROP","[0:0]")})
'''

_NETNS_ENTER_SOURCE = _NETNS_COMMON_SOURCE + r'''
_filter_stage = 'enter'
def main():
    global _filter_stage
    _filter_stage = 'enter'
    request = decode(sys.stdin.buffer.read(8193))
    if (type(request) is not dict or set(request) != {"action","namespace","deadline"}
            or request["action"] not in {"install","verify"} or os.geteuid() != 0
            or type(request["deadline"]) not in {int,float}
            or not 0 < request["deadline"]-time.monotonic() <= 3):
        raise PermissionError("entered helper binding invalid")
    def namespace():
        info = os.stat("/proc/self/ns/net")
        actual = [info.st_dev,info.st_ino]
        if actual != request["namespace"]: raise PermissionError("entered namespace changed")
        return actual
    namespace()
    pairs = [("/usr/sbin/iptables-save","/usr/sbin/iptables-restore",RULES4),
             ("/usr/sbin/ip6tables-save","/usr/sbin/ip6tables-restore",RULES6)]
    if request["action"] == "install":
        # Refuse foreign rules before either family is modified. NAT is never flushed.
        for index,(save, restore, rules) in enumerate(pairs):
            _filter_stage = "precheck4" if index==0 else "precheck6"
            if not empty_filter(run([save,"-t","filter"],request["deadline"])):
                raise PermissionError("unexpected preexisting filter")
        for index,(save, restore, rules) in enumerate(pairs):
            _filter_stage = "restore4" if index==0 else "restore6"
            namespace()
            run([restore,"--noflush","--wait","1"],request["deadline"],rules.encode())
    for index,(save, restore, rules) in enumerate(pairs):
        _filter_stage = "verify4" if index==0 else "verify6"
        namespace()
        if normal(run([save,"-t","filter"],request["deadline"])) != normal(rules.encode()):
            raise PermissionError("effective filter or order differs")
    print(json.dumps({"namespace":namespace(),"rules_sha256":RULE_HASH},separators=(',',':')))
_enter_main = main
def main():
    try:return _enter_main()
    except BaseException as error:
        emit_failure(error)
        raise
'''

_NETNS_ROOT_SOURCE = _NETNS_COMMON_SOURCE + "\nENTER_SOURCE = " + repr(_NETNS_ENTER_SOURCE) + r'''
import http.client, signal, socket
from pathlib import Path
_filter_stage = "input"

def main():
    global _filter_stage
    _filter_stage = "input"
    deadline = time.monotonic()+3
    raw = sys.stdin.buffer.read(8193)
    if len(raw)>8192 or os.geteuid()!=0: raise PermissionError("root filter input invalid")
    request = decode(raw)
    keys = {"action","boot_id","container_id","image_digest","work","nonce","network_id","expected"}
    if type(request) is not dict or set(request)!=keys or request["action"] not in {"install","verify"}:
        raise PermissionError("root filter fields invalid")
    for key, pattern in (("boot_id",r"[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}"),
            ("container_id",r"[0-9a-f]{64}"),("network_id",r"[0-9a-f]{64}"),
            ("image_digest",r"sha256:[0-9a-f]{64}"),("work",r"[0-9a-f]{64}"),("nonce",r"[0-9a-f]{48}")):
        if type(request[key]) is not str or not re.fullmatch(pattern,request[key]):
            raise PermissionError("root filter identity invalid")
    if (request["action"] == "install") != (request["expected"] is None):
        raise PermissionError("filter cannot be reinstalled")
    _filter_stage = "boot"
    if Path('/proc/sys/kernel/random/boot_id').read_text().strip()!=request["boot_id"]:
        raise PermissionError("filter boot changed")
    class Docker(http.client.HTTPConnection):
        def connect(self):
            self.sock = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
            self.sock.settimeout(max(.001,min(.5,deadline-time.monotonic())))
            self.sock.connect('/var/run/docker.sock')
    _filter_stage = "image"
    connection = Docker('docker')
    try:
        connection.request('GET','/v1.53/images/'+request["image_digest"]+'/json')
        response = connection.getresponse()
        body = response.read(65537)
        if response.status!=200 or len(body)>65536: raise PermissionError("filter image unavailable")
        image = decode(body)
    finally: connection.close()
    inherited = image.get("Config",{}).get("Labels")
    if inherited is None: inherited = {}
    if (image.get("Id")!=request["image_digest"] or type(inherited) is not dict
            or any(type(k) is not str or type(v) is not str or k.startswith("curis.") for k,v in inherited.items())):
        raise PermissionError("filter image labels conflict with ownership")
    labels = {**inherited,"curis.reader.work":request["work"],"curis.reader.nonce":request["nonce"]}
    def identity():
        global _filter_stage
        _filter_stage = "container"
        if time.monotonic()>=deadline: raise TimeoutError("filter identity budget expired")
        connection = Docker('docker')
        try:
            connection.request('GET','/v1.53/containers/'+request["container_id"]+'/json')
            response = connection.getresponse()
            body = response.read(65537)
            if response.status!=200 or len(body)>65536: raise PermissionError("filter container unavailable")
            info = decode(body)
        finally: connection.close()
        status,config = info.get("State",{}),info.get("Config",{})
        networks = info.get("NetworkSettings",{}).get("Networks",{})
        if (info.get("Id")!=request["container_id"] or info.get("Image")!=request["image_digest"]
                or config.get("Labels")!=labels
                or config.get("User")!="pwuser" or status.get("Running") is not True
                or status.get("Restarting") is not False or type(status.get("Pid")) is not int or status["Pid"]<=1
                or type(status.get("StartedAt")) is not str or not status["StartedAt"]
                or info.get("HostConfig",{}).get("NetworkMode")!=request["network_id"]
                or len(networks)!=1): raise PermissionError("filter original container mismatch")
        endpoint = next(iter(networks.values()))
        if endpoint.get("NetworkID")!=request["network_id"] or endpoint.get("IPAddress")!="172.30.253.3":
            raise PermissionError("filter original network mismatch")
        _filter_stage = "process"
        pid = status["Pid"]
        fields = Path('/proc/'+str(pid)+'/stat').read_text().rsplit(')',1)[1].split()
        start = int(fields[19])
        uid_line = next(line for line in Path('/proc/'+str(pid)+'/status').read_text().splitlines() if line.startswith('Uid:'))
        if start<=0 or any(int(value)==0 for value in uid_line.split()[1:]):
            raise PermissionError("filter worker process identity invalid")
        return {"pid":pid,"started_at":status["StartedAt"],"kernel_start":start}
    original = identity()
    # Open here, after sudo. Only this held descriptor crosses nsenter.
    _filter_stage = "namespace"
    fd = os.open('/proc/'+str(original["pid"])+ '/ns/net',os.O_RDONLY|os.O_CLOEXEC)
    try:
        held = os.fstat(fd)
        namespace = [held.st_dev,held.st_ino]
        host = os.stat('/proc/self/ns/net')
        current = os.stat('/proc/'+str(original["pid"])+ '/ns/net')
        if (namespace==[host.st_dev,host.st_ino] or namespace!=[current.st_dev,current.st_ino]
                or identity()!=original): raise PermissionError("filter namespace acquisition raced")
        receipt = {key:request[key] for key in ("boot_id","container_id","image_digest","work","nonce","network_id")}
        receipt.update(original,namespace=namespace,rules_sha256=RULE_HASH)
        if request["action"]=="verify" and request["expected"]!=receipt:
            raise PermissionError("filter held generation changed")
        entered = json.dumps({"action":request["action"],"namespace":namespace,"deadline":deadline}).encode()
        _filter_stage = "enter"
        result = decode(run(['/usr/bin/nsenter','--net=/proc/self/fd/'+str(fd),'--',
            '/usr/bin/python3','-I','-S','-B','-c',ENTER_SOURCE+'\nmain()\n'],deadline,entered,(fd,),seconds=3))
        if result!={"namespace":namespace,"rules_sha256":RULE_HASH} or identity()!=original:
            raise PermissionError("filter final generation mismatch")
        _filter_stage = "final"
        current = os.stat('/proc/'+str(original["pid"])+ '/ns/net')
        if namespace!=[current.st_dev,current.st_ino]: raise PermissionError("filter namespace replaced")
        print(json.dumps(receipt,separators=(',',':')))
    finally: os.close(fd)

_root_main = main
def main():
    def expired(signum,frame): raise TimeoutError("privileged filter total deadline expired")
    previous = signal.signal(signal.SIGALRM,expired)
    try:
        signal.setitimer(signal.ITIMER_REAL,3)
        return _root_main()
    except BaseException as error:
        emit_failure(error)
        raise
    finally:
        signal.setitimer(signal.ITIMER_REAL,0)
        signal.signal(signal.SIGALRM,previous)
'''


def _netns_binding(binding):
    import re
    patterns = {"boot_id":r"[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}",
        "container_id":r"[0-9a-f]{64}", "network_id":r"[0-9a-f]{64}",
        "image_digest":r"sha256:[0-9a-f]{64}", "work":r"[0-9a-f]{64}", "nonce":r"[0-9a-f]{48}"}
    if (type(binding) is not dict or set(binding) != set(patterns)
            or any(type(binding[k]) is not str or not re.fullmatch(pattern,binding[k]) for k,pattern in patterns.items())):
        raise PermissionError("Netns filter requires the original fixed generation")
    return binding.copy()


def _netns_receipt(binding, receipt, *, paired=False):
    binding = _netns_binding(binding)
    if (type(receipt) is not dict or set(receipt) != set(binding) | {"pid","started_at","kernel_start","namespace","rules_sha256"}
            or any(receipt[k] != value for k,value in binding.items())
            or type(receipt["pid"]) is not int or receipt["pid"] <= 1
            or type(receipt["kernel_start"]) is not int or receipt["kernel_start"] <= 0
            or type(receipt["started_at"]) is not str or not receipt["started_at"]
            or type(receipt["namespace"]) is not list or len(receipt["namespace"]) != 2
            or any(type(value) is not int or value <= 0 for value in receipt["namespace"])
            or type(paired) is not bool
            or receipt["rules_sha256"] != (_NETNS_PAIRED_FILTER_SHA256 if paired else _NETNS_FILTER_SHA256)):
        raise PermissionError("Netns filter receipt does not prove the original generation")
    return {**receipt,"namespace":receipt["namespace"].copy()}


class _DedicatedDockerSSH:
    """Actual SSH host-key authentication, independent connection for each call.

    Creating this candidate is not runtime release. Missing public enrollment
    fails before any subprocess, ledger creation, VM start or private-key access.
    """
    def browser_filter(self, action, binding, expected=None, *, paired=False):
        import json, os, shlex, sys
        from .agent_browser_runtime import _unique_json_object, _invalid_json_constant, _finite_json_float
        binding = _netns_binding(binding)
        if type(paired) is not bool or action not in {"install","verify"} or (action == "install") != (expected is None):
            raise PermissionError("Netns filter operation is outside fixed scope")
        if expected is not None:
            expected = _netns_receipt(binding,expected,paired=paired)
        payload = json.dumps({**binding,"action":action,"expected":expected},allow_nan=False).encode()
        if len(payload) > 8192: raise ValueError("Netns helper input exceeded bound")
        directory, fds = _owner_directory(), []
        try:
            for name in ("reader-owner-ssh.config",_OWNER_KNOWN_HOSTS):
                fds.append(_owner_file(directory,name,os.O_RDONLY))
            texts = [os.read(fd,65537).decode("ascii") for fd in fds]
            if any(len(value)>65536 for value in texts): raise PermissionError("Owner enrollment exceeded bound")
            _ssh_owner_inputs(*texts)
            for fd in fds: os.lseek(fd,0,os.SEEK_SET)
            argv = _ssh_owner_argv(*fds)
            # sudo receives no namespace descriptor. The fixed privileged source opens it itself.
            source = _NETNS_ROOT_SOURCE.replace("172.30.253.", "172.30.251.") if paired else _NETNS_ROOT_SOURCE
            argv[-1] = "/usr/bin/sudo -n /usr/bin/python3 -I -S -B -c " + shlex.quote(source+"\nmain()\n")
            raw = _bounded_ssh_exchange(argv,tuple(fds),payload,5)
            if len(raw)>65536: raise ValueError("Netns helper response exceeded bound")
            receipt = _netns_receipt(binding,json.loads(raw,object_pairs_hook=_unique_json_object,
                parse_constant=_invalid_json_constant,parse_float=_finite_json_float),paired=paired)
            if expected is not None and receipt != expected:
                raise PermissionError("Netns filter changed after installation")
            return receipt
        finally:
            pending, errors = sys.exception(), []
            for fd in [*fds,directory]:
                try: os.close(fd)
                except BaseException as error: errors.append(error)
            if errors:
                interrupt = next((error for error in errors if not isinstance(error,Exception)),None)
                if pending is not None and not isinstance(pending,Exception):
                    pending.add_note("Owner filter input close failed; resources remain UNKNOWN")
                elif interrupt is not None:
                    raise interrupt
                elif pending is not None:
                    pending.add_note("Owner filter input close failed; resources remain UNKNOWN")
                else:
                    raise errors[0]

    def request(self, method, path, *, boot_id=None, body=None, seconds=5):
        import json, os, re
        from .agent_browser_runtime import _unique_json_object, _invalid_json_constant, _finite_json_float
        allowed = ((method == "GET" and (path == "/version" or re.fullmatch(r"/containers/[0-9a-f]{64}/json|/images/sha256:[0-9a-f]{64}/json|/networks/[0-9a-f]{64}", path)))
            or (method == "POST" and (path in {"/containers/create", "/networks/create"} or re.fullmatch(r"/containers/[0-9a-f]{64}/(?:start|stop\?t=1|kill\?signal=SIGKILL)", path)))
            or (method == "POST" and re.fullmatch(r"/networks/[0-9a-f]{64}/disconnect", path)
                and type(body) is dict and set(body) == {"Container", "Force"}
                and re.fullmatch(r"[0-9a-f]{64}", str(body["Container"])) and body["Force"] is True)
            or (method == "DELETE" and re.fullmatch(r"/networks/[0-9a-f]{64}", path) and body is None))
        if not allowed or (method != "GET" and not boot_id):
            raise PermissionError("Docker operation is outside owned scope")
        payload = json.dumps({"method":method,"path":path,"boot_id":boot_id,"body":body}, allow_nan=False).encode()
        if len(payload) > 65536:
            raise ValueError("Docker request oversized")
        directory, fds = _owner_directory(), []
        try:
            for name in ("reader-owner-ssh.config", _OWNER_KNOWN_HOSTS):
                fds.append(_owner_file(directory, name, os.O_RDONLY))
            texts = [os.read(fd, 65537).decode("ascii") for fd in fds]
            if any(len(text)>65536 for text in texts):
                raise PermissionError("Owner SSH inputs oversized")
            _ssh_owner_inputs(*texts)
            for fd in fds:
                os.lseek(fd, 0, os.SEEK_SET)
            raw = _bounded_ssh_exchange(_ssh_owner_argv(*fds), tuple(fds), payload, seconds)
            value = json.loads(raw, object_pairs_hook=_unique_json_object, parse_constant=_invalid_json_constant, parse_float=_finite_json_float)
            if (type(value) is not dict or set(value) != {"boot_id","status","body"}
                    or not re.fullmatch(r"[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}", str(value["boot_id"]))
                    or (boot_id is not None and value["boot_id"] != boot_id) or type(value["status"]) is not int
                    or not (200 <= value["status"] < 300
                            or (value["status"] == 304 and method == "POST" and path.endswith("/stop?t=1"))
                            or (value["status"] == 404 and method == "GET"
                                and re.fullmatch(r"/networks/[0-9a-f]{64}", path)))):
                raise PermissionError("Authenticated Docker response rejected; outcome UNKNOWN")
            return value
        finally:
            for fd in fds:
                os.close(fd)
            os.close(directory)


def _owner_records(raw):
    import json
    from .agent_browser_runtime import _unique_json_object
    if len(raw)>1048576 or (raw and not raw.endswith(b"\n")):
        raise PermissionError("Owner ledger incomplete; retain UNKNOWN")
    records = []
    for line in raw.splitlines():
        row = json.loads(line, object_pairs_hook=_unique_json_object)
        if type(row) is not dict or row.get("state") not in {"INTENT", "NETWORK", "PROXY_CREATED", "CREATED", "START_INTENT", "NETNS_FILTER_INTENT", "NETNS_FILTER_VERIFIED", "ATTACHED", "REVOKING", "STOP_RETURNED", "NETWORK_RETIRE_INTENT", "NETWORKS_RETIRED", "UNSTARTED_RECOVERY_INTENT", "STOPPED_RECOVERY_INTENT", "RETIREMENT_RECOVERY_INTENT", "AGENT_REVOKED_RECOVERY_INTENT", "CLOSED_VERIFIED", "BOOT_CLOSURES_VERIFIED"}:
            raise PermissionError("Owner ledger unrecognized; retain UNKNOWN")
        records.append(row)
    return records


class _OwnerJournal:
    """Exclusive, append-only unresolved ownership; no automatic reset or reuse."""
    def __init__(self, *, _held_lock=None):
        import fcntl, os
        self.directory, self.lock_fd, self.ledger_fd = _owner_directory(), None, None
        self.poisoned = False
        self.peer = None
        self._write_lock = threading.Lock()
        try:
            if _held_lock is None:
                self.lock_fd = _owner_file(self.directory, "reader-owner.lock", os.O_RDWR | os.O_CREAT)
                fcntl.flock(self.lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                name = "reader-owner-ledger.jsonl"
            else:
                if (not isinstance(_held_lock, _OwnerJournalBase) or type(_held_lock.lock_fd) is not int
                        or _held_lock.ledger_fd is None or _held_lock.poisoned):
                    raise PermissionError("Agent journal requires the original held global lease")
                name = "reader-owner-agent-ledger.jsonl"
            # Missing child history requires explicit installation/recovery, never an empty reset.
            flags = os.O_RDWR | os.O_APPEND
            self.ledger_fd = _owner_file(self.directory, name, flags)
            self.records = _owner_records(os.read(self.ledger_fd, 1048577))
            if _held_lock is None:
                self.peer = _OwnerJournalBase(_held_lock=self)
            os.fsync(self.directory)
        except BaseException:
            self.close()
            raise

    def append(self, record):
        with self._write_lock:
            return self._append(record)

    def _append(self, record):
        import json, os
        if self.poisoned or self.ledger_fd is None:
            raise PermissionError("Owner ledger is unavailable; retain UNKNOWN")
        raw = (json.dumps(record, sort_keys=True, separators=(",", ":"), allow_nan=False)+"\n").encode()
        _owner_records(raw)
        if os.fstat(self.ledger_fd).st_size + len(raw)>1048576:
            raise PermissionError("Owner ledger full; retain UNKNOWN")
        self.poisoned = True
        # One append; partial writes are retained and forbid subsequent mutation.
        if os.write(self.ledger_fd, raw) != len(raw):
            raise OSError("Owner ledger partial write; retain UNKNOWN")
        os.fsync(self.ledger_fd)
        self.records.append(json.loads(raw))
        self.poisoned = False

    def close(self):
        import os
        errors = []
        if getattr(self, "peer", None) is not None:
            try: self.peer.close()
            except BaseException as error: errors.append(error)
            self.peer = None
        for name in ("ledger_fd", "lock_fd", "directory"):
            fd = getattr(self, name, None)
            if fd is not None:
                setattr(self, name, None)
                try:
                    os.close(fd)
                except BaseException as error:
                    errors.append(error)
        if errors:
            # Finish all close attempts, then preserve the first interruption.
            raise next((error for error in errors if not isinstance(error, Exception)), errors[0])


_OwnerJournalBase = _OwnerJournal


class _WorkJournalView:
    def __init__(self, journal):
        self._journal, self.closed = journal, False

    def __getattr__(self, name):
        return getattr(self._journal, name)

    def append(self, row):
        if self.closed: raise PermissionError("Original child journal is closed")
        return self._journal.append(row)

    def close(self):
        self.closed = True  # The parent retains the one physical global lease.


class _OriginalWorkOwners:
    """One server-created attempt; children never join by a Work string."""
    def __init__(self, identity):
        import secrets
        keys = {"tenant_id", "company_id", "work_ref", "task_id", "employee_id", "binding_ref"}
        if type(identity) is not dict or set(identity) != keys or any(type(v) is not str or not v for v in identity.values()):
            raise PermissionError("Complete original Work identity required")
        self.identity, self.attempt = identity.copy(), secrets.token_hex(24)
        self.owners, self.revokers = {}, {}
        self.journal, self.boot_id, self._token = None, None, None
        self.receipt = None
        self._lock, self.closed, self._preflight = threading.RLock(), False, False

    def __enter__(self):
        if self.closed or self._token is not None or _WORK_OWNER_SCOPE.get() is not None:
            raise PermissionError("Original Work scope cannot be nested or reused")
        self._token = _WORK_OWNER_SCOPE.set(self)
        return self

    def __exit__(self, kind, error, traceback):
        try:
            self.close()
        except BaseException:
            if error is None: raise
            error.add_note("Original Work child closure UNKNOWN; no retry or reuse")
        finally:
            _WORK_OWNER_SCOPE.reset(self._token)

    def bind(self, owner, role):
        with self._lock:
            if (self.closed or _WORK_OWNER_SCOPE.get() is not self or role not in {"reader", "agent"}
                    or role in self.owners or type(owner) is not _DedicatedDockerOwner
                    or owner.identity != self.identity or owner.nonce is not None):
                raise PermissionError("Original Work child scope changed")
            self.owners[role] = owner
            owner._work_parent, owner._work_role = self, role
            owner._paired_provider = role == "agent"

    def borrow(self, owner):
        with self._lock:
            role = getattr(owner, "_work_role", None)
            if self.closed or self.owners.get(role) is not owner or owner.identity != self.identity:
                raise PermissionError("Original Work lease is unavailable")
            if self.boot_id is not None and owner.boot_id != self.boot_id:
                raise PermissionError("Original Work boot changed")
            if self.journal is None:
                self.journal = _OwnerJournal()
                self.boot_id = owner.boot_id
            return _WorkJournalView(self.journal if role == "reader" else self.journal.peer)

    def preflight(self, image_digest):
        import json
        with self._lock:
            if self.closed or self.journal is not None or _WORK_OWNER_SCOPE.get() is not self:
                raise PermissionError("Original Work preflight cannot be reused")
            audit=_DedicatedDockerOwner(self.identity,image_digest)
            version=audit.connection.request("GET","/version")
            if version["body"].get("Os")!="linux" or version["body"].get("Arch")!="arm64" or version["body"].get("Version")!="29.5.2":
                raise PermissionError("Original Work daemon changed")
            audit.boot_id=version["boot_id"]
            image=audit.connection.request("GET","/images/"+image_digest+"/json",boot_id=audit.boot_id)["body"]
            _verified_image_labels(image,image_digest)
            self.journal,self.boot_id=_OwnerJournal(),audit.boot_id
            self._audit_histories(audit,None)
            work=hashlib.sha256(json.dumps(self.identity,sort_keys=True,separators=(',',':')).encode()).hexdigest()
            if any(row.get("work")==work for journal in (self.journal,self.journal.peer) for row in journal.records):
                raise PermissionError("Original Work attempt cannot be replayed")

    def _audit_histories(self, owner, nonce):
        for journal in (self.journal, self.journal.peer):
            audit=_DedicatedDockerOwner(self.identity,owner.image_digest)
            audit.boot_id,audit.journal=self.boot_id,journal
            audit._verify_prior_holds(nonce)
        self._preflight=True

    def can_reseed(self):
        with self._lock:
            return not self.closed and self._preflight and self.journal is not None and not self.owners

    def verify_prior(self, owner, nonce):
        with self._lock:
            if self.closed or self.owners.get(owner._work_role) is not owner or owner.boot_id != self.boot_id:
                raise PermissionError("Original Work preparation revoked")
            if not self._preflight:
                self._audit_histories(owner,nonce)
            if any(row.get("nonce")==nonce for journal in (self.journal,self.journal.peer) for row in journal.records):
                raise PermissionError("Original child nonce was already used")
            owner._verify_prior_holds(nonce)
            for sibling in self.owners.values():
                if sibling is owner or sibling.nonce is None: continue
                if sibling.nonce == nonce or sibling.boot_id != self.boot_id or sibling.identity != self.identity:
                    raise PermissionError("Original sibling generation changed")
                if sibling.stop_requested:
                    if not sibling._stop_done.is_set() or not sibling.stop_receipt or sibling.stop_receipt.get("ledger_state") != "CLOSED_VERIFIED":
                        raise PermissionError("Original sibling closure UNKNOWN")
                else:
                    groups = sibling._history_groups()
                    if not groups or groups[-1]["base"] != sibling._record or groups[-1]["state"] != "ATTACHED":
                        raise PermissionError("Original sibling is not a verified live generation")
                    sibling._topology()
                    info = sibling._inspect()
                    if info["State"].get("Running") is not True or info["State"].get("Pid", 0) <= 0:
                        raise PermissionError("Original sibling stopped or changed")

    def close(self, *, retain_lease=False):
        with self._lock:
            if self.closed:
                if not retain_lease and self.receipt is not None and self.journal is not None:
                    self.journal.close()
                return
            self.closed = True
            owners = list(reversed(list(self.owners.values())))
        errors = []
        for revoke in self.revokers.values():
            try: revoke()
            except BaseException as error: errors.append(error)
        for owner in owners:
            owner._revoked_event.set()
            try:
                with owner._state_lock:
                    owner.revoked = True
                    cid = owner.container_id
                if owner.stop_requested:
                    if not owner._stop_done.wait(6) or not owner.stop_receipt or owner.stop_receipt.get("ledger_state") != "CLOSED_VERIFIED":
                        raise PermissionError("Original child closure UNKNOWN")
                elif cid or owner.proxy_id:
                    owner.revoke_bound_and_stop(owner.identity.copy(), owner.nonce, {
                        "complete": False, "executionAuthorized": False, "boot_id": owner.boot_id,
                        "container_id": cid, "image_digest": owner.image_digest})
                elif owner.journal and any(row.get("nonce") == owner.nonce and row.get("state") == "INTENT" for row in owner.journal.records):
                    raise PermissionError("Original child allocation UNKNOWN")
            except BaseException as error: errors.append(error)
        if errors:
            _UNRESOLVED_WORK_OWNERS.append(self)
            raise RuntimeError("Original Work closure UNKNOWN; lease retained") from errors[0]
        self.receipt = {"identity": self.identity.copy(), "parent_attempt": self.attempt,
            "boot_id": self.boot_id, "ledger_state": "CLOSED_VERIFIED",
            "children": [dict(owner.stop_receipt) for owner in owners if owner.stop_receipt is not None]}
        if not retain_lease and self.journal is not None: self.journal.close()


def original_work_owners(identity):
    return _OriginalWorkOwners(identity)


def _verified_image_labels(image, digest):
    if type(image) is not dict or image.get("Id") != digest:
        raise PermissionError("Inherited label image identity changed")
    labels = image.get("Config", {}).get("Labels")
    if labels is None: labels = {}
    if (type(labels) is not dict or any(type(k) is not str or type(v) is not str
            or k.startswith("curis.") for k,v in labels.items())):
        raise PermissionError("Image labels conflict with Curis ownership")
    return labels.copy()


def _never_started_container(info):
    state = info.get("State", {})
    return (state.get("Status") == "created" and state.get("Running") is False
        and state.get("Restarting") is False and state.get("Dead") is False
        and type(state.get("Pid")) is int and state["Pid"] == 0
        and type(state.get("ExitCode")) is int and state["ExitCode"] == 0
        and state.get("StartedAt") == "0001-01-01T00:00:00Z"
        and state.get("FinishedAt") == "0001-01-01T00:00:00Z")


def _empty_created_endpoint(info, endpoint, address):
    return (_never_started_container(info) and type(endpoint) is dict
        and all(endpoint.get(k) == "" for k in ("NetworkID", "EndpointID", "IPAddress",
            "Gateway", "IPv6Gateway", "GlobalIPv6Address"))
        and endpoint.get("IPAMConfig", {}).get("IPv4Address") == address)


def _stopped_container(info):
    state = info.get("State", {})
    return (state.get("Status") == "exited" and state.get("Running") is False
        and state.get("Restarting") is False and state.get("Dead") is False
        and type(state.get("Pid")) is int and state["Pid"] == 0
        and type(state.get("ExitCode")) is int
        and all(type(state.get(k)) is str and 0 < len(state[k]) <= 64
            and state[k] != "0001-01-01T00:00:00Z" for k in ("StartedAt","FinishedAt")))


def _stopped_agent_networks(networks):
    """Docker retains its inert built-in none entry after an isolated exit."""
    import re
    if type(networks) is not dict:return False
    if not networks:return True
    if set(networks) != {"none"} or type(networks["none"]) is not dict:return False
    endpoint = networks["none"]
    nulls = {"IPAMConfig","Links","Aliases","DriverOpts","DNSNames"}
    empty = {"EndpointID","Gateway","IPAddress","MacAddress","IPv6Gateway","GlobalIPv6Address"}
    zeros = {"GwPriority","IPPrefixLen","GlobalIPv6PrefixLen"}
    return (set(endpoint) == nulls | empty | zeros | {"NetworkID"}
        and all(endpoint[k] is None for k in nulls)
        and all(endpoint[k] == "" for k in empty)
        and all(type(endpoint[k]) is int and endpoint[k] == 0 for k in zeros)
        and type(endpoint["NetworkID"]) is str and re.fullmatch(r"[0-9a-f]{64}",endpoint["NetworkID"]) is not None)


class _HistoryBootChanged(PermissionError):
    pass


_AGENT_CONTAINER_IMAGE = "sha256:b74e2077c6af9c43fd90f936069d3b8040b1abde8513117222c337af9aeb4bfb"
_AGENT_CONTAINER_SOURCE = r'''
import hashlib,json,os,re,select,signal,socket,subprocess,sys,time
from pathlib import Path
assert sys.argv[1:]==['--curis-agent-container']
def read_frame(seconds):
    data=bytearray();deadline=time.monotonic()+seconds
    while b'\n' not in data:
        remaining=deadline-time.monotonic()
        if remaining<=0 or not select.select([sys.stdin],[],[],remaining)[0]:raise TimeoutError('channel timeout')
        part=os.read(sys.stdin.fileno(),65536-len(data))
        if not part:raise EOFError('channel closed')
        data.extend(part)
        if len(data)>=65536:raise ValueError('frame bound')
    line,tail=bytes(data).split(b'\n',1)
    if tail:raise ValueError('unexpected pipelined frame')
    return json.loads(line)
def bound(frame,sequence,action):
    assert set(frame)=={'identity','nonce','boot_id','container_id','image_digest','sequence','action','arguments'}
    assert frame['sequence']==sequence and type(frame['sequence']) is int and frame['action']==action
    identity=frame['identity']
    assert type(identity) is dict and set(identity)=={'tenant_id','company_id','work_ref','task_id','employee_id','binding_ref'}
    assert all(type(v) is str and v for v in identity.values())
    assert hashlib.sha256(json.dumps(identity,sort_keys=True,separators=(',',':')).encode()).hexdigest()==os.environ['CURIS_AGENT_CONTAINER_WORK']
    assert frame['nonce']==os.environ['CURIS_AGENT_CONTAINER_NONCE']
    assert frame['image_digest']==os.environ['CURIS_AGENT_CONTAINER_IMAGE']
    assert frame['boot_id']==Path('/proc/sys/kernel/random/boot_id').read_text().strip()
    assert re.fullmatch('[0-9a-f]{64}',frame['container_id']) and socket.gethostname()==frame['container_id'][:12]
    return {k:frame[k] for k in ('identity','nonce','boot_id','container_id','image_digest','sequence')}
def emit(binding,result):
    print(json.dumps({**binding,'result':result},separators=(',',':')),flush=True)
def stopped(_number,_frame):raise SystemExit(130)
signal.signal(signal.SIGTERM,stopped);signal.signal(signal.SIGINT,stopped)
first=read_frame(5);binding=bound(first,0,'bootstrap');assert first['arguments']=={}
emit(binding,{'ready':True,'network':'none','credentials':False})
frame=read_frame(5);binding=bound(frame,1,'execute');args=frame['arguments']
assert set(args)=={'command','input','timeout'}
command=args['command']
assert type(command) is list and len(command)==5 and command[:4]==['/usr/bin/python3','-I','-B','-c']
assert all(type(x) is str and '\0' not in x for x in command) and len(command[4].encode())<=16384
assert type(args['input']) is str and len(args['input'].encode())<=32768
assert type(args['timeout']) in (int,float) and 0<args['timeout']<=80
child=None;out=bytearray();err=bytearray();reason='completed'
try:
    child=subprocess.Popen(command,cwd='/tmp',env={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8'},
        stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True,close_fds=True)
    for pipe in (child.stdin,child.stdout,child.stderr):os.set_blocking(pipe.fileno(),False)
    pending=memoryview(args['input'].encode());deadline=time.monotonic()+args['timeout']
    streams={child.stdout:out,child.stderr:err}
    while True:
        if time.monotonic()>=deadline:reason='timeout';break
        if not pending and not child.stdin.closed:child.stdin.close()
        readable,writable,_=select.select([sys.stdin,*streams],
            [child.stdin] if pending else [],[],min(.02,max(0,deadline-time.monotonic())))
        if sys.stdin in readable:reason='eof';break
        if child.stdin in writable:
            try:pending=pending[os.write(child.stdin.fileno(),pending[:4096]):]
            except BrokenPipeError:pending=memoryview(b'')
        for pipe,target in list(streams.items()):
            if pipe in readable:
                data=os.read(pipe.fileno(),8193);target.extend(data)
                if len(out)+len(err)>8192:raise ValueError('output bound')
                if not data:del streams[pipe];pipe.close()
        if child.poll() is not None and not streams:break
    if reason=='completed':
        emit(binding,{'reason':reason,'returncode':child.returncode,
            'stdout':out.decode('utf-8',errors='replace'),'stderr':err.decode('utf-8',errors='replace')})
        # Keep PID1 alive until the owner revokes and stops this exact namespace.
        try:read_frame(5)
        except (EOFError,TimeoutError):pass
    else:emit(binding,{'reason':reason})
finally:
    if child is not None and child.poll() is None:
        child.terminate()
        try:child.wait(timeout=.2)
        except subprocess.TimeoutExpired:child.kill();child.wait(timeout=.2)
'''


_AGENT_MCP_STDIO_SOURCE = r'''
import json,os,select,socket,sys,time
def bridge_main():
    peer=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
    peer.settimeout(80)
    peer.connect('/tmp/curis-agent-work/owner-mcp.sock')
    pending=bytearray();deadline=time.monotonic()+80
    try:
        while time.monotonic()<deadline:
            if not select.select([sys.stdin],[],[],min(.05,max(0,deadline-time.monotonic())))[0]:continue
            data=os.read(sys.stdin.fileno(),32769)
            if not data:return
            pending.extend(data)
            if len(pending)>32768:raise ValueError('MCP input bound')
            while b'\n' in pending:
                line,tail=bytes(pending).split(b'\n',1);pending=bytearray(tail)
                request=json.loads(line)
                if type(request) is not dict:raise ValueError('MCP object required')
                peer.sendall(line+b'\n');response=bytearray()
                while b'\n' not in response:
                    peer.settimeout(max(.001,deadline-time.monotonic()))
                    part=peer.recv(60001-len(response))
                    if not part:raise EOFError('MCP owner closed')
                    response.extend(part)
                    if len(response)>60000:raise ValueError('MCP reply bound')
                reply,extra=bytes(response).split(b'\n',1)
                if extra:raise ValueError('MCP extra owner reply')
                value=json.loads(reply)
                if value is not None:
                    if type(value) is not dict:raise ValueError('MCP reply object required')
                    print(json.dumps(value,separators=(',',':')),flush=True)
    finally:peer.close()
bridge_main()
'''


_AGENT_CODEX_SOURCE = _AGENT_CONTAINER_SOURCE.split('first=read_frame(5)',1)[0] + r'''
import stat,struct
WORK='/tmp/curis-agent-work'
HOME='/tmp/curis-agent-home'
BINARY='/opt/curis/bin/codex'
BINARY_SHA='57a159f67999794494a172e71c12c6b5a211542ea90c66ea2ce9e6ac1edec6b1'
BRIDGE=__CURIS_STDIO_SOURCE__
def codex_argv():
    settings={
        'history.persistence':'none','project_doc_max_bytes':0,
        'skills.include_instructions':False,'skills.bundled.enabled':False,
        'features.plugins':False,'features.apps':False,'features.memories':False,
        'features.shell_tool':False,'features.shell_snapshot':False,
        'features.image_generation':False,'features.apply_patch_freeform':False,
        'features.multi_agent':False,'features.multi_agent_v2':False,'features.hooks':False,
        'tools.experimental_request_user_input.enabled':False,
        'features.skill_mcp_dependency_install':False,'web_search':'disabled',
        'model_catalog_json':WORK+'/model-catalog.json','sqlite_home':WORK,
        'cli_auth_credentials_store':'file',
    }
    command=[BINARY,'exec','--ignore-user-config','--ephemeral','--json',
             '--sandbox','read-only','--cd',WORK,'--skip-git-repo-check',
             '--model','gpt-5.6-sol','--strict-config','--ignore-rules']
    for key,value in settings.items():command.extend(['-c',key+'='+json.dumps(value,separators=(',',':'))])
    mcp='mcp_servers={curis={command="/usr/bin/python3",args='+json.dumps(['-I','-B','-c',BRIDGE])+',required=true,startup_timeout_sec=10,tool_timeout_sec=15}}'
    command.extend(['-c',mcp])
    for name in ('read_skill','write_output','browser'):
        command.extend(['-c','mcp_servers.curis.tools.'+name+'.approval_mode="approve"'])
    return command+['-']
def read_owned_auth_cache():
    path=HOME+'/.codex/auth.json'
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    try:
        info=os.fstat(fd)
        assert stat.S_ISREG(info.st_mode) and info.st_uid==1001 and info.st_nlink==1
        assert stat.S_IMODE(info.st_mode)==0o600 and 0<info.st_size<=32768
        raw=os.read(fd,32769);assert 0<len(raw)<=32768
    finally:os.close(fd)
    return raw.decode('utf-8')
def return_owned_auth(binding,result,deadline,*,logged_out=False):
    if not MANAGED_AUTH:return binding,result
    cache=None if logged_out else read_owned_auth_cache()
    result=dict(result)
    for raw in (PREVIOUS_AUTH_CACHE,cache):
        if raw is None:continue
        tokens=json.loads(raw).get('tokens',{})
        for secret in tokens.values():
            if type(secret) is str and secret:
                for key in ('stdout','stderr'):
                    result[key]=result[key].replace(secret,'[REDACTED]').replace(json.dumps(secret)[1:-1],'[REDACTED]')
    payload={'auth_writeback':{'cache':cache,'authenticated':not logged_out}}
    assert len(json.dumps(payload).encode())<=60000
    if time.monotonic()>=deadline:raise TimeoutError('original authentication writeback deadline')
    emit(binding,payload)
    remaining=deadline-time.monotonic()
    if remaining<=0:raise TimeoutError('original authentication writeback deadline')
    frame=read_frame(remaining);binding=bound(frame,binding['sequence']+1,'auth_saved')
    assert set(frame['arguments'])=={'accepted'} and frame['arguments']['accepted'] is True
    if time.monotonic()>=deadline:raise TimeoutError('original authentication writeback deadline')
    return binding,result
def run_codex(frame,binding,args,environment):
    listener=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
    peer=None;child=None;out=bytearray();err=bytearray();request_buffer=bytearray()
    deadline=time.monotonic()+args['timeout'];sequence=frame['sequence'];tool_sequence=0;peer_seen=False
    try:
        listener.bind(WORK+'/owner-mcp.sock');os.chmod(WORK+'/owner-mcp.sock',0o600)
        listener.listen(1);listener.setblocking(False)
        child=subprocess.Popen(codex_argv(),cwd=WORK,env=environment,stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True,close_fds=True)
        for stream in (child.stdin,child.stdout,child.stderr):os.set_blocking(stream.fileno(),False)
        pending=memoryview(args['input'].encode());streams={child.stdout:out,child.stderr:err}
        while True:
            remaining=deadline-time.monotonic()
            if remaining<=0:raise TimeoutError('original Codex deadline')
            if not pending and not child.stdin.closed:child.stdin.close()
            readers=[sys.stdin,*streams,*([peer] if peer is not None else [] if peer_seen else [listener])]
            readable,writable,_=select.select(readers,[child.stdin] if pending else [],[],min(.02,remaining))
            if sys.stdin in readable:raise EOFError('original owner revoked')
            if listener in readable:
                peer,_=listener.accept();peer_seen=True
                credentials=peer.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,12)
                if struct.unpack('3i',credentials)[1]!=os.geteuid():raise PermissionError('foreign MCP peer')
                peer.setblocking(False)
            if child.stdin in writable:
                try:pending=pending[os.write(child.stdin.fileno(),pending[:4096]):]
                except BrokenPipeError:pending=memoryview(b'')
            for stream,target in list(streams.items()):
                if stream in readable:
                    data=os.read(stream.fileno(),8193);target.extend(data)
                    if len(out)+len(err)>8192:raise ValueError('Codex output bound')
                    if not data:del streams[stream];stream.close()
            if peer is not None and peer in readable:
                data=peer.recv(32769)
                if not data:
                    if request_buffer:raise EOFError('incomplete MCP peer request')
                    peer.close();peer=None
                    continue
                request_buffer.extend(data)
                if len(request_buffer)>32768:raise ValueError('MCP request bound')
                if b'\n' in request_buffer:
                    line,tail=bytes(request_buffer).split(b'\n',1)
                    if tail:raise ValueError('MCP pipelined peer request')
                    request_buffer.clear();request=json.loads(line);tool_sequence+=1
                    if tool_sequence>200:raise ValueError('MCP request count')
                    tool={k:binding[k] for k in ('identity','nonce','boot_id','container_id','image_digest')}
                    emit(binding,{'tool_request':{**tool,'sequence':tool_sequence,'request':request}})
                    sequence+=1;reply=read_frame(max(.001,deadline-time.monotonic()))
                    binding=bound(reply,sequence,'tool_response');value=reply['arguments']
                    if (type(value) is not dict or set(value)!={*tool,'sequence','response'}
                            or any(value[k]!=v for k,v in tool.items())
                            or type(value['sequence']) is not int or value['sequence']!=tool_sequence):
                        raise PermissionError('MCP original response changed')
                    data=(json.dumps(value['response'],separators=(',',':'),allow_nan=False)+'\n').encode()
                    if len(data)>60000:raise ValueError('MCP reply bound')
                    peer.setblocking(True);peer.settimeout(max(.001,deadline-time.monotonic()));peer.sendall(data);peer.setblocking(False)
            if child.poll() is not None and not streams:
                return binding,{'reason':'completed','returncode':child.returncode,
                    'stdout':out.decode('utf-8',errors='replace'),'stderr':err.decode('utf-8',errors='replace')}
    finally:
        if peer is not None:peer.close()
        listener.close()
        if child is not None and child.poll() is None:
            child.terminate()
            try:child.wait(timeout=.2)
            except subprocess.TimeoutExpired:child.kill();child.wait(timeout=.2)
        if child is not None:
            for stream in (child.stdin,child.stdout,child.stderr):
                if not stream.closed:stream.close()
def authenticate_device(frame,binding,args,environment):
    assert set(args)=={'timeout'} and type(args['timeout']) in (int,float) and 0<args['timeout']<=80
    deadline=time.monotonic()+args['timeout'];child=None;output=bytearray();open_output=True;sent=False
    try:
        child=subprocess.Popen([BINARY,'-c','cli_auth_credentials_store="file"','login','--device-auth'],cwd=WORK,env=environment,
            stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,start_new_session=True,close_fds=True)
        os.set_blocking(child.stdout.fileno(),False)
        while True:
            remaining=deadline-time.monotonic()
            if remaining<=0:raise TimeoutError('original login deadline')
            readable,_,_=select.select([sys.stdin,*([child.stdout] if open_output else [])],[],[],min(.05,remaining))
            if sys.stdin in readable:raise EOFError('login owner revoked')
            if child.stdout in readable:
                part=os.read(child.stdout.fileno(),8193);output.extend(part)
                if len(output)>8192:raise ValueError('login output bound')
                if not part:open_output=False;child.stdout.close()
                if not sent:
                    clean=re.sub(r'\x1b\[[0-9;]*m','',output.decode('utf-8',errors='strict'))
                    codes=re.findall(r'(?m)^\s*([A-Z0-9]{4}-[A-Z0-9]{4})\s*$',clean)
                    if 'https://auth.openai.com/codex/device' in clean and len(codes)==1:
                        emit(binding,{'device_login':{'verification_url':'https://auth.openai.com/codex/device','user_code':codes[0]}})
                        reply=read_frame(max(.001,deadline-time.monotonic()))
                        binding=bound(reply,frame['sequence']+1,'login_ack')
                        if type(reply['arguments']) is not dict or set(reply['arguments'])!={'continue'} or type(reply['arguments']['continue']) is not bool:
                            raise PermissionError('login approval changed')
                        if not reply['arguments']['continue']:return binding,False
                        sent=True;output.clear()
            if child.poll() is not None and not open_output:
                if not sent or child.returncode!=0:return binding,False
                status=subprocess.run([BINARY,'-c','cli_auth_credentials_store="file"','login','status'],cwd=WORK,env=environment,
                    stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,
                    timeout=min(2,max(.001,deadline-time.monotonic())),check=False)
                return binding,status.returncode==0
    finally:
        if child is not None:
            if child.poll() is None:
                child.terminate()
                try:child.wait(timeout=.2)
                except subprocess.TimeoutExpired:child.kill();child.wait(timeout=.2)
            if not child.stdout.closed:child.stdout.close()

first=read_frame(5);binding=bound(first,0,'bootstrap')
args=first['arguments']
assert type(args) is dict and set(args) in ({'resources','catalog'},{'resources','catalog','auth_cache','auth_mode'})
MANAGED_AUTH='auth_cache' in args
AUTH_MODE=args.get('auth_mode')
PREVIOUS_AUTH_CACHE=args.get('auth_cache')
if MANAGED_AUTH:
    assert AUTH_MODE in {'login','use','status','disconnect'}
    if AUTH_MODE=='login':assert PREVIOUS_AUTH_CACHE is None
    else:assert type(PREVIOUS_AUTH_CACHE) is str
resources=args['resources'];raw=json.dumps(resources['resources'],sort_keys=True,separators=(',',':'),allow_nan=False).encode()
assert len(raw)<=32768 and hashlib.sha256(raw).hexdigest()==resources['sha256']
assert resources['resources']['identity']=={k:binding['identity'][k] for k in ('tenant_id','company_id','work_ref','task_id')}
for path in (WORK,HOME):os.mkdir(path,0o700)
if MANAGED_AUTH:
    os.umask(0o077);os.mkdir(HOME+'/.codex',0o700)
    if PREVIOUS_AUTH_CACHE is not None:
        assert 0<len(PREVIOUS_AUTH_CACHE.encode())<=32768
        cached=json.loads(PREVIOUS_AUTH_CACHE)
        assert type(cached) is dict and cached.get('auth_mode')=='chatgpt' and not cached.get('OPENAI_API_KEY')
        fd=os.open(HOME+'/.codex/auth.json',os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
        try:
            raw=PREVIOUS_AUTH_CACHE.encode();assert os.write(fd,raw)==len(raw);os.fsync(fd)
        finally:os.close(fd)
environment={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','HOME':HOME,'CODEX_HOME':HOME+'/.codex','TMPDIR':WORK,
    'NO_PROXY':''}
proxy_address='http://172.30.251.2:8443' if os.environ.get('CURIS_AGENT_PAIRED_NETWORK')=='1' else 'http://172.30.253.2:8443'
environment.update({key:proxy_address for key in ('HTTP_PROXY','HTTPS_PROXY','ALL_PROXY')})
info=os.stat(BINARY,follow_symlinks=False)
assert stat.S_ISREG(info.st_mode) and info.st_uid==0 and not info.st_mode&0o022
with open(BINARY,'rb') as binary:assert hashlib.file_digest(binary,'sha256').hexdigest()==BINARY_SHA
catalog=json.dumps(args['catalog'],sort_keys=True,separators=(',',':'),allow_nan=False).encode()
assert len(catalog)<=32768
fd=os.open(WORK+'/model-catalog.json',os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o400)
try:assert os.write(fd,catalog)==len(catalog)
finally:os.close(fd)
status=subprocess.run([BINARY,'-c','cli_auth_credentials_store="file"','login','status'],env=environment,cwd=WORK,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=2,check=False)
emit(binding,{'ready':True,'resource_sha256':resources['sha256'],'binary_sha256':BINARY_SHA,'authenticated':status.returncode==0})
frame=read_frame(5);execution_sequence=1
if frame.get('action')=='authenticate':
    binding=bound(frame,1,'authenticate')
    assert status.returncode!=0
    binding,authenticated=authenticate_device(frame,binding,frame['arguments'],environment)
    emit(binding,{'authenticated':authenticated})
    if not authenticated:
        try:read_frame(5)
        except (EOFError,TimeoutError):pass
        raise SystemExit(0)
    status.returncode=0;execution_sequence=3;frame=read_frame(5)
if frame.get('action')=='auth_finish':
    binding=bound(frame,execution_sequence,'auth_finish');args=frame['arguments']
    assert MANAGED_AUTH and AUTH_MODE in {'login','status','disconnect'}
    assert set(args)=={'timeout'} and type(args['timeout']) in (int,float) and 0<args['timeout']<=80
    deadline=time.monotonic()+args['timeout']
    if AUTH_MODE=='disconnect':
        logout=subprocess.run([BINARY,'-c','cli_auth_credentials_store="file"','logout'],env=environment,cwd=WORK,
            stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=min(2,args['timeout']),check=False)
        assert logout.returncode==0
    status=subprocess.run([BINARY,'-c','cli_auth_credentials_store="file"','login','status'],env=environment,cwd=WORK,
        stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=min(2,args['timeout']),check=False)
    authenticated=status.returncode==0
    if authenticated is (AUTH_MODE!='disconnect'):
        result={'reason':'completed','returncode':0,'stdout':json.dumps({'authenticated':authenticated,'operation':AUTH_MODE}),'stderr':''}
        binding,result=return_owned_auth(binding,result,deadline,logged_out=not authenticated);emit(binding,result)
    else:emit(binding,{'reason':'authentication_required'})
else:
    binding=bound(frame,execution_sequence,'execute');args=frame['arguments']
    assert not MANAGED_AUTH or AUTH_MODE=='use'
    assert type(args) is dict and set(args)=={'input','timeout'} and type(args['input']) is str and len(args['input'].encode())<=32768
    assert type(args['timeout']) in (int,float) and 0<args['timeout']<=80
    deadline=time.monotonic()+args['timeout']
    if status.returncode!=0:emit(binding,{'reason':'authentication_required'})
    else:
        binding,result=run_codex(frame,binding,args,environment)
        if MANAGED_AUTH and result['returncode']!=0:raise PermissionError('Codex execution or authentication unconfirmed')
        binding,result=return_owned_auth(binding,result,deadline);emit(binding,result)
try:read_frame(5)
except (EOFError,TimeoutError):pass
'''.replace('__CURIS_STDIO_SOURCE__',repr(_AGENT_MCP_STDIO_SOURCE))


def _serve_codex_provider_tunnel(proxy, raw):
    """Private CONNECT transport; release still requires the original outer filter."""
    import select, socket
    from .agent_browser_policy import PublicReadProxy
    if proxy.policy.hosts != frozenset({"auth.openai.com","chatgpt.com"}):
        raise PermissionError("Provider authorities must match the pinned source")
    upstream=None
    proxy.track(raw)
    try:
        proxy.check()
        stream=raw.makefile("rb",buffering=0)
        try:
            line=stream.readline(8193)
            if len(line)>8192:raise ValueError("Provider CONNECT line bound")
            fields=line.decode("ascii").rstrip("\r\n").split(" ")
            if (len(fields)!=3 or fields[0]!="CONNECT" or fields[2]!="HTTP/1.1"
                    or fields[1] not in {"auth.openai.com:443","chatgpt.com:443"}):
                raise PermissionError("Provider CONNECT authority rejected")
            headers=PublicReadProxy.headers(stream)
            if (headers.get("Host")!=fields[1] or headers.get("Transfer-Encoding") is not None
                    or headers.get("Content-Length","0")!="0" or headers.get("Proxy-Authorization") is not None):
                raise PermissionError("Provider CONNECT header rejected")
        finally:stream.close()
        host=fields[1][:-4]
        addresses=proxy.policy.resolve(host)
        proxy.check()
        # PublicTargets validates every address. Connect only its literal result.
        family,kind,protocol,_,address=addresses[0]
        upstream=proxy.track(socket.socket(family,kind,protocol))
        upstream.connect(address)
        proxy.check();raw.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")
        readers=[raw,upstream]
        while readers:
            proxy.check()
            readable,_,_=select.select(readers,[],[],.05)
            for source in readable:
                destination=upstream if source is raw else raw
                chunk=source.recv(65536)
                if not chunk:
                    readers.remove(source)
                    destination.shutdown(socket.SHUT_WR)
                    continue
                with proxy.lock:
                    proxy.total_bytes+=len(chunk)
                    if proxy.total_bytes>32*1024*1024:raise ValueError("Provider tunnel byte bound")
                proxy.check();destination.sendall(chunk)
    finally:
        for connection in (upstream,raw):
            if connection is not None:
                with proxy.lock:proxy.sockets.discard(connection)
                connection.close()


class _DedicatedDockerOwner:
    """Private real Docker lifecycle candidate, not an accepted Reader adapter.

    prepare() allocates stopped containers; start_runtime() explicitly bootstraps
    the private pair. The bundled production lock remains closed pending
    independent sandbox/egress evidence. No caller-supplied connection is accepted.
    """
    def __init__(self, identity, image_digest):
        import re
        keys = {"tenant_id", "company_id", "work_ref", "task_id", "employee_id", "binding_ref"}
        if (type(identity) is not dict or set(identity) != keys
                or any(type(v) is not str or not v for v in identity.values())
                or type(image_digest) is not str or not re.fullmatch(r"sha256:[0-9a-f]{64}", image_digest)):
            raise PermissionError("Dedicated owner binding invalid")
        self.identity, self.image_digest = identity.copy(), image_digest
        self.connection = _DedicatedDockerSSH()
        self.journal, self.boot_id, self.container_id, self.nonce = None, None, None, None
        self.revoked, self.stop_requested = False, False
        self.private_network = self.external_network = self.proxy_id = None
        self.channels = []
        self.stop_receipt = None
        self._stop_done = threading.Event()
        self._filter_snapshot = None
        self._filter_install_attempted = False
        self._admission_lock = threading.Lock()
        self._revoked_event = threading.Event()
        self._state_lock = threading.Lock()

    def prepare_agent(self, nonce):
        self._agent_candidate = True
        self._provider_mode = getattr(self,"_linux_bootstrap",None) is not None
        return self.prepare(nonce, hosts=["auth.openai.com","chatgpt.com"] if self._provider_mode else None, _agent=True)

    def prepare(self, nonce, *, hosts=None, _agent=False):
        import hashlib, json, re
        if type(nonce) is not str or not re.fullmatch(r"[0-9a-f]{48}", nonce):
            raise PermissionError("Dedicated owner nonce invalid")
        from contextlib import nullcontext
        provider=getattr(self,"_provider_mode",False)
        if (type(_agent) is not bool or _agent and hosts is not None and
                (not provider or hosts != ["auth.openai.com","chatgpt.com"])):
            raise PermissionError("Agent candidate cannot acquire Reader egress")
        with self._state_lock:
            if self.nonce is not None or self.revoked:
                raise PermissionError("Dedicated owner cannot be reused")
            self.nonce = nonce  # Failed preparation is never retried.
        # Validate and retain immutable inputs before any remote operation or
        # durable resource allocation, including creation of private networks.
        if hosts is not None:
            from .agent_browser_policy import PublicTargets
            self.hosts = sorted(PublicTargets(hosts).hosts)
            self._seccomp_profile = _private_seccomp()
        version = self.connection.request("GET", "/version")
        info = version["body"]
        if type(info) is not dict or info.get("Os") != "linux" or info.get("Arch") != "arm64" or info.get("Version") != "29.5.2":
            raise PermissionError("Dedicated Docker daemon identity/version mismatch")
        self.boot_id = version["boot_id"]
        image = self.connection.request("GET", "/images/"+self.image_digest+"/json", boot_id=self.boot_id)["body"]
        if (type(image) is not dict or image.get("Id") != self.image_digest
                or image.get("Os") != "linux" or image.get("Architecture") != "arm64"):
            raise PermissionError("Dedicated derived image identity mismatch")
        self._image_labels = _verified_image_labels(image, self.image_digest)
        parent = getattr(self, "_work_parent", None)
        self.journal = parent.borrow(self) if parent is not None else _OwnerJournal()
        try:
            if parent is not None:
                parent.verify_prior(self, nonce)
            else:
                self._verify_prior_holds(nonce)
                peer = getattr(self.journal, "peer", None)
                if peer is not None:
                    audit = _DedicatedDockerOwner(self.identity, self.image_digest)
                    audit.boot_id, audit.journal = self.boot_id, peer
                    audit._verify_prior_holds(nonce)
            work = hashlib.sha256(json.dumps(self.identity, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
            self._record = {"work":work,"nonce":nonce,"boot_id":self.boot_id,"image_digest":self.image_digest}
            if parent is not None: self._record["parent_attempt"] = parent.attempt
            if hosts is not None:
                self._record["network_retirement"] = "OWNED_NETWORK_RETIRE_V1"
                self._record["netns_filter"] = "IPTABLES_NETNS_AGENT_PAIRED_V1" if getattr(self,"_paired_provider",False) else "IPTABLES_NETNS_V1"
            if not _agent or provider:
                self.journal.append({**self._record,"state":"INTENT"})  # Must fsync before Docker mutation.
            if hosts is not None:
                self._create_networks()
            config = {"Image":self.image_digest,"User":"pwuser","WorkingDir":"/tmp",
                "Entrypoint":["python3","-I","-B","-c","import sys; sys.path.insert(0, '/opt/curis/reader'); from app.agent_browser_guest import main; main()","--stdio"],
                "Env":["PATH=/usr/bin:/bin","LANG=C.UTF-8"],"OpenStdin":True,"StdinOnce":False,"Tty":False,
                "AttachStdin":True,"AttachStdout":True,"AttachStderr":False,
                "Labels":{"curis.reader.work":work,"curis.reader.nonce":nonce},
                "HostConfig":{"NetworkMode":"none","ReadonlyRootfs":True,"Privileged":False,
                    "CapDrop":["ALL"],"SecurityOpt":["no-new-privileges"],"IpcMode":"private","ShmSize":268435456,
                    "Tmpfs":{"/tmp":"rw,nosuid,nodev,size=512m,mode=1777"},"Memory":1610612736,"PidsLimit":192,
                    "NanoCpus":1000000000,"RestartPolicy":{"Name":"no"},"Binds":[],"PortBindings":{},
                    "LogConfig":{"Type":"local","Config":{"max-size":"1m","max-file":"2"}}}}
            if _agent:
                config["Entrypoint"]=["/usr/bin/python3","-I","-B","-c",
                    _AGENT_CODEX_SOURCE if getattr(self,"_linux_bootstrap",None) is not None else _AGENT_CONTAINER_SOURCE]
                config["Cmd"]=["--curis-agent-container"]
                config["StdinOnce"]=True
                if provider:config["HostConfig"]["LogConfig"]={"Type":"none","Config":{}}
                config["Env"] += ["CURIS_AGENT_CONTAINER_WORK="+work,"CURIS_AGENT_CONTAINER_NONCE="+nonce,
                                  "CURIS_AGENT_CONTAINER_IMAGE="+self.image_digest]
                if getattr(self,"_paired_provider",False): config["Env"].append("CURIS_AGENT_PAIRED_NETWORK=1")
                self._agent_config = config
                self._agent_image_env = image.get("Config",{}).get("Env") or []
            if hosts is not None:
                config["HostConfig"].update({"NetworkMode":self.private_network,"Dns":["127.0.0.1"],
                    "Sysctls":{"net.ipv6.conf.all.disable_ipv6":"1","net.ipv6.conf.default.disable_ipv6":"1"},
                    "SecurityOpt":["no-new-privileges", "seccomp="+self._seccomp_profile]})
                private,external = self._network_prefixes()
                config["NetworkingConfig"]={"EndpointsConfig":{self.private_network:{"IPAMConfig":{"IPv4Address":private+".3"}}}}
                import copy
                proxy_config=copy.deepcopy(config)
                proxy_config["Entrypoint"]=["python3","-I","-B","-c","import sys; sys.path.insert(0, '/opt/curis/reader'); from app.reader_vm_host import proxy_main; proxy_main()","--proxy-stdio"]
                if provider:
                    proxy_config["Entrypoint"]=["python3","-I","-B","-c","import sys; sys.path.insert(0, '/opt/curis/reader'); from app.reader_vm_host import provider_proxy_main; provider_proxy_main()"]
                    proxy_config["Cmd"]=["--provider-proxy-stdio"]
                    self._provider_proxy_config=proxy_config
                proxy_config["HostConfig"]["Dns"]=["1.1.1.1"]
                proxy_config["Labels"]={**config["Labels"],"curis.reader.role":"proxy"}
                proxy_config["NetworkingConfig"]={"EndpointsConfig":{
                    self.private_network:{"IPAMConfig":{"IPv4Address":private+".2"},"GwPriority":0},
                    self.external_network:{"IPAMConfig":{"IPv4Address":external+".2"},"GwPriority":1}}}
                with self._state_lock if _agent else nullcontext():
                    if _agent and (self.revoked or self._revoked_event.is_set()):raise PermissionError("Agent proxy allocation revoked")
                    proxy=self.connection.request("POST","/containers/create",boot_id=self.boot_id,body=proxy_config)["body"]
                    if type(proxy) is not dict or not re.fullmatch(r"[0-9a-f]{64}",str(proxy.get("Id",""))):
                        raise PermissionError("Proxy create UNKNOWN; never adopt or retry")
                    self.proxy_id=proxy["Id"]
                    self.journal.append({**self._record,"state":"PROXY_CREATED","container_id":self.proxy_id})
            if _agent:
                # Serialize allocation/ID retention with revocation, as for start.
                with self._state_lock:
                    if self.revoked or self._revoked_event.is_set():
                        raise PermissionError("Agent allocation revoked")
                    if not provider:self.journal.append({**self._record,"state":"INTENT"})
                    result = self.connection.request("POST", "/containers/create", boot_id=self.boot_id, body=config)["body"]
                    if type(result) is not dict or not re.fullmatch(r"[0-9a-f]{64}",str(result.get("Id",""))):
                        raise PermissionError("Agent create UNKNOWN; no guessing or retry")
                    self.container_id=result["Id"]
                    self.journal.append({**self._record,"state":"CREATED","container_id":self.container_id})
            else:
                result = self.connection.request("POST", "/containers/create", boot_id=self.boot_id, body=config)["body"]
                if type(result) is not dict or not re.fullmatch(r"[0-9a-f]{64}", str(result.get("Id", ""))):
                    raise PermissionError("Docker create outcome UNKNOWN; no resource guessed or retried")
                self.container_id = result["Id"]
            if not _agent:
                self.journal.append({**self._record,"state":"CREATED","container_id":self.container_id})
            state = self._inspect().get("State", {})
            if state.get("Running") is not False or state.get("Restarting") is not False or state.get("Pid") != 0:
                raise PermissionError("Prepared container is unexpectedly running; retain UNKNOWN")
            return {"boot_id":self.boot_id,"container_id":self.container_id,"image_digest":self.image_digest,
                    "running":False,"executionAuthorized":False}
        except BaseException as error:
            self._revoked_event.set()
            with self._state_lock:
                self.revoked = True
            if self.container_id or self.proxy_id:
                try:
                    self.revoke_bound_and_stop(self.identity.copy(), self.nonce, {
                        "complete":False, "executionAuthorized":False,
                        "boot_id":self.boot_id, "container_id":self.container_id,
                        "image_digest":self.image_digest})
                except BaseException:
                    error.add_note("Original prepare cleanup UNKNOWN; no retry or reuse")
            else:
                try:
                    self.journal.close()
                except BaseException:
                    error.add_note("Owner journal close failed; hold remains UNKNOWN")
            raise

    def _history_groups(self, nonce=None, *, recovery=False):
        """Prior boots require a verified closure audit or completed retained-resource recovery."""
        import re, json
        groups, seen_nonces, seen_ids = [], set(), set()
        audited_prefix = 0
        base_keys = {"work", "nonce", "boot_id", "image_digest"}
        for index,row in enumerate(self.journal.records):
            if type(row) is not dict:
                raise PermissionError("Owner history is malformed")
            state = row.get("state")
            if state == "BOOT_CLOSURES_VERIFIED":
                if (set(row)!={"state","boot_id","prior_ledger_sha256","history_sha256","closures_sha256"}
                        or not groups or any(g["state"]!="CLOSED_VERIFIED" for g in groups)
                        or not re.fullmatch(r"[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}",str(row.get("boot_id")))
                        or not re.fullmatch(r"[0-9a-f]{64}",str(row.get("prior_ledger_sha256")))
                        or row.get("history_sha256")!=hashlib.sha256(json.dumps(self.journal.records[:index],sort_keys=True,separators=(",", ":")).encode()).hexdigest()
                        or row.get("closures_sha256")!=hashlib.sha256(json.dumps(groups,sort_keys=True,separators=(",", ":")).encode()).hexdigest()):
                    raise PermissionError("Closed-history boot audit is invalid")
                if row["boot_id"] == self.boot_id:audited_prefix = len(groups)
                continue
            if state == "INTENT":
                if groups and groups[-1]["state"] != "CLOSED_VERIFIED":
                    raise PermissionError("Prior owner history is unresolved")
                base_keys = {"work", "nonce", "boot_id", "image_digest"}
                if "network_retirement" in row:
                    base_keys.add("network_retirement")
                    if row["network_retirement"] != "OWNED_NETWORK_RETIRE_V1":
                        raise PermissionError("Owner retirement scope is unknown")
                if "netns_filter" in row:
                    base_keys.add("netns_filter")
                    if row["netns_filter"] not in {"IPTABLES_NETNS_V1","IPTABLES_NETNS_AGENT_PAIRED_V1"}:
                        raise PermissionError("Owner filter scope is unknown")
                if "parent_attempt" in row:
                    base_keys.add("parent_attempt")
                    if not re.fullmatch(r"[0-9a-f]{48}", str(row["parent_attempt"])):
                        raise PermissionError("Original parent attempt is invalid")
                if (set(row) != base_keys | {"state"}
                        or not re.fullmatch(r"[0-9a-f]{64}", str(row.get("work", "")))
                        or not re.fullmatch(r"[0-9a-f]{48}", str(row.get("nonce", "")))
                        or not re.fullmatch(r"sha256:[0-9a-f]{64}", str(row.get("image_digest", "")))
                        or not re.fullmatch(r"[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}", str(row.get("boot_id", "")))
                        or row["nonce"] in seen_nonces or row["nonce"] == nonce):
                    raise PermissionError("Owner history binding or boot changed")
                seen_nonces.add(row["nonce"])
                groups.append({"base":{k:row[k] for k in base_keys}, "state":state,
                               "networks":{}, "container_id":None, "proxy_id":None,"filter_state":None})
                continue
            if not groups:
                raise PermissionError("Owner history lacks intent")
            group = groups[-1]
            if any(row.get(k) != v for k,v in group["base"].items()):
                raise PermissionError("Owner history generation changed")
            previous = group["state"]
            extra = set()
            if state == "NETWORK":
                role = row.get("role")
                expected = "INTENT" if role == "private" else "NETWORK"
                if (role not in {"private", "external"} or previous != expected
                        or role in group["networks"]
                        or (role == "external" and set(group["networks"]) != {"private"})):
                    raise PermissionError("Owner network history is incomplete")
                value = row.get("network_id")
                extra = {"role", "network_id"}
                group["networks"][role] = value
            elif state in {"PROXY_CREATED", "CREATED"}:
                networked = bool(group["networks"])
                expected = ("NETWORK" if state == "PROXY_CREATED" else
                            "PROXY_CREATED" if networked else "INTENT")
                if (previous != expected or (networked and set(group["networks"]) != {"private", "external"})
                        or (state == "PROXY_CREATED" and not networked)):
                    raise PermissionError("Owner container history is incomplete")
                value = row.get("container_id")
                extra = {"container_id"}
                group["proxy_id" if state == "PROXY_CREATED" else "container_id"] = value
            elif state == "AGENT_REVOKED_RECOVERY_INTENT" or previous == "AGENT_REVOKED_RECOVERY_INTENT":
                extra = {"container_id","proxy_id","recovery_boot_id","recovery_ledger_sha256",
                         "recovery_inspection_sha256","recovery_prior_sha256","exit_codes"}
                if (previous != ("REVOKING" if state == "AGENT_REVOKED_RECOVERY_INTENT" else "AGENT_REVOKED_RECOVERY_INTENT")
                        or state not in {"AGENT_REVOKED_RECOVERY_INTENT","CLOSED_VERIFIED"}
                        or group["networks"] or group["proxy_id"] is not None or group["filter_state"] is not None
                        or set(group["base"]) != {"work","nonce","boot_id","image_digest"}
                        or row.get("container_id") != group["container_id"] or row.get("proxy_id") is not None
                        or not re.fullmatch(r"[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}",str(row.get("recovery_boot_id")))
                        or row["recovery_boot_id"] == group["base"]["boot_id"]
                        or any(not re.fullmatch(r"[0-9a-f]{64}",str(row.get(k))) for k in
                               ("recovery_ledger_sha256","recovery_inspection_sha256","recovery_prior_sha256"))
                        or type(row.get("exit_codes")) is not dict or set(row["exit_codes"]) != {group["container_id"]}
                        or type(row["exit_codes"][group["container_id"]]) is not int):
                    raise PermissionError("Agent revoked recovery history changed")
                for key in extra - {"container_id","proxy_id"}:
                    if previous == "AGENT_REVOKED_RECOVERY_INTENT" and row[key] != group[key]:
                        raise PermissionError("Agent recovery receipt changed")
                    group[key] = row[key]
                group["recovery_kind"] = "stopped"
                value = None
            elif state in {"START_INTENT", "NETNS_FILTER_INTENT", "NETNS_FILTER_VERIFIED", "ATTACHED", "REVOKING", "STOP_RETURNED", "NETWORK_RETIRE_INTENT", "NETWORKS_RETIRED", "UNSTARTED_RECOVERY_INTENT", "STOPPED_RECOVERY_INTENT", "RETIREMENT_RECOVERY_INTENT", "CLOSED_VERIFIED"}:
                guarded = group["base"].get("netns_filter") in {"IPTABLES_NETNS_V1","IPTABLES_NETNS_AGENT_PAIRED_V1"}
                allowed = {"START_INTENT":{"CREATED"},
                           "NETNS_FILTER_INTENT":{"START_INTENT"} if guarded else set(),
                           "NETNS_FILTER_VERIFIED":{"NETNS_FILTER_INTENT"} if guarded else set(),
                           "ATTACHED":{"NETNS_FILTER_VERIFIED"} if guarded else {"START_INTENT"},
                           "REVOKING":{"CREATED", "START_INTENT", "NETNS_FILTER_INTENT", "NETNS_FILTER_VERIFIED", "ATTACHED"},
                           "STOP_RETURNED":{"REVOKING"}, "NETWORK_RETIRE_INTENT":{"STOP_RETURNED"},
                           "NETWORKS_RETIRED":{"NETWORK_RETIRE_INTENT"},
                           "UNSTARTED_RECOVERY_INTENT":{"CREATED"},
                           "STOPPED_RECOVERY_INTENT":{"STOP_RETURNED"},
                           "RETIREMENT_RECOVERY_INTENT":{"NETWORK_RETIRE_INTENT"},
                           "CLOSED_VERIFIED":{"NETWORKS_RETIRED", "UNSTARTED_RECOVERY_INTENT", "STOPPED_RECOVERY_INTENT", "RETIREMENT_RECOVERY_INTENT"} if group["networks"] else {"STOP_RETURNED"}}
                if (previous not in allowed[state] or row.get("container_id") != group["container_id"]
                        or row.get("proxy_id") != group["proxy_id"]):
                    raise PermissionError("Owner lifecycle history is out of order")
                extra = {"container_id", "proxy_id"}
                if state == "NETNS_FILTER_INTENT":
                    group["filter_state"] = "INTENT"
                if state == "NETNS_FILTER_VERIFIED":
                    extra.add("filter")
                    bound = {key:group["base"][key] for key in ("boot_id","image_digest","work","nonce")}
                    _netns_receipt({**bound,"container_id":group["container_id"],
                                   "network_id":group["networks"].get("private")},row.get("filter"),
                                   paired=group["base"].get("netns_filter")=="IPTABLES_NETNS_AGENT_PAIRED_V1")
                    group["filter_state"] = "VERIFIED"
                if state in {"NETWORK_RETIRE_INTENT", "NETWORKS_RETIRED", "UNSTARTED_RECOVERY_INTENT", "STOPPED_RECOVERY_INTENT", "RETIREMENT_RECOVERY_INTENT", "CLOSED_VERIFIED"} and group["networks"]:
                    extra.add("networks")
                    if row.get("networks") != group["networks"] or group["base"].get("network_retirement") != "OWNED_NETWORK_RETIRE_V1":
                        raise PermissionError("Network retirement lacks future-owned scope")
                if state in {"UNSTARTED_RECOVERY_INTENT","STOPPED_RECOVERY_INTENT","RETIREMENT_RECOVERY_INTENT"} or previous in {"UNSTARTED_RECOVERY_INTENT","STOPPED_RECOVERY_INTENT","RETIREMENT_RECOVERY_INTENT"}:
                    stopped = state in {"STOPPED_RECOVERY_INTENT","RETIREMENT_RECOVERY_INTENT"} or previous in {"STOPPED_RECOVERY_INTENT","RETIREMENT_RECOVERY_INTENT"}
                    retirement = state == "RETIREMENT_RECOVERY_INTENT" or previous == "RETIREMENT_RECOVERY_INTENT"
                    extra.update({"recovery_boot_id", "recovery_ledger_sha256"})
                    boot = row.get("recovery_boot_id")
                    ledger_hash = row.get("recovery_ledger_sha256")
                    if (not re.fullmatch(r"[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}", str(boot))
                            or not re.fullmatch(r"[0-9a-f]{64}", str(ledger_hash))
                            or boot == group["base"]["boot_id"]
                            or (previous in {"UNSTARTED_RECOVERY_INTENT","STOPPED_RECOVERY_INTENT","RETIREMENT_RECOVERY_INTENT"} and
                                (boot != group["recovery_boot_id"] or ledger_hash != group["recovery_ledger_sha256"]))
                            or group["filter_state"] not in ({"INTENT","VERIFIED"} if retirement else {"INTENT"} if stopped else {None})
                            or set(group["networks"]) != {"private", "external"}):
                        raise PermissionError("Recovery history changed")
                    if previous in {"UNSTARTED_RECOVERY_INTENT","STOPPED_RECOVERY_INTENT","RETIREMENT_RECOVERY_INTENT"}:
                        exits = row.get("exit_codes")
                        if (type(exits) is not dict or set(exits)!={group["container_id"],group["proxy_id"]}
                                or any(type(v) is not int for v in exits.values())
                                or (not stopped and any(v!=0 for v in exits.values()))):
                            raise PermissionError("Recovery exit receipt changed")
                    group["recovery_boot_id"] = boot
                    group["recovery_ledger_sha256"] = ledger_hash
                    group["recovery_kind"] = "stopped" if stopped else "unstarted"
                    if stopped:
                        extra.update({"filter_outcome","recovery_inspection_sha256","recovery_prior_sha256"})
                        for key in ("recovery_inspection_sha256","recovery_prior_sha256"):
                            if (not re.fullmatch(r"[0-9a-f]{64}",str(row.get(key))) or
                                    previous in {"STOPPED_RECOVERY_INTENT","RETIREMENT_RECOVERY_INTENT"} and row[key] != group[key]):
                                raise PermissionError("Stopped recovery inspection changed")
                            group[key] = row[key]
                        if row.get("filter_outcome") != "UNKNOWN":
                            raise PermissionError("Recovery cannot promote filter outcome")
                        exits = row.get("exit_codes")
                        if (type(exits) is not dict or set(exits)!={group["container_id"],group["proxy_id"]}
                                or any(type(v) is not int for v in exits.values())
                                or previous in {"STOPPED_RECOVERY_INTENT","RETIREMENT_RECOVERY_INTENT"} and exits != group["recovery_exit_codes"]):
                            raise PermissionError("Stopped recovery exit snapshot changed")
                        group["recovery_exit_codes"] = exits.copy()
                        group["filter_outcome"] = "UNKNOWN"
                if state == "NETWORK_RETIRE_INTENT":
                    exits = row.get("exit_codes")
                    if (type(exits) is not dict or set(exits)!={group["container_id"],group["proxy_id"]}
                            or any(type(v) is not int for v in exits.values())):
                        raise PermissionError("Retirement lacks exact stopped exit receipt")
                    group["retirement_exit_codes"] = exits.copy()
                if state == "RETIREMENT_RECOVERY_INTENT" and row.get("exit_codes") != group.get("retirement_exit_codes"):
                    raise PermissionError("Retirement recovery exit receipt changed")
                if "exit_codes" in row:
                    extra.add("exit_codes")
                if state == "CLOSED_VERIFIED":
                    group["exit_codes"] = row.get("exit_codes")
                    group.pop("retirement_exit_codes",None)
                value = None
            else:
                raise PermissionError("Owner history state is unknown")
            if set(row) != base_keys | {"state"} | extra:
                raise PermissionError("Owner history fields are ambiguous")
            if state in {"NETWORK", "PROXY_CREATED", "CREATED"}:
                if not re.fullmatch(r"[0-9a-f]{64}", str(value)) or value in seen_ids:
                    raise PermissionError("Owner resource ID is ambiguous")
                seen_ids.add(value)
            group["state"] = state
        covered = audited_prefix
        for index,group in enumerate(groups):
            if group.get("recovery_kind") == "stopped":
                import json
                prior = hashlib.sha256(json.dumps(groups[:index],sort_keys=True,separators=(",", ":")).encode()).hexdigest()
                if group.get("recovery_prior_sha256") != prior:
                    raise PermissionError("Recovery prior closures changed")
                if group["state"] == "CLOSED_VERIFIED" and group.get("recovery_boot_id") == self.boot_id:
                    covered = max(covered,index)
        if not recovery and any(g["base"]["boot_id"] != self.boot_id and index >= covered and
                not (g["state"] == "CLOSED_VERIFIED" and g.get("recovery_boot_id") == self.boot_id)
                for index,g in enumerate(groups)):
            raise _HistoryBootChanged("Owner history binding or boot changed")
        return groups

    def recover_revoked_agent(self, expected, *, ledger_sha256, inspection_sha256):
        """Audit an exact stopped retained generation after reboot; never start or stop it."""
        import hashlib, json, os, re
        with self._state_lock:
            if self.nonce is not None or self.revoked or getattr(self,"_recovery_attempted",False):
                raise PermissionError("Recovery owner cannot be reused")
            self._recovery_attempted = self.revoked = True
        self._revoked_event.set()
        work = hashlib.sha256(json.dumps(self.identity,sort_keys=True,separators=(",",":")).encode()).hexdigest()
        if (type(expected) is not dict or set(expected) != {"work","nonce","boot_id","image_digest","container_id","proxy_id","networks"}
                or expected["work"] != work or expected["image_digest"] != _AGENT_CONTAINER_IMAGE
                or self.image_digest != _AGENT_CONTAINER_IMAGE or expected["proxy_id"] is not None or expected["networks"] != {}
                or any(not re.fullmatch(r"[0-9a-f]{64}",str(v)) for v in (ledger_sha256,inspection_sha256))):
            raise PermissionError("Recovery requires exact Agent pins")
        expected = json.loads(json.dumps(expected,allow_nan=False))
        self.journal = _OwnerJournal()
        try:
            original = os.pread(self.journal.ledger_fd,1048577,0)
            if hashlib.sha256(original).hexdigest() != ledger_sha256:raise PermissionError("Recovery ledger changed")
            version = self.connection.request("GET","/version")
            if (version["body"].get("Os") != "linux" or version["body"].get("Arch") != "arm64"
                    or version["body"].get("Version") != "29.5.2" or version["boot_id"] == expected["boot_id"]):
                raise PermissionError("Recovery requires verified new boot")
            self.boot_id = version["boot_id"]
            groups = self._history_groups(recovery=True)
            if not groups:raise PermissionError("Recovery history missing")
            group = groups[-1]
            pins = {**group["base"],**{k:group[k] for k in ("container_id","proxy_id","networks")}}
            if (pins != expected or group["state"] != "REVOKING" or group["filter_state"] is not None
                    or set(group["base"]) != {"work","nonce","boot_id","image_digest"}):
                raise PermissionError("Recovery is not the original revoked Agent")
            for prior in groups[:-1]:
                if prior["state"] != "CLOSED_VERIFIED" or self._group_exits(prior) != prior.get("exit_codes"):
                    raise PermissionError("Prior retained generation unresolved")
                for nid in prior["networks"].values():
                    if self.connection.request("GET","/networks/"+nid,boot_id=self.boot_id)["status"] != 404:
                        raise PermissionError("Prior retired network returned")
            def inspect():
                exits = self._group_exits(group)
                info = self.connection.request("GET","/containers/"+expected["container_id"]+"/json",boot_id=self.boot_id)["body"]
                cfg = info.get("HostConfig",{})
                if (not _stopped_container(info) or cfg.get("NetworkMode") != "none" or cfg.get("PidMode")
                        or cfg.get("Binds") or cfg.get("Privileged") is not False
                        or not _stopped_agent_networks(info.get("NetworkSettings",{}).get("Networks"))):
                    raise PermissionError("Recovery Agent isolation or stopped state changed")
                snapshot = {"containers":{expected["container_id"]:info},"networks":{}}
                if hashlib.sha256(json.dumps(snapshot,sort_keys=True,separators=(",",":"),allow_nan=False).encode()).hexdigest() != inspection_sha256:
                    raise PermissionError("Recovery inspection differs from approved snapshot")
                return exits
            exits = inspect()
            if os.pread(self.journal.ledger_fd,1048577,0) != original:raise PermissionError("Recovery ledger changed before intent")
            receipt = {**group["base"],"container_id":expected["container_id"],"proxy_id":None,
                "recovery_boot_id":self.boot_id,"recovery_ledger_sha256":ledger_sha256,
                "recovery_inspection_sha256":inspection_sha256,
                "recovery_prior_sha256":hashlib.sha256(json.dumps(groups[:-1],sort_keys=True,separators=(",",":")).encode()).hexdigest(),
                "exit_codes":exits}
            self.journal.append({**receipt,"state":"AGENT_REVOKED_RECOVERY_INTENT"})
            if inspect() != exits:raise PermissionError("Recovery exit changed")
            self.journal.append({**receipt,"state":"CLOSED_VERIFIED"})
            return {**receipt,"state":"CLOSED_VERIFIED","containers_retained":True,"effects":"UNKNOWN","descendants":"UNKNOWN"}
        finally:
            self.journal.close()

    def recover_unstarted(self, expected, *, ledger_sha256):
        return self._recover_retained(expected,ledger_sha256=ledger_sha256,inspection_sha256=None)

    def recover_stopped(self, expected, *, ledger_sha256, inspection_sha256):
        if type(inspection_sha256) is not str:
            raise PermissionError("Stopped recovery requires approved inspection digest")
        return self._recover_retained(expected,ledger_sha256=ledger_sha256,inspection_sha256=inspection_sha256)

    def recover_retirement(self, expected, *, ledger_sha256, inspection_sha256):
        """Recover only a pinned, interrupted network retirement after a new boot."""
        if type(inspection_sha256) is not str:
            raise PermissionError("Retirement recovery requires approved inspection digest")
        return self._recover_retained(expected,ledger_sha256=ledger_sha256,
            inspection_sha256=inspection_sha256,retirement=True)

    def _recover_retained(self, expected, *, ledger_sha256, inspection_sha256, retirement=False):
        """Explicit exact-generation recovery; never called by prepare or retried."""
        import hashlib, json, os, re
        stopped = inspection_sha256 is not None
        if stopped and not re.fullmatch(r"[0-9a-f]{64}",str(inspection_sha256)):
            raise PermissionError("Stopped recovery requires approved inspection digest")
        with self._state_lock:
            if self.nonce is not None or self.revoked or getattr(self, "_recovery_attempted", False):
                raise PermissionError("Recovery owner cannot be reused")
            self._recovery_attempted = self.revoked = True
        self._revoked_event.set()
        keys = {"work", "nonce", "boot_id", "image_digest", "container_id", "proxy_id", "networks"}
        work = hashlib.sha256(json.dumps(self.identity,sort_keys=True,separators=(",", ":")).encode()).hexdigest()
        if (type(expected) is not dict or set(expected) != keys or expected["work"] != work
                or expected["image_digest"] != self.image_digest
                or not re.fullmatch(r"[0-9a-f]{64}", str(ledger_sha256))):
            raise PermissionError("Recovery requires exact original pins")
        expected = json.loads(json.dumps(expected,allow_nan=False))
        self.journal = _OwnerJournal()
        try:
            original = os.pread(self.journal.ledger_fd,1048577,0)
            if hashlib.sha256(original).hexdigest() != ledger_sha256:
                raise PermissionError("Recovery ledger changed")
            version = self.connection.request("GET", "/version")
            if (version["body"].get("Os") != "linux" or version["body"].get("Arch") != "arm64"
                    or version["body"].get("Version") != "29.5.2" or version["boot_id"] == expected["boot_id"]):
                raise PermissionError("Recovery requires verified new boot")
            self.boot_id = version["boot_id"]
            groups = self._history_groups(recovery=True)
            if not groups or (not stopped and (len(groups) != 1 or len(self.journal.records) != 5)):
                raise PermissionError("Recovery is restricted to one original created generation")
            group = groups[-1]
            for prior in groups[:-1]:
                if prior["state"] != "CLOSED_VERIFIED" or self._group_exits(prior) != prior.get("exit_codes"):
                    raise PermissionError("Prior retained generation is unresolved")
                for nid in prior["networks"].values():
                    if self.connection.request("GET","/networks/"+nid,boot_id=self.boot_id)["status"]!=404:
                        raise PermissionError("Prior retired network returned")
            pins = {**{k:group["base"][k] for k in ("work","nonce","boot_id","image_digest")},
                    **{k:group[k] for k in ("container_id","proxy_id","networks")}}
            if (pins != expected or group["state"] != ("NETWORK_RETIRE_INTENT" if retirement else "STOP_RETURNED" if stopped else "CREATED")
                    or group["filter_state"] not in ({"INTENT","VERIFIED"} if retirement else {"INTENT"} if stopped else {None})
                    or set(group["networks"]) != {"private","external"}
                    or group["base"].get("network_retirement") != "OWNED_NETWORK_RETIRE_V1"
                    or group["base"].get("netns_filter") != "IPTABLES_NETNS_V1"):
                raise PermissionError("Recovery generation is not the pinned recoverable pair")
            image = self.connection.request("GET", "/images/"+self.image_digest+"/json", boot_id=self.boot_id)["body"]
            inherited = _verified_image_labels(image,self.image_digest)
            labels = {**inherited,"curis.reader.work":expected["work"],"curis.reader.nonce":expected["nonce"]}
            names = {"curis-reader-"+expected["nonce"]+"-"+role:nid for role,nid in expected["networks"].items()}
            removed,detached = set(),set()
            baseline = None
            if retirement:
                for nid in expected["networks"].values():
                    response = self.connection.request("GET","/networks/"+nid,boot_id=self.boot_id)
                    if response["status"] == 404:
                        removed.add(nid)
                    elif response["status"] != 200:
                        raise PermissionError("Recovery network status is ambiguous; UNKNOWN")
            def verify():
                nonlocal baseline
                snapshot = {"containers":{},"networks":{}}
                references = set()
                for role in ("proxy", "container"):
                    cid = expected[role+"_id"]
                    info = self.connection.request("GET","/containers/"+cid+"/json",boot_id=self.boot_id)["body"]
                    owned = {**labels,**({"curis.reader.role":"proxy"} if role=="proxy" else {})}
                    cfg = info.get("HostConfig",{})
                    endpoints = info.get("NetworkSettings",{}).get("Networks")
                    if (info.get("Id")!=cid or info.get("Image")!=self.image_digest
                            or info.get("Config",{}).get("Labels")!=owned or info.get("Config",{}).get("User")!="pwuser"
                            or cfg.get("NetworkMode")!=expected["networks"]["private"]
                            or cfg.get("RestartPolicy",{}).get("Name")!="no"
                            or not (_stopped_container(info) if stopped else _never_started_container(info))
                            or type(endpoints) is not dict
                            or retirement and info.get("State",{}).get("ExitCode") != group["retirement_exit_codes"].get(cid)):
                        raise PermissionError("Recovery original container changed; UNKNOWN")
                    allowed = set(expected["networks"].values()) if role=="proxy" else {expected["networks"]["private"]}
                    snapshot["containers"][cid] = json.loads(json.dumps(info,allow_nan=False))
                    if stopped and baseline is not None:
                        old = baseline["containers"][cid]
                        if ({k:v for k,v in info.items() if k!="NetworkSettings"} !=
                                {k:v for k,v in old.items() if k!="NetworkSettings"}
                                or {k:v for k,v in info["NetworkSettings"].items() if k!="Networks"} !=
                                   {k:v for k,v in old["NetworkSettings"].items() if k!="Networks"}):
                            raise PermissionError("Recovery stopped snapshot changed; UNKNOWN")
                    seen = set()
                    for name,endpoint in endpoints.items():
                        nid = names.get(name, name if name in allowed else None)
                        address = "172.30.253.3" if role=="container" else "172.30.253.2" if nid==expected["networks"]["private"] else "172.30.254.2"
                        empty = (_empty_created_endpoint(info,endpoint,address) if not stopped else
                            type(endpoint) is dict and endpoint.get("NetworkID") in {"",nid}
                            and all(endpoint.get(k)=="" for k in ("EndpointID","IPAddress","Gateway","IPv6Gateway","GlobalIPv6Address"))
                            and endpoint.get("IPAMConfig",{}).get("IPv4Address")==address)
                        if nid not in allowed or nid in seen or not empty:
                            raise PermissionError("Recovery has active or foreign endpoint; UNKNOWN")
                        if stopped and baseline is not None:
                            previous = baseline["containers"][cid]["NetworkSettings"]["Networks"].get(name)
                            if (previous is None or (cid,nid) not in detached and nid not in removed and endpoint!=previous
                                    or (cid,nid) in detached and endpoint.get("NetworkID")!=""):
                                raise PermissionError("Recovery endpoint changed outside owned detach; UNKNOWN")
                        if nid in removed and endpoint.get("NetworkID"):
                            raise PermissionError("Retired network still referenced; UNKNOWN")
                        if stopped and endpoint.get("NetworkID")==nid:references.add((cid,nid))
                        seen.add(nid)
                    required = allowed-removed-{nid for target,nid in detached if target==cid}
                    if not required <= seen:
                        raise PermissionError("Recovery configured network missing; UNKNOWN")
                for role,nid in expected["networks"].items():
                    response = self.connection.request("GET","/networks/"+nid,boot_id=self.boot_id)
                    if nid in removed:
                        if response["status"]!=404: raise PermissionError("Recovery removed network returned; UNKNOWN")
                        snapshot["networks"][nid] = None
                        continue
                    info = response["body"]
                    snapshot["networks"][nid] = json.loads(json.dumps(info,allow_nan=False))
                    internal = role=="private"
                    if (response["status"]!=200 or info.get("Id")!=nid or info.get("Name")!="curis-reader-"+expected["nonce"]+"-"+role
                            or info.get("Labels")!={k:labels[k] for k in ("curis.reader.work","curis.reader.nonce")}
                            or info.get("Driver")!="bridge" or info.get("Internal") is not internal
                            or info.get("EnableIPv6") is not False or info.get("Attachable") is not False
                            or info.get("Containers")!={} or type(info.get("Containers")) is not dict
                            or [row.get("Subnet") for row in info.get("IPAM",{}).get("Config",[])]!=["172.30.253.0/29" if internal else "172.30.254.0/29"]
                            or info.get("Options",{}).get("com.docker.network.bridge.gateway_mode_ipv4")!=("isolated" if internal else "nat")
                            or info.get("Options",{}).get("com.docker.network.bridge.enable_icc")!=("true" if internal else "false")):
                        raise PermissionError("Recovery original network is not verified empty; UNKNOWN")
                    if stopped and baseline is not None and info != baseline["networks"][nid]:
                        raise PermissionError("Recovery empty network snapshot changed; UNKNOWN")
                if stopped and baseline is None:
                    digest = hashlib.sha256(json.dumps(snapshot,sort_keys=True,separators=(",", ":"),allow_nan=False).encode()).hexdigest()
                    if digest != inspection_sha256:
                        raise PermissionError("Recovery inspection differs from approved snapshot; UNKNOWN")
                    baseline = snapshot
                return references
            verify()
            if os.pread(self.journal.ledger_fd,1048577,0) != original:
                raise PermissionError("Recovery ledger changed before intent")
            receipt = {**group["base"],"container_id":expected["container_id"],"proxy_id":expected["proxy_id"],
                "networks":expected["networks"].copy(),"recovery_boot_id":self.boot_id,"recovery_ledger_sha256":ledger_sha256}
            if stopped:
                receipt.update(filter_outcome="UNKNOWN",recovery_inspection_sha256=inspection_sha256,
                    exit_codes={cid:v["State"]["ExitCode"] for cid,v in baseline["containers"].items()},
                    recovery_prior_sha256=hashlib.sha256(json.dumps(groups[:-1],sort_keys=True,separators=(",", ":")).encode()).hexdigest())
            self.journal.append({**receipt,"state":"RETIREMENT_RECOVERY_INTENT" if retirement else "STOPPED_RECOVERY_INTENT" if stopped else "UNSTARTED_RECOVERY_INTENT"})
            for nid in expected["networks"].values():
                references = verify()
                if nid in removed:
                    continue
                if stopped:
                    for cid in (expected["proxy_id"],expected["container_id"]):
                        if (cid,nid) in references:
                            verify()
                            self.connection.request("POST","/networks/"+nid+"/disconnect",boot_id=self.boot_id,
                                body={"Container":cid,"Force":True})
                            detached.add((cid,nid))
                            verify()
                self.connection.request("DELETE","/networks/"+nid,boot_id=self.boot_id)
                removed.add(nid)
                verify()
            receipt["exit_codes"] = ({cid:v["State"]["ExitCode"] for cid,v in baseline["containers"].items()} if stopped
                else {expected["container_id"]:0, expected["proxy_id"]:0})
            self.journal.append({**receipt,"state":"CLOSED_VERIFIED"})
            return {**receipt,"state":"CLOSED_VERIFIED","containers_retained":True,"effects":"UNKNOWN","descendants":"UNKNOWN"}
        finally:
            import sys
            pending = sys.exception()
            try:
                self.journal.close()
            except BaseException:
                if pending is None: raise
                pending.add_note("Recovery journal close failed; resources remain UNKNOWN")

    def _check_agent_preparation(self):
        if getattr(self,"_agent_candidate",False) and self._revoked_event.is_set():
            raise PermissionError("Agent preparation revoked")

    def _group_exits(self, group, *, preparing=False):
        if preparing:self._check_agent_preparation()
        bound = group["base"]
        image = self.connection.request("GET", "/images/"+bound["image_digest"]+"/json", boot_id=self.boot_id)["body"]
        labels = {**_verified_image_labels(image, bound["image_digest"]),
                  "curis.reader.work":bound["work"], "curis.reader.nonce":bound["nonce"]}
        exits = {}
        for cid in filter(None, (group["proxy_id"], group["container_id"])):
            if preparing:self._check_agent_preparation()
            info = self.connection.request("GET", "/containers/"+cid+"/json", boot_id=self.boot_id)["body"]
            expected = {**labels, "curis.reader.role":"proxy"} if cid == group["proxy_id"] else labels
            status = info.get("State", {})
            if (info.get("Id") != cid or info.get("Image") != bound["image_digest"]
                    or info.get("Config", {}).get("Labels") != expected
                    or status.get("Running") is not False or status.get("Restarting") is not False
                    or type(status.get("Pid")) is not int or status["Pid"] != 0
                    or info.get("HostConfig", {}).get("RestartPolicy", {}).get("Name") != "no"
                    or type(status.get("ExitCode")) is not int):
                raise PermissionError("Prior owned container exit is unproven")
            exits[cid] = status["ExitCode"]  # 137 remains forced, never called graceful.
        return exits

    def _verify_prior_holds(self, nonce):
        """Reverify terminal generations; persist a new-boot audit before allocating this Work."""
        groups = self._history_groups(nonce,recovery=True)
        self._check_agent_preparation()
        for group in groups:
            if (not group["container_id"] or group["state"] not in {"STOP_RETURNED", "CLOSED_VERIFIED"}
                    or (group["filter_state"] == "INTENT" and not (group["state"]=="CLOSED_VERIFIED"
                        and group.get("recovery_kind")=="stopped" and group.get("filter_outcome")=="UNKNOWN"))
                    or (group["networks"] and group["state"] != "CLOSED_VERIFIED")):
                raise PermissionError("Prior owner remains unresolved; no automatic retirement")
        for group in groups:
            exits = (self._group_exits(group,preparing=True) if getattr(self,"_agent_candidate",False)
                     else self._group_exits(group))
            if group["state"] == "CLOSED_VERIFIED":
                if group.get("exit_codes") != exits:
                    raise PermissionError("Prior terminal exit receipt changed")
                for nid in group["networks"].values():
                    self._check_agent_preparation()
                    if self.connection.request("GET", "/networks/"+nid, boot_id=self.boot_id)["status"] != 404:
                        raise PermissionError("Retired network absence is unproven")
            else:  # Legacy non-network container only; never remove retained networks.
                self.journal.append({**group["base"], "state":"CLOSED_VERIFIED",
                    "container_id":group["container_id"], "proxy_id":None, "exit_codes":exits})
        try:
            self._history_groups(nonce)
        except _HistoryBootChanged:
            import os, json
            # Revalidation above is read-only. Persist the audit before this Work allocates anything.
            fd = getattr(self.journal,"ledger_fd",None)
            if type(fd) is not int:raise PermissionError("Boot reconciliation requires the held durable ledger")
            raw = os.pread(fd,1048577,0)
            if _owner_records(raw) != self.journal.records:
                raise PermissionError("Closed history changed before boot audit")
            groups = self._history_groups(nonce,recovery=True)
            self._check_agent_preparation()
            self.journal.append({"state":"BOOT_CLOSURES_VERIFIED","boot_id":self.boot_id,
                "prior_ledger_sha256":hashlib.sha256(raw).hexdigest(),
                "history_sha256":hashlib.sha256(json.dumps(self.journal.records,sort_keys=True,separators=(",", ":")).encode()).hexdigest(),
                "closures_sha256":hashlib.sha256(json.dumps(groups,sort_keys=True,separators=(",", ":")).encode()).hexdigest()})
            self._history_groups(nonce)

    def _retire_current_networks(self):
        """Native Docker detach/remove only for this future-created, stopped generation."""
        groups = self._history_groups()
        if not groups:
            raise PermissionError("Current owner lacks durable intent")
        group = groups[-1]
        if (group["base"] != self._record or group["state"] != "STOP_RETURNED"
                or group["filter_state"] == "INTENT"
                or group["container_id"] != self.container_id or group["proxy_id"] != self.proxy_id
                or group["networks"] != {k:v for k,v in (("private",self.private_network),("external",self.external_network)) if v}):
            raise PermissionError("Current owner generation is incomplete")
        exits = self._group_exits(group)
        receipt = {**self._record, "container_id":self.container_id,"proxy_id":self.proxy_id,"exit_codes":exits}
        if group["networks"]:
            if (self._record.get("network_retirement") != "OWNED_NETWORK_RETIRE_V1"
                    or set(group["networks"]) != {"private","external"} or not self.proxy_id):
                raise PermissionError("Network removal is not authorized for retained history")
            receipt["networks"] = group["networks"].copy()
            # Verify both networks and all attachments before recording any destructive intent.
            for role,nid in group["networks"].items():
                self._retirement_network(group, role, nid)
            self._retirement_attachments(group)
            self.journal.append({**receipt,"state":"NETWORK_RETIRE_INTENT"})
            for role,nid in group["networks"].items():
                targets = [self.proxy_id, self.container_id] if role == "private" else [self.proxy_id]
                for cid in targets:
                    self._group_exits(group)
                    self._retirement_network(group, role, nid)
                    attached = self._retirement_attachments(group)
                    if nid in attached[cid]:
                        # Docker forced detach is needed for stopped endpoints; never force an unknown target.
                        self.connection.request("POST", "/networks/"+nid+"/disconnect", boot_id=self.boot_id,
                                                body={"Container":cid,"Force":True})
                        if nid in self._retirement_attachments(group)[cid]:
                            raise PermissionError("Original endpoint detach is unconfirmed")
                self._group_exits(group)
                network = self._retirement_network(group, role, nid)
                if network["Containers"] or any(nid in nets for nets in self._retirement_attachments(group).values()):
                    raise PermissionError("Original network is not empty")
                self.connection.request("DELETE", "/networks/"+nid, boot_id=self.boot_id)
                if self.connection.request("GET", "/networks/"+nid, boot_id=self.boot_id)["status"] != 404:
                    raise PermissionError("Original network removal is unconfirmed")
            self.journal.append({**receipt,"state":"NETWORKS_RETIRED"})
        self.journal.append({**receipt,"state":"CLOSED_VERIFIED"})

    def _retirement_network(self, group, role, nid):
        info = self.connection.request("GET", "/networks/"+nid, boot_id=self.boot_id)["body"]
        bound = group["base"]
        labels = {"curis.reader.work":bound["work"],"curis.reader.nonce":bound["nonce"]}
        allowed = {self.proxy_id,self.container_id} if role == "private" else {self.proxy_id}
        if (info.get("Id") != nid or info.get("Name") != "curis-reader-"+bound["nonce"]+"-"+role
                or info.get("Labels") != labels or info.get("Driver") != "bridge"
                or info.get("Internal") is not (role == "private") or info.get("EnableIPv6") is not False
                or type(info.get("Containers")) is not dict or not set(info["Containers"]).issubset(allowed)):
            raise PermissionError("Original network has foreign or changed endpoints")
        return info

    def _retirement_attachments(self, group):
        names = {"curis-reader-"+self.nonce+"-"+role:nid for role,nid in group["networks"].items()}
        result = {}
        self._group_exits(group)
        for cid in (self.proxy_id,self.container_id):
            info = self.connection.request("GET", "/containers/"+cid+"/json", boot_id=self.boot_id)["body"]
            endpoints = info.get("NetworkSettings", {}).get("Networks")
            allowed = set(group["networks"].values()) if cid == self.proxy_id else {self.private_network}
            if type(endpoints) is not dict:
                raise PermissionError("Stopped container attachments are unavailable")
            attached = set()
            for name,endpoint in endpoints.items():
                nid = names.get(name, name if name in group["networks"].values() else None)
                private,external = self._network_prefixes()
                address = private+".3" if cid == self.container_id else private+".2" if nid == self.private_network else external+".2"
                if nid in allowed and _empty_created_endpoint(info, endpoint, address):
                    continue
                if (nid not in allowed or type(endpoint) is not dict
                        or endpoint.get("NetworkID") != nid or nid in attached):
                    raise PermissionError("Stopped container has a foreign attachment")
                attached.add(nid)
            result[cid] = attached
        return result

    def _network_prefixes(self):
        return ("172.30.251", "172.30.252") if getattr(self,"_paired_provider",False) else ("172.30.253", "172.30.254")

    def _create_networks(self):
        import re
        from contextlib import nullcontext
        labels={"curis.reader.work":self._record["work"],"curis.reader.nonce":self.nonce}
        private,external = self._network_prefixes()
        for role,subnet,internal in [("private",private+".0/29",True),("external",external+".0/29",False)]:
            options={"com.docker.network.bridge.enable_icc":"true" if internal else "false",
                     "com.docker.network.bridge.gateway_mode_ipv4":"isolated" if internal else "nat"}
            spec={"Name":"curis-reader-"+self.nonce+"-"+role,"Driver":"bridge","Internal":internal,
                  "EnableIPv6":False,"Attachable":False,"Labels":labels,"Options":options,
                  "IPAM":{"Driver":"default","Config":[{"Subnet":subnet}]}}
            with self._state_lock if getattr(self,"_agent_candidate",False) else nullcontext():
                if getattr(self,"_agent_candidate",False) and (self.revoked or self._revoked_event.is_set()):
                    raise PermissionError("Agent network allocation revoked")
                result=self.connection.request("POST","/networks/create",boot_id=self.boot_id,body=spec)["body"]
                if type(result) is not dict or not re.fullmatch(r"[0-9a-f]{64}",str(result.get("Id",""))):
                    raise PermissionError("Network create UNKNOWN; never adopt or retry")
                setattr(self,role+"_network",result["Id"])
                self.journal.append({**self._record,"state":"NETWORK","role":role,"network_id":result["Id"]})

    def _topology(self):
        network_info={}
        private,external = self._network_prefixes()
        for role,internal,subnet in [("private",True,private+".0/29"),("external",False,external+".0/29")]:
            nid=getattr(self,role+"_network")
            info=self.connection.request("GET","/networks/"+nid,boot_id=self.boot_id)["body"]
            if (info.get("Id")!=nid or info.get("Name")!="curis-reader-"+self.nonce+"-"+role
                    or info.get("Driver")!="bridge" or info.get("Internal") is not internal or info.get("EnableIPv6") is not False
                    or info.get("Labels")!={"curis.reader.work":self._record["work"],"curis.reader.nonce":self.nonce}
                    or [row.get("Subnet") for row in info.get("IPAM",{}).get("Config",[])]!=[subnet]
                    or info.get("Options",{}).get("com.docker.network.bridge.gateway_mode_ipv4")!=("isolated" if internal else "nat")
                    or info.get("Options",{}).get("com.docker.network.bridge.enable_icc")!=("true" if internal else "false")):
                raise PermissionError("Original private network topology changed")
            network_info[nid]=info
        active={nid:set() for nid in network_info}
        for cid,role,addresses in [(self.container_id,"browser",{self.private_network:private+".3"}),
                (self.proxy_id,"proxy",{self.private_network:private+".2",self.external_network:external+".2"})]:
            info=self.connection.request("GET","/containers/"+cid+"/json",boot_id=self.boot_id)["body"]
            labels={**self._image_labels,"curis.reader.work":self._record["work"],"curis.reader.nonce":self.nonce}
            if role=="proxy": labels["curis.reader.role"]="proxy"
            cfg=info.get("HostConfig",{})
            security=cfg.get("SecurityOpt",[])
            endpoints=info.get("NetworkSettings",{}).get("Networks",{})
            running=info.get("State",{}).get("Running")
            configured={}
            for name,endpoint in endpoints.items():
                matches=[nid for nid,net in network_info.items() if name in (nid,net["Name"])]
                if len(matches)!=1: raise PermissionError("Foreign container network attachment")
                nid=matches[0]
                configured[nid]=endpoint.get("IPAMConfig",{}).get("IPv4Address")
                if running is True:
                    if endpoint.get("NetworkID")!=nid or endpoint.get("IPAddress")!=addresses.get(nid):
                        raise PermissionError("Active container network identity mismatch")
                    active[nid].add(cid)
            if (info.get("Id")!=cid or info.get("Image")!=self.image_digest or info.get("Config",{}).get("Labels")!=labels
                    or info.get("Config",{}).get("User")!="pwuser" or cfg.get("ReadonlyRootfs") is not True
                    or cfg.get("Privileged") is not False or cfg.get("CapDrop")!=["ALL"] or cfg.get("CapAdd")
                    or cfg.get("Binds") or cfg.get("PortBindings") or cfg.get("PublishAllPorts") or cfg.get("PidMode")
                    or cfg.get("IpcMode")!="private" or cfg.get("NetworkMode")!=self.private_network
                    or not any(x in security for x in ("no-new-privileges","no-new-privileges=true"))
                    or "seccomp="+self._seccomp_profile not in security or configured!=addresses or type(running) is not bool
                    or cfg.get("Dns")!=(["127.0.0.1"] if role=="browser" else ["1.1.1.1"])
                    or cfg.get("Sysctls")!={"net.ipv6.conf.all.disable_ipv6":"1","net.ipv6.conf.default.disable_ipv6":"1"}
                    or cfg.get("Memory")!=1610612736 or cfg.get("PidsLimit")!=192 or cfg.get("NanoCpus")!=1000000000
                    or any(m.get("Type")!="tmpfs" or m.get("Destination")!="/tmp" for m in info.get("Mounts",[]))):
                raise PermissionError("Original container isolation configuration changed")
        for nid,info in network_info.items():
            if set(info.get("Containers",{}))!=active[nid]:
                raise PermissionError("Foreign or missing active network endpoint")

    def start_runtime(self):
        import re
        with self._state_lock:
            if self.revoked or getattr(self,"_runtime_start_attempted",False) or not self.proxy_id or not self.container_id:
                raise PermissionError("Original private runtime cannot start")
            self._runtime_start_attempted=True
        try:
            self._topology()
            self.journal.append({**self._record,"state":"START_INTENT","container_id":self.container_id,"proxy_id":self.proxy_id})
            proxy=self._attach_owned(self.proxy_id)
            self._start_owned(self.proxy_id)
            self._topology()
            proxy_runtime={"boot_id":self.boot_id,"container_id":self.proxy_id,"image_digest":self.image_digest}
            ack=proxy.request({"identity":self.identity.copy(),"nonce":self.nonce,"runtime":proxy_runtime,"hosts":self.hosts})
            expected={"identity":self.identity.copy(),"nonce":self.nonce,"sequence":0,**proxy_runtime}
            if (any(ack.get(k)!=v for k,v in expected.items()) or type(ack.get("result")) is not dict
                    or ack["result"].get("proxy_ready") is not True
                    or not re.fullmatch(r"[A-Za-z0-9+/]{43}=",str(ack["result"].get("proxy_spki","")))):
                raise PermissionError("Original Work proxy TLS bootstrap failed")
            browser=self._attach_owned(self.container_id)
            self._start_owned(self.container_id)
            self._topology()
            runtime={"boot_id":self.boot_id,"container_id":self.container_id,"image_digest":self.image_digest}
            ready=browser.request({"identity":self.identity.copy(),"nonce":self.nonce,"runtime":runtime,"hosts":self.hosts,
                                   "proxy_spki":ack["result"]["proxy_spki"]})
            if ready!={"identity":self.identity.copy(),"nonce":self.nonce,"sequence":0,**runtime,
                       "result":{"bootstrapped":True,"browser_started":False}}:
                raise PermissionError("Original Reader bootstrap failed")
            self._install_netns_filter()
            self._topology()
            with self._state_lock:
                if self.revoked or self._revoked_event.is_set(): raise PermissionError("Original runtime revoked during startup")
                self._channel,self._ready,self._owner_sequence=browser,True,0
            self.journal.append({**self._record,"state":"ATTACHED","container_id":self.container_id,"proxy_id":self.proxy_id})
            return browser
        except BaseException as error:
            self._revoked_event.set()
            with self._state_lock: self.revoked=True
            try:
                self.revoke_bound_and_stop(self.identity.copy(),self.nonce,{"complete":False,"executionAuthorized":False,
                    "boot_id":self.boot_id,"container_id":self.container_id,"image_digest":self.image_digest})
            except BaseException: error.add_note("Original runtime cleanup UNKNOWN; no retry or reuse")
            raise

    def _filter_binding(self):
        return _netns_binding({**{key:self._record[key] for key in ("boot_id","image_digest","work","nonce")},
            "container_id":self.container_id,"network_id":self.private_network})

    def _install_netns_filter(self):
        with self._state_lock:
            if self.revoked or self._revoked_event.is_set() or self._filter_install_attempted:
                raise PermissionError("Original filter installation cannot be repeated")
            self._filter_install_attempted = True
        self.journal.append({**self._record,"state":"NETNS_FILTER_INTENT",
            "container_id":self.container_id,"proxy_id":self.proxy_id})
        paired = getattr(self,"_paired_provider",False)
        options = {"paired":True} if paired else {}
        receipt = _netns_receipt(self._filter_binding(),
            self.connection.browser_filter("install",self._filter_binding(),**options),paired=paired)
        if self._revoked_event.is_set():
            raise PermissionError("Original filter completed after revocation; outcome UNKNOWN")
        self.journal.append({**self._record,"state":"NETNS_FILTER_VERIFIED",
            "container_id":self.container_id,"proxy_id":self.proxy_id,"filter":receipt})
        self._filter_snapshot = receipt

    def _verify_netns_filter(self):
        if self._filter_snapshot is None or self._revoked_event.is_set():
            raise PermissionError("Original browser has no verified netns filter")
        paired = getattr(self,"_paired_provider",False)
        options = {"paired":True} if paired else {}
        expected = _netns_receipt(self._filter_binding(),self._filter_snapshot,paired=paired)
        receipt = self.connection.browser_filter("verify",self._filter_binding(),expected=expected,**options)
        if _netns_receipt(self._filter_binding(),receipt,paired=paired) != expected:
            raise PermissionError("Original browser filter generation changed")

    def _attach_owned(self, cid):
        if not cid or cid not in (self.container_id,self.proxy_id) or self._revoked_event.is_set():
            raise PermissionError("Attach is outside the original owned resources")
        channel=_DockerAttachChannel(cid,self.boot_id)
        with self._state_lock:
            revoked=self.revoked or self._revoked_event.is_set()
            if not revoked: self.channels.append(channel)
        if revoked:
            channel.close()
            raise PermissionError("Original attach completed after revocation")
        return channel

    def _verify_provider_proxy(self, *, running):
        value=self.connection.request("GET","/containers/"+self.proxy_id+"/json",boot_id=self.boot_id)["body"]
        config=value.get("Config",{});spec=self._provider_proxy_config
        expected=dict(item.split("=",1) for item in self._agent_image_env+spec["Env"])
        env=config.get("Env");state=value.get("State",{});restart=value.get("HostConfig",{}).get("RestartPolicy")
        if (any(config.get(k)!=spec[k] for k in ("Entrypoint","Cmd","User","OpenStdin","StdinOnce","Tty","WorkingDir"))
                or type(env) is not list or any(type(x) is not str or "=" not in x for x in env)
                or len({x.split("=",1)[0] for x in env})!=len(env)
                or dict(x.split("=",1) for x in env)!=expected
                or type(restart) is not dict or set(restart)-{"Name","MaximumRetryCount"}
                or restart.get("Name")!="no" or type(restart.get("MaximumRetryCount",0)) is not int
                or restart.get("MaximumRetryCount",0)!=0
                or state.get("Running") is not running or state.get("Restarting") is not False
                or type(state.get("Pid")) is not int or (state["Pid"]<=0 if running else state["Pid"]!=0)):
            raise PermissionError("Original provider proxy command or state changed")

    def _verify_agent_container(self, *, running):
        info=self._inspect()
        spec=getattr(self,"_agent_config",None)
        def reject(code):
            error=PermissionError("Agent isolation rejected: "+code+"; UNKNOWN")
            error.agent_code=code
            raise error
        provider=getattr(self,"_provider_mode",False)
        if spec is None or (not provider and (self.private_network or self.proxy_id)):reject("SCOPE")
        if provider:
            if not self.private_network or not self.proxy_id:reject("SCOPE")
            self._topology()
            self._verify_provider_proxy(running=running)
        config,host=info.get("Config",{}),info.get("HostConfig",{})
        networks=info.get("NetworkSettings",{}).get("Networks")
        expected=dict(item.split("=",1) for item in self._agent_image_env+spec["Env"])
        env=config.get("Env")
        valid_env=(type(env) is list and all(type(x) is str and "=" in x for x in env)
            and len({x.split("=",1)[0] for x in env})==len(env)
            and dict(x.split("=",1) for x in env)==expected)
        if not valid_env:reject("ENV")
        if (config.get("Entrypoint")!=spec["Entrypoint"] or config.get("Cmd")!=spec["Cmd"]
                or config.get("User")!="pwuser" or config.get("WorkingDir")!="/tmp"
                or config.get("StdinOnce") is not True or config.get("OpenStdin") is not True
                or config.get("Tty") is not False or config.get("Hostname")!=self.container_id[:12]):reject("PROCESS_CONFIG")
        if (host.get("ReadonlyRootfs") is not True or host.get("Privileged") is not False
                or host.get("CapDrop")!=["ALL"] or host.get("CapAdd")):reject("CAPABILITIES")
        if any(host.get(k) for k in ("Binds","PortBindings","PublishAllPorts","PidMode","UTSMode",
                "UsernsMode","Devices","DeviceRequests","DeviceCgroupRules","VolumesFrom")):reject("HOST_EXPOSURE")
        if provider:
            security=host.get("SecurityOpt")
            if (host.get("NetworkMode")!=self.private_network or host.get("IpcMode")!="private"
                    or type(security) is not list or len(security)!=2
                    or set(security) not in ({"no-new-privileges","seccomp="+self._seccomp_profile},
                                            {"no-new-privileges=true","seccomp="+self._seccomp_profile})):
                reject("NETWORK")
        else:
            if (host.get("NetworkMode")!="none" or host.get("IpcMode")!="private"
                    or type(networks) is not dict or set(networks)-{"none"}
                    or any(type(v) is not dict or v.get("IPAddress") or v.get("GlobalIPv6Address") for v in networks.values())):reject("NETWORK")
            if host.get("SecurityOpt") not in (["no-new-privileges"],["no-new-privileges=true"]):reject("SECURITY_OPT")
        for key in ("Tmpfs","Memory","PidsLimit","NanoCpus","ShmSize","LogConfig"):
            if host.get(key)!=spec["HostConfig"][key]:reject("RESOURCE_"+key.upper())
        restart=host.get("RestartPolicy")
        # Docker inspect includes its explicit zero retry default; still forbid every restart policy.
        if (type(restart) is not dict or set(restart)-{"Name","MaximumRetryCount"}
                or restart.get("Name")!="no" or type(restart.get("MaximumRetryCount",0)) is not int
                or restart.get("MaximumRetryCount",0)!=0):reject("RESTART_POLICY")
        mounts=info.get("Mounts")
        if (type(mounts) is not list or any(type(m) is not dict or m.get("Type")!="tmpfs"
                or m.get("Destination")!="/tmp" for m in mounts)):reject("MOUNTS")
        state=info.get("State",{})
        if (state.get("Running") is not running or state.get("Restarting") is not False
                or type(state.get("Pid")) is not int or (state["Pid"]<=0 if running else state["Pid"]!=0)):reject("PROCESS_STATE")
        if provider and running and self._filter_snapshot is not None:self._verify_netns_filter()
        return info

    def start_agent_runtime(self):
        self._verify_agent_container(running=False)
        with self._state_lock:
            if self.revoked or self._revoked_event.is_set():raise PermissionError("Agent start revoked")
            self.journal.append({**self._record,"state":"START_INTENT","container_id":self.container_id,"proxy_id":self.proxy_id})
        if getattr(self,"_provider_mode",False):
            proxy=_DockerAttachChannel(self.proxy_id,self.boot_id,timeout_seconds=80)
            with self._state_lock:
                if self.revoked or self._revoked_event.is_set():
                    proxy.close();raise PermissionError("Provider proxy attach revoked")
                self.channels.append(proxy)
            self._start_owned(self.proxy_id)
            self._topology()
            runtime={"boot_id":self.boot_id,"container_id":self.proxy_id,"image_digest":self.image_digest}
            ack=proxy.request({"identity":self.identity.copy(),"nonce":self.nonce,"runtime":runtime,"hosts":self.hosts})
            if ack!={"identity":self.identity.copy(),"nonce":self.nonce,"sequence":0,**runtime,
                    "result":{"proxy_ready":True,"purpose":"CODEX_PROVIDER_CONNECT_V1"}}:
                raise PermissionError("Original provider proxy bootstrap changed")
        channel=_DockerAttachChannel(self.container_id,self.boot_id,timeout_seconds=80)
        with self._state_lock:
            if self.revoked or self._revoked_event.is_set():
                channel.close()
                raise PermissionError("Agent attach revoked")
            self.channels.append(channel)
        self._start_owned(self.container_id)
        if getattr(self,"_provider_mode",False):
            self._topology();self._install_netns_filter();self._topology()
        arguments=getattr(self,"_linux_bootstrap",None) or {}
        try:
            ready=channel.request(self.agent_frame(0,"bootstrap",arguments))
        finally:
            arguments.pop("auth_cache",None)
        expected={k:v for k,v in self.agent_frame(0,"bootstrap",arguments).items() if k not in {"action","arguments"}}
        if arguments:
            if (type(ready) is not dict or type(ready.get("result")) is not dict
                    or ready["result"].get("ready") is not True or type(ready["result"].get("authenticated")) is not bool):
                raise PermissionError("Original Linux authentication acknowledgement changed")
            result={"ready":True,"resource_sha256":arguments["resources"]["sha256"],
                    "binary_sha256":"57a159f67999794494a172e71c12c6b5a211542ea90c66ea2ce9e6ac1edec6b1",
                    "authenticated":True}
            self._linux_authenticated=ready=={**expected,"result":result}
            if ready=={**expected,"result":{**result,"authenticated":False}}:
                result["authenticated"]=False
        else:result={"ready":True,"network":"none","credentials":False}
        if ready!={**expected,"result":result}:
            raise PermissionError("Agent bootstrap binding changed")
        self._verify_agent_container(running=True)
        with self._state_lock:
            if self.revoked or self._revoked_event.is_set():raise PermissionError("Agent bootstrap revoked")
            self.journal.append({**self._record,"state":"ATTACHED","container_id":self.container_id,"proxy_id":self.proxy_id})
        return channel

    def agent_frame(self, sequence, action, arguments):
        return {"identity":self.identity.copy(),"nonce":self.nonce,"boot_id":self.boot_id,
            "container_id":self.container_id,"image_digest":self.image_digest,
            "sequence":sequence,"action":action,"arguments":arguments}

    def _start_owned(self, cid):
        # Stop sets the event immediately, then waits behind this bounded submit.
        # Docker stop can therefore never complete before an admitted late start.
        with self._state_lock:
            if not cid or cid not in (self.container_id,self.proxy_id) or self.revoked or self._revoked_event.is_set():
                raise PermissionError("Original start revoked or target unowned")
            self.connection.request("POST","/containers/"+cid+"/start",boot_id=self.boot_id)

    def bind_session(self, identity, nonce, snapshot):
        if (identity!=self.identity or nonce!=self.nonce or not getattr(self,"_ready",False) or self.revoked or self._revoked_event.is_set()
                or any(snapshot.get(k)!=getattr(self,k) for k in ("boot_id","container_id","image_digest"))):
            raise PermissionError("Original runtime session mismatch")
        return self._channel

    def dispatch_if_active(self, identity, transport, frame):
        if not self._admission_lock.acquire(blocking=False): raise PermissionError("Original request already admitted")
        try:
            with self._state_lock:
                if (self.revoked or self._revoked_event.is_set() or not getattr(self,"_ready",False) or identity!=self.identity or transport is not self._channel
                        or frame.get("identity")!=self.identity or frame.get("nonce")!=self.nonce
                        or any(frame.get(k)!=getattr(self,k) for k in ("boot_id","container_id","image_digest"))
                        or type(frame.get("sequence")) is not int or frame["sequence"]!=self._owner_sequence+1):
                    raise PermissionError("Original request revoked or binding changed")
                self._owner_sequence=frame["sequence"]
            try:
                self._verify_netns_filter()
                if self._revoked_event.is_set():
                    raise PermissionError("Original request revoked during filter verification")
                result=transport.request(frame)
                self._verify_netns_filter()
            except BaseException:
                self._revoked_event.set()
                with self._state_lock: self.revoked=True
                raise
            with self._state_lock:
                if self.revoked or self._revoked_event.is_set(): raise PermissionError("Original response arrived after revocation")
            return result
        finally:
            self._admission_lock.release()

    def _inspect(self, *, seconds=5):
        if not self.container_id:
            raise PermissionError("No exact owned container")
        value = self.connection.request("GET", "/containers/"+self.container_id+"/json", boot_id=self.boot_id, seconds=seconds)["body"]
        if (type(value) is not dict or value.get("Id") != self.container_id or value.get("Image") != self.image_digest
                or value.get("Config", {}).get("Labels") != {**self._image_labels,"curis.reader.work":self._record["work"],"curis.reader.nonce":self.nonce}
                or value.get("HostConfig", {}).get("NetworkMode") != (self.private_network or "none")):
            raise PermissionError("Original Docker container binding changed; retain UNKNOWN")
        return value

    def verified_snapshot(self, identity):
        if identity != self.identity:
            raise PermissionError("Original Work mismatch")
        if _released_vm_image() != self.image_digest:
            raise PermissionError("Original Reader image is not released")
        with self._state_lock:
            if (self.revoked or self._revoked_event.is_set() or not getattr(self, "_ready", False)
                    or self.stop_requested or not self.container_id or not self.proxy_id):
                raise PermissionError("Original Reader runtime is not active")
        self._topology()
        self._verify_netns_filter()
        for cid in (self.proxy_id, self.container_id):
            value = self.connection.request("GET", "/containers/"+cid+"/json", boot_id=self.boot_id)["body"]
            state, config = value.get("State", {}), value.get("HostConfig", {})
            labels = {**self._image_labels, "curis.reader.work": self._record["work"],
                      "curis.reader.nonce": self.nonce}
            if cid == self.proxy_id:
                labels["curis.reader.role"] = "proxy"
            if (value.get("Id") != cid or value.get("Image") != self.image_digest
                    or value.get("Config", {}).get("Labels") != labels
                    or state.get("Running") is not True or state.get("Restarting") is not False
                    or state.get("Status") != "running" or type(state.get("Pid")) is not int or state["Pid"] <= 0
                    or config.get("RestartPolicy", {}).get("Name") != "no"):
                raise PermissionError("Original running container binding changed")
        with self._state_lock:
            if self.revoked or self._revoked_event.is_set() or self.stop_requested:
                raise PermissionError("Original Reader revoked during verification")
        return {"complete": True, "executionAuthorized": True,
                "boot_id": self.boot_id, "container_id": self.container_id, "image_digest": self.image_digest}

    def revoke_bound_and_stop(self, identity, nonce, snapshot):
        expected = {"boot_id":self.boot_id,"container_id":self.container_id,"image_digest":self.image_digest}
        if (identity != self.identity or nonce != self.nonce or type(snapshot) is not dict or not (self.container_id or self.proxy_id)
                or set(snapshot) != {"complete", "executionAuthorized", *expected}
                or any(snapshot[k] != v for k,v in expected.items())
                or any(type(snapshot[k]) is not bool for k in ("complete", "executionAuthorized"))):
            raise PermissionError("Stop does not own the original container generation")
        self._revoked_event.set()
        with self._state_lock:
            if self.stop_requested:
                raise PermissionError("Original stop already requested; no automatic retry")
            self.revoked, self.stop_requested = True, True
        try:
            errors=[]
            try:
                self.journal.append({**self._record,"state":"REVOKING","container_id":self.container_id,"proxy_id":self.proxy_id})
            except BaseException as error:
                errors.append(error)  # Durable INTENT already forbids reuse; still stop original handles.
            for channel in self.channels:
                try: channel.close()
                except BaseException as error:
                    try:
                        settled = callable(getattr(channel,"wait_closed",None)) and channel.wait_closed(1)
                    except BaseException as wait_error:
                        errors.append(wait_error)
                        settled = False
                    if not settled:errors.append(error)
            # Stop the egress proxy first, then the browser; never let one failure
            # silently skip the other original resource or discover replacement IDs.
            # Each original target has independent bounded inspect/stop/verify calls
            # (1/2/1 seconds); proxy latency cannot consume the browser's stop budget.
            for cid in [value for value in (self.proxy_id,self.container_id) if value]:
                try:
                    info=self.connection.request("GET","/containers/"+cid+"/json",boot_id=self.boot_id,
                                                 seconds=1)["body"]
                    labels={**self._image_labels,"curis.reader.work":self._record["work"],"curis.reader.nonce":self.nonce}
                    if cid==self.proxy_id: labels["curis.reader.role"]="proxy"
                    if info.get("Id")!=cid or info.get("Image")!=self.image_digest or info.get("Config",{}).get("Labels")!=labels:
                        raise PermissionError("Original stop target changed; retain UNKNOWN")
                    self.connection.request("POST","/containers/"+cid+"/stop?t=1",boot_id=self.boot_id,
                                            seconds=2)
                    value=self.connection.request("GET","/containers/"+cid+"/json",boot_id=self.boot_id,
                                            seconds=1)["body"]
                    state=value.get("State",{})
                    if (value.get("Id")!=cid or value.get("Image")!=self.image_digest or state.get("Running") is not False
                            or state.get("Restarting") is not False or state.get("Pid")!=0):
                        raise PermissionError("Docker container exit unconfirmed; retain UNKNOWN")
                except BaseException as error: errors.append(error)
            if errors:
                interruption=next((error for error in errors if not isinstance(error,Exception)),None)
                if interruption is not None: raise interruption
                raise RuntimeError("Original container stop incomplete; resources remain UNKNOWN") from errors[0]
            self.journal.append({**self._record,"state":"STOP_RETURNED","container_id":self.container_id,"proxy_id":self.proxy_id})
            self._retire_current_networks()
            self.stop_receipt={"identity":self.identity.copy(),"nonce":self.nonce,"boot_id":self.boot_id,
                "image_digest":self.image_digest,"container_id":self.container_id,"proxy_id":self.proxy_id,
                "ledger_state":self.journal.records[-1]["state"],"exit_codes":self.journal.records[-1]["exit_codes"],
                "effects":"UNKNOWN","descendants":"UNKNOWN"}
            return {"container":"STOP_RETURNED","exit_codes":self.journal.records[-1]["exit_codes"],
                    "descendants":"UNKNOWN","effects":"UNKNOWN"}
        finally:
            import sys
            pending = sys.exception()
            try:
                self.journal.close()
            except BaseException:
                if pending is None:
                    raise
                pending.add_note("Owner journal close failed; resource state remains UNKNOWN")
            finally:
                self._stop_done.set()


_DOCKER_ATTACH_SOURCE = r"""
import json, os, re, select, socket, struct, sys, time
from pathlib import Path
request = json.loads(sys.stdin.buffer.readline(4097))
assert set(request) == {'container_id','boot_id'}
cid = request['container_id']
assert re.fullmatch('[0-9a-f]{64}', cid)
boot = Path('/proc/sys/kernel/random/boot_id').read_text().strip()
assert request['boot_id'] == boot
channel = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
channel.settimeout(3)
channel.connect('/var/run/docker.sock')
channel.sendall(('POST /v1.53/containers/'+cid+'/attach?stream=1&stdin=1&stdout=1&stderr=0 HTTP/1.1\r\nHost: docker\r\nConnection: Upgrade\r\nUpgrade: tcp\r\nContent-Length: 0\r\n\r\n').encode())
header = bytearray()
header_deadline = time.monotonic()+3
while not header.endswith(b'\r\n\r\n'):
    budget=header_deadline-time.monotonic()
    assert budget>0
    channel.settimeout(budget)
    part = channel.recv(1)
    assert part and len(header)<8192
    header.extend(part)
assert bytes(header).split(b'\r\n',1)[0] in (b'HTTP/1.1 101 UPGRADED', b'HTTP/1.1 101 Switching Protocols', b'HTTP/1.1 200 OK')
sys.stdout.write(json.dumps({'boot_id':boot,'container_id':cid,'result':{'attached':True}})+'\n')
sys.stdout.flush()
for fd in (sys.stdin.fileno(), sys.stdout.fileno()): os.set_blocking(fd, False)
channel.setblocking(False)
wire, outgoing, incoming = bytearray(), bytearray(), bytearray()
remaining = 0
deadline = time.monotonic()+90
try:
    while time.monotonic()<deadline:
        readers = ([channel] if len(incoming)<16777216 else []) + ([sys.stdin.fileno()] if len(outgoing)<262144 else [])
        writers = ([channel] if outgoing else []) + ([sys.stdout.fileno()] if incoming else [])
        ready, writable, _ = select.select(readers, writers, [], min(.05,max(0,deadline-time.monotonic())))
        if sys.stdin.fileno() in ready:
            try: data = os.read(sys.stdin.fileno(),65536)
            except BlockingIOError: continue
            if not data: break
            outgoing.extend(data)
        if channel in writable:
            try: count=channel.send(outgoing)
            except BlockingIOError: count=0
            del outgoing[:count]
        if channel in ready:
            try: data=channel.recv(65536)
            except BlockingIOError: continue
            if not data: break
            wire.extend(data)
            while wire:
                if not remaining:
                    if len(wire)<8: break
                    assert wire[0]==1 and wire[1:4]==bytes(3)
                    remaining=struct.unpack('>I',wire[4:8])[0]
                    del wire[:8]
                    assert 0<=remaining<=16777216
                count=min(remaining,len(wire))
                incoming.extend(wire[:count]); del wire[:count]; remaining-=count
                assert len(incoming)<=16842752
        if sys.stdout.fileno() in writable:
            try: count=os.write(sys.stdout.fileno(),incoming)
            except BlockingIOError: count=0
            del incoming[:count]
finally:
    channel.close()
"""


class _DockerAttachChannel:
    """Reuse existing bounded Reader pipes; Docker stdcopy is decoded remotely."""
    def __init__(self, container_id, boot_id, *, timeout_seconds=_READER_ATTACH_TIMEOUT_SECONDS):
        import json, os, re, shlex, subprocess
        if (type(timeout_seconds) not in (int,float) or not 0<timeout_seconds<=80
                or type(container_id) is not str or not re.fullmatch(r"[0-9a-f]{64}",container_id)
                or type(boot_id) is not str or not re.fullmatch(r"[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}",boot_id)):
            raise PermissionError("Original attach identity invalid")
        from .agent_browser_runtime import BoundedPipeTransport
        directory, fds, self.process, self.pipe = _owner_directory(), [], None, None
        self.closed = False
        self._close_lock = threading.Lock()
        self._close_pending = self._close_failure = False
        self._close_done = threading.Event()
        try:
            for name in ("reader-owner-ssh.config", _OWNER_KNOWN_HOSTS):
                fds.append(_owner_file(directory,name,os.O_RDONLY))
            texts=[os.read(fd,65537).decode("ascii") for fd in fds]
            if any(len(text)>65536 for text in texts): raise PermissionError("Owner SSH inputs oversized")
            _ssh_owner_inputs(*texts)
            for fd in fds: os.lseek(fd,0,os.SEEK_SET)
            public_before=_ssh_public_snapshot(tuple(fds))
            argv=_ssh_owner_argv(*fds)
            argv[-1]="/usr/bin/python3 -I -B -c "+shlex.quote(_DOCKER_ATTACH_SOURCE)
            if _ssh_public_snapshot(tuple(fds)) != public_before:
                raise PermissionError("Owner public enrollment changed before attach")
            self.process=subprocess.Popen(argv,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,
                cwd=_OWNER_ROOT,env={"PATH":"/usr/bin:/bin","LANG":"C.UTF-8","HOME":_OWNER_ROOT+"/home"},
                close_fds=True,pass_fds=())
            self.pipe=BoundedPipeTransport(self.process.stdout.fileno(),self.process.stdin.fileno(),
                alive=lambda:not self.closed and self.process.poll() is None,timeout=timeout_seconds)
            ack=self.pipe.request({"container_id":container_id,"boot_id":boot_id})
            if ack != {"boot_id":boot_id,"container_id":container_id,"result":{"attached":True}}:
                raise PermissionError("Original Docker attach channel mismatch")
            if _ssh_public_snapshot(tuple(fds)) != public_before:
                raise PermissionError("Owner public enrollment changed during attach; outcome UNKNOWN")
        except BaseException as error:
            try: self.close()
            except BaseException: error.add_note("Original attach cleanup failed; resources UNKNOWN")
            raise
        finally:
            for fd in fds: os.close(fd)
            os.close(directory)

    def request(self, frame):
        if self.closed: raise PermissionError("Original Docker attach closed")
        return self.pipe.request(frame)

    def wait_closed(self, timeout):
        return self._close_done.wait(timeout) and not self._close_failure

    def close(self):
        import subprocess
        with self._close_lock:
            if self.closed:
                if self._close_pending: raise RuntimeError("Attach cleanup pending; resources UNKNOWN")
                if self._close_failure: raise RuntimeError("Attach cleanup failed; resources UNKNOWN")
                return
            self.closed=True
            self._close_pending=True
            self._close_failure=True
        errors=[]
        try:
            if self.pipe is not None:
                try: self.pipe.close()
                except BaseException as error: errors.append(error)
            if self.process is not None:
                for stream in (self.process.stdin,self.process.stdout):
                    try: stream.close()
                    except BaseException as error: errors.append(error)
                try:
                    if self.process.poll() is None:
                        try: self.process.terminate()
                        except BaseException as error: errors.append(error)
                        try: self.process.wait(timeout=.2)
                        except subprocess.TimeoutExpired: pass
                        except BaseException as error: errors.append(error)
                        if self.process.poll() is None:
                            self.process.kill()
                            self.process.wait(timeout=.2)
                except BaseException as error: errors.append(error)
            with self._close_lock:
                self._close_failure=bool(errors)
        finally:
            with self._close_lock:
                self._close_pending=False
                self._close_done.set()
        if errors:
            interruption=next((error for error in errors if not isinstance(error,Exception)),None)
            raise interruption if interruption is not None else errors[0]


def _linux_proxy_tls(directory, hosts):
    """Executed only in the owned non-root proxy container; key never leaves it."""
    import base64, hashlib, os, ssl, subprocess, time
    from .agent_browser_policy import host_name
    directory.mkdir(mode=0o700)  # Fresh tmpfs directory; no preexisting key adoption.
    config,key,cert=[directory/name for name in ("request.cnf","key.pem","cert.pem")]
    config.write_text("[req]\nprompt=no\ndistinguished_name=dn\nx509_extensions=extensions\n"
        "[dn]\nCN=Curis Work Reader\n[extensions]\nsubjectAltName="+
        ",".join("DNS:"+host_name(host) for host in sorted(hosts))+"\n")
    env={"PATH":"/usr/bin:/bin","LANG":"C.UTF-8","OPENSSL_CONF":str(config)}
    deadline=time.monotonic()+4
    def openssl(args, data=None):
        budget=deadline-time.monotonic()
        if budget<=0: raise TimeoutError("Proxy certificate deadline expired")
        return subprocess.run(["/usr/bin/openssl",*args],input=data,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,
                              cwd=directory,env=env,check=True,timeout=budget).stdout
    try:
        openssl(["req","-new","-newkey","rsa:2048","-nodes","-x509","-days","1","-config",str(config),
                 "-keyout",str(key),"-out",str(cert)])
        key.chmod(0o600)
        public=openssl(["x509","-in",str(cert),"-pubkey","-noout"])
        der=openssl(["pkey","-pubin","-outform","DER"],public)
        context=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.minimum_version=ssl.TLSVersion.TLSv1_2
        context.load_cert_chain(cert,key)
        context.set_alpn_protocols(["http/1.1"])
        return context,base64.b64encode(hashlib.sha256(der).digest()).decode()
    finally:
        key.unlink(missing_ok=True)


def provider_proxy_main():
    return proxy_main(_provider=True)


def proxy_main(*, _provider=False):
    """Private image entrypoint, controlled by original authenticated Docker attach."""
    import os, sys, select, time
    from pathlib import Path
    from .agent_browser_guest import _linux_worker_preflight
    from .agent_browser_policy import PublicTargets, PublicReadProxy
    from .agent_browser_runtime import _unique_json_object, _invalid_json_constant, _finite_json_float
    import json
    if sys.argv[1:] != (["--provider-proxy-stdio"] if _provider else ["--proxy-stdio"]): raise PermissionError("Fixed proxy entrypoint required")
    boot=_linux_worker_preflight()
    deadline,pending=time.monotonic()+5,bytearray()
    while b"\n" not in pending:
        remaining=deadline-time.monotonic()
        if remaining<=0 or not select.select([sys.stdin.fileno()],[],[],remaining)[0]: raise TimeoutError("Proxy bootstrap expired")
        chunk=os.read(sys.stdin.fileno(),262145-len(pending))
        if not chunk or len(chunk)+len(pending)>262144: raise ValueError("Proxy bootstrap invalid")
        pending.extend(chunk)
    line,tail=bytes(pending).split(b"\n",1)
    if tail: raise ValueError("Proxy bootstrap contains extra frames")
    value=json.loads(line,object_pairs_hook=_unique_json_object,parse_constant=_invalid_json_constant,parse_float=_finite_json_float)
    if type(value) is not dict or set(value)!={"identity","nonce","runtime","hosts"} or value["runtime"].get("boot_id")!=boot:
        raise PermissionError("Proxy original runtime mismatch")
    # Reuse strict original-Work/nonce/runtime validation without creating resources.
    from .agent_browser_guest import ReaderGuest
    policy=PublicTargets(value["hosts"])
    ReaderGuest(value["identity"],value["nonce"],value["runtime"],policy,None)
    expiry=time.monotonic()+88
    proxy=PublicReadProxy.__new__(PublicReadProxy)
    if _provider:
        import types
        if policy.hosts!=frozenset({"auth.openai.com","chatgpt.com"}):raise PermissionError("Provider hosts changed")
        context=spki=None
        proxy.serve=types.MethodType(_serve_codex_provider_tunnel,proxy)
    else:context,spki=_linux_proxy_tls(Path("/tmp/curis-reader-proxy"),policy.hosts)
    private = "172.30.251" if _provider and os.environ.get("CURIS_AGENT_PAIRED_NETWORK")=="1" else "172.30.253"
    proxy._initialize(policy,lambda:time.monotonic()<expiry,88,context,spki,(private+".2",8443),private+".3")
    try:
        ack={"identity":dict(value["identity"]),"nonce":value["nonce"],"sequence":0,**value["runtime"],"result":({"proxy_ready":True,"purpose":"CODEX_PROVIDER_CONNECT_V1"} if _provider else {"proxy_ready":True,"proxy_spki":spki})}
        output=memoryview((json.dumps(ack,separators=(",",":"))+"\n").encode())
        os.set_blocking(sys.stdout.fileno(),False)
        ack_deadline=time.monotonic()+1
        while output:
            remaining=ack_deadline-time.monotonic()
            if remaining<=0 or not select.select([],[sys.stdout.fileno()],[],remaining)[1]: raise TimeoutError("Proxy ack expired")
            try: count=os.write(sys.stdout.fileno(),output)
            except BlockingIOError: continue
            if count<=0: raise OSError("Proxy ack channel closed")
            output=output[count:]
        while time.monotonic()<expiry:
            if select.select([sys.stdin.fileno()],[],[],.05)[0]:
                os.read(sys.stdin.fileno(),1)  # EOF or any extra frame revokes this one-shot bootstrap.
                break
    finally:
        proxy.close()


def _private_seccomp():
    import hashlib, json, os, stat
    from pathlib import Path
    path=str(Path(__file__).with_name("reader_seccomp.json"))
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    try:
        info=os.fstat(fd)
        if (not stat.S_ISREG(info.st_mode) or info.st_uid!=os.geteuid() or info.st_nlink!=1
                or info.st_mode & 0o022 or not 0<info.st_size<=65536):
            raise PermissionError("Private seccomp input identity or size invalid")
        raw=os.read(fd,65537)
    finally:
        os.close(fd)
    if hashlib.sha256(raw).hexdigest()!=_PRIVATE_SECCOMP_SHA256:
        raise PermissionError("Private seccomp input changed")
    return json.dumps(json.loads(raw),separators=(",",":"))


class OwnedAgentContainerError(RuntimeError):
    def __init__(self, reason, receipt=None, diagnostic=None):
        super().__init__("Owned Agent container: "+reason+"; external effects UNKNOWN")
        self.reason, self.receipt, self.diagnostic = reason, receipt, diagnostic


def _validate_agent_candidate_request(command, input, timeout, should_stop):
    import math
    if (type(command) is not list or len(command)!=5
            or command[:4]!=["/usr/bin/python3","-I","-B","-c"]
            or any(type(x) is not str or "\0" in x for x in command)
            or len(command[4].encode())>16384 or type(input) is not str or len(input.encode())>32768
            or type(timeout) not in (int,float) or not math.isfinite(timeout) or not 0<timeout<=80
            or not callable(should_stop)):
        raise PermissionError("Agent CPU candidate input is outside fixed scope")


class _OwnedAgentContainerSession:
    """Unreleased zero-provider candidate; the existing owner owns all mutations."""
    def __init__(self, identity, image_digest=_AGENT_CONTAINER_IMAGE, *, _linux_profile=False):
        import re
        if (type(_linux_profile) is not bool or
                (not _linux_profile and image_digest != _AGENT_CONTAINER_IMAGE)
                or not re.fullmatch(r"sha256:[0-9a-f]{64}",str(image_digest))):
            raise PermissionError("Agent candidate requires its fixed existing image")
        self.owner=_DedicatedDockerOwner(identity,image_digest)
        self._used=False
        self._lock,self._stop_lock=threading.Lock(),threading.Lock()
        self._revoked=threading.Event()
        self._done=threading.Event()
        self._reason=None
        self.stop_receipt=None
        self.work_tools=None
        self._linux_before_launch=None
        self._linux_on_login=None
        self._linux_control=False
        self._owned_auth=None
        self._auth_writeback_seen=False

    def bind_owned_auth(self, lease, capability_id):
        from .credential_vault import _CodexAuthLease
        with self._lock:
            if (self._used or self._owned_auth is not None or type(lease) is not _CodexAuthLease
                    or lease.identity != self.owner.identity or lease.metadata["capability_id"] != capability_id
                    or getattr(self.owner,"_work_parent",None) is None):
                raise PermissionError("Original Keychain authentication lease is invalid")
            self._owned_auth=lease
            lease.bind_parent(self.owner._work_parent)
        return self

    def _auth_binding(self):
        parent=self.owner._work_parent
        return {"identity":self.owner.identity.copy(),"parent_attempt":parent.attempt,
            **{key:getattr(self.owner,key) for key in ("nonce","boot_id","container_id","image_digest")}}

    def run_linux_control(self, public_catalog, *, timeout, should_stop, on_device_login=None):
        from .agent_work_resources import scoped_codex_model_catalog
        import json
        if self._owned_auth is None or self._owned_auth.intent not in {"login","status","disconnect"}:
            raise PermissionError("Original authentication-only lease required")
        catalog,_=scoped_codex_model_catalog(public_catalog,"gpt-5.6-sol")
        data={"identity":{key:self.owner.identity[key] for key in ("tenant_id","company_id","work_ref","task_id")},"skills":[]}
        def deny_model():raise PermissionError("Authentication control cannot call a model")
        with self._lock:
            if self._used or self._linux_before_launch is not None:raise PermissionError("Authentication control cannot replay")
            self._linux_control=True;self._linux_before_launch=deny_model;self._linux_on_login=on_device_login
            self.owner._linux_bootstrap={"resources":{"resources":data,"sha256":hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()},"catalog":catalog}
        return self._run_once(["/usr/bin/python3","-I","-B","-c","pass"],input="",timeout=timeout,should_stop=should_stop,linux=True)

    def run_linux_candidate(self, prompt, public_catalog, *, timeout, should_stop, before_launch, on_device_login=None):
        from .agent_work_resources import scoped_codex_model_catalog
        if (not callable(before_launch) or self.work_tools is None
                or on_device_login is not None and not callable(on_device_login)):
            raise PermissionError("Linux candidate requires original tools and model reservation")
        _validate_agent_candidate_request(["/usr/bin/python3","-I","-B","-c","pass"],prompt,timeout,should_stop)
        catalog,_=scoped_codex_model_catalog(public_catalog,"gpt-5.6-sol")
        import json
        bootstrap={"resources":self.work_tools.descriptor,"catalog":catalog}
        if len(json.dumps(bootstrap,separators=(",",":"),allow_nan=False).encode())>60000:
            raise PermissionError("Linux bootstrap exceeds original channel bound")
        with self._lock:
            if self._used or self._linux_before_launch is not None:
                raise PermissionError("Linux candidate cannot be replayed")
            self.owner._linux_bootstrap=bootstrap
            self._linux_before_launch=before_launch
            self._linux_on_login=on_device_login
        return self._run_once(["/usr/bin/python3","-I","-B","-c","pass"],input=prompt,timeout=timeout,should_stop=should_stop,linux=True)

    def _authenticate_linux(self, channel, deadline):
        import re,time
        if self._linux_on_login is None:raise OwnedAgentContainerError("authentication_required")
        def request(sequence,action,arguments):
            if self._revoked.is_set() or time.monotonic()>=deadline:raise OwnedAgentContainerError("cancelled")
            frame=self.owner.agent_frame(sequence,action,arguments)
            value=channel.request(frame)
            bound={k:v for k,v in frame.items() if k not in {"action","arguments"}}
            if (type(value) is not dict or set(value)!={*bound,"result"}
                    or any(value.get(k)!=v for k,v in bound.items())):
                raise OwnedAgentContainerError("response_invalid")
            return value["result"]
        value=request(1,"authenticate",{"timeout":min(80,deadline-time.monotonic())})
        if value=={"authenticated":False}:raise OwnedAgentContainerError("authentication_required")
        if type(value) is not dict or set(value)!={"device_login"}:raise OwnedAgentContainerError("response_invalid")
        challenge=value["device_login"]
        if (type(challenge) is not dict or set(challenge)!={"verification_url","user_code"}
                or challenge["verification_url"]!="https://auth.openai.com/codex/device"
                or type(challenge["user_code"]) is not str
                or not re.fullmatch(r"[A-Z0-9]{4}-[A-Z0-9]{4}",challenge["user_code"])):
            raise OwnedAgentContainerError("response_invalid")
        approved=self._linux_on_login(challenge.copy()) is True
        result=request(2,"login_ack",{"continue":approved})
        if not approved:raise OwnedAgentContainerError("cancelled")
        if type(result) is not dict or set(result)!={"authenticated"} or result["authenticated"] is not True:
            raise OwnedAgentContainerError("authentication_required")
        return 3

    def bind_work_tools(self, tools):
        with self._lock:
            if self._used or self.work_tools is not None:
                raise PermissionError("Original Work tools cannot be rebound")
            if tools.identity != self.owner.identity:
                raise PermissionError("Original Work tools identity changed")
            self.work_tools=tools
            parent = getattr(self.owner, "_work_parent", None)
            if parent is not None: parent.revokers[self.owner._work_role] = tools.revoke
        return self

    def revoke(self, reason=None):
        self._revoked.set()
        self.owner._revoked_event.set()
        if reason is not None and self._owned_auth is not None:self._owned_auth.cancel()
        with self._lock:
            if reason is not None and self._reason is None:self._reason=reason
        # Allocation/start also hold this lock until their exact IDs are retained.
        with self.owner._state_lock:self.owner.revoked=True
        if self.work_tools is not None:self.work_tools.revoke()

    def _execute_with_tools(self, channel, frame, deadline):
        import time
        if self.work_tools is not None:
            self.work_tools.bind({key:getattr(self.owner,key) for key in
                                  ("nonce","boot_id","container_id","image_digest")})
        while True:
            if self._revoked.is_set() or time.monotonic() >= deadline:
                raise OwnedAgentContainerError("timeout" if time.monotonic() >= deadline else "cancelled")
            if getattr(self.owner,"_provider_mode",False):self.owner._verify_agent_container(running=True)
            response=channel.request(frame)
            if getattr(self.owner,"_provider_mode",False):self.owner._verify_agent_container(running=True)
            expected={k:v for k,v in frame.items() if k not in {"action","arguments"}}
            if (type(response) is not dict or set(response)!={*expected,"result"}
                    or any(response.get(k)!=v for k,v in expected.items())):
                raise OwnedAgentContainerError("response_invalid")
            value=response["result"]
            if type(value) is dict and "auth_writeback" in value:
                payload=value["auth_writeback"]
                if (set(value)!={"auth_writeback"} or self._owned_auth is None or self._auth_writeback_seen
                        or type(payload) is not dict or set(payload)!={"cache","authenticated"}):
                    raise OwnedAgentContainerError("response_invalid")
                self._auth_writeback_seen=True
                self._owned_auth.persist(self._auth_binding(),payload["cache"],authenticated=payload["authenticated"])
                if self._revoked.is_set() or time.monotonic()>=deadline:raise OwnedAgentContainerError("cancelled")
                frame=self.owner.agent_frame(frame["sequence"]+1,"auth_saved",{"accepted":True})
                continue
            if type(value) is not dict or "tool_request" not in value:return response,frame
            if self._auth_writeback_seen:raise OwnedAgentContainerError("response_invalid")
            if set(value)!={"tool_request"} or self.work_tools is None:
                raise OwnedAgentContainerError("response_invalid")
            if self._revoked.is_set() or time.monotonic() >= deadline:
                raise OwnedAgentContainerError("cancelled")
            reply=self.work_tools.dispatch(value["tool_request"])
            if self._revoked.is_set() or time.monotonic() >= deadline:
                raise OwnedAgentContainerError("cancelled")
            frame=self.owner.agent_frame(frame["sequence"]+1,"tool_response",reply)

    def _stop(self):
        self.revoke()
        with self._lock:
            if not self._used:return None
        with self._stop_lock:
            with self.owner._state_lock:
                cid=self.owner.container_id
            if not cid:
                if not self._done.wait(6):raise OwnedAgentContainerError("allocation_unknown")
                with self.owner._state_lock:cid=self.owner.container_id
            if not cid:
                if self.owner.journal and any(r.get("nonce")==self.owner.nonce and r.get("state")=="INTENT"
                                              for r in self.owner.journal.records):
                    raise OwnedAgentContainerError("allocation_unknown")
                return None
            if not self.owner.stop_requested:
                self.owner.revoke_bound_and_stop(self.owner.identity.copy(),self.owner.nonce,
                    dict(complete=False,executionAuthorized=False,boot_id=self.owner.boot_id,
                         container_id=cid,image_digest=self.owner.image_digest))
            elif not self.owner._stop_done.wait(6):
                raise OwnedAgentContainerError("cleanup_unknown")
            receipt=self.owner.stop_receipt
            expected={"identity":self.owner.identity,"nonce":self.owner.nonce,"boot_id":self.owner.boot_id,
                      "container_id":cid,"image_digest":self.owner.image_digest}
            if (type(receipt) is not dict or any(receipt.get(k)!=v for k,v in expected.items())
                    or receipt.get("ledger_state")!="CLOSED_VERIFIED"
                    or receipt.get("proxy_id")!=self.owner.proxy_id
                    or type(receipt.get("exit_codes")) is not dict
                    or set(receipt["exit_codes"])!=set(filter(None,(cid,self.owner.proxy_id)))
                    or any(type(v) is not int for v in receipt["exit_codes"].values())):
                raise OwnedAgentContainerError("cleanup_unknown")
            self.stop_receipt=receipt.copy()
            return self.stop_receipt

    def close(self):
        self.revoke("eof")
        return self._stop()

    def run(self, command, *, input, timeout, should_stop):
        return self._run_once(command,input=input,timeout=timeout,should_stop=should_stop,linux=False)

    def _run_once(self, command, *, input, timeout, should_stop, linux):
        import json,math,secrets,time
        with self._lock:
            if linux != (self._linux_before_launch is not None):
                raise PermissionError("Original execution mode changed")
            if self._used:raise PermissionError("Agent container session cannot be replayed")
            self._used=True
        _validate_agent_candidate_request(command,input,timeout,should_stop)
        def cancelled():
            try:return self._revoked.is_set() or bool(self._owned_auth is not None and self._owned_auth.cancelled.is_set()) or bool(should_stop())
            except Exception:return True
        if cancelled() or self._revoked.is_set():raise OwnedAgentContainerError("cancelled")
        deadline=time.monotonic()+timeout
        nonce=secrets.token_hex(24)
        result={}
        def worker():
            phase="prepare"
            try:
                self.owner.prepare_agent(nonce)
                if self._revoked.is_set():raise OwnedAgentContainerError("cancelled")
                if self._owned_auth is not None:
                    self.owner._verify_agent_container(running=False)
                    cache=self._owned_auth.restore(self._auth_binding())
                    self.owner._linux_bootstrap.update(auth_cache=cache,auth_mode=self._owned_auth.intent)
                    if len(json.dumps(self.owner._linux_bootstrap,separators=(',',':')).encode())>58000:
                        raise OwnedAgentContainerError("response_invalid")
                    if self._revoked.is_set() or time.monotonic()>=deadline:raise OwnedAgentContainerError("cancelled")
                phase="bootstrap"
                channel=self.owner.start_agent_runtime()
                remaining=deadline-time.monotonic()
                if remaining<=0:raise OwnedAgentContainerError("timeout")
                if self._revoked.is_set():raise OwnedAgentContainerError("cancelled")
                execution_sequence=1
                if self._linux_before_launch is not None and not getattr(self.owner,"_linux_authenticated",False):
                    if self._owned_auth is None or self._owned_auth.intent=="login":
                        execution_sequence=self._authenticate_linux(channel,deadline)
                    elif not self._linux_control:raise OwnedAgentContainerError("authentication_required")
                frame=self.owner.agent_frame(execution_sequence,"execute",{"command":command,"input":input,"timeout":remaining})
                phase="execute"
                if self._linux_control:
                    frame=self.owner.agent_frame(execution_sequence,"auth_finish",{"timeout":deadline-time.monotonic()})
                elif self._linux_before_launch is not None:
                    self._linux_before_launch()
                    if self._revoked.is_set() or time.monotonic()>=deadline:
                        raise OwnedAgentContainerError("cancelled")
                    frame=self.owner.agent_frame(execution_sequence,"execute",{"input":input,"timeout":deadline-time.monotonic()})
                response,frame=self._execute_with_tools(channel,frame,deadline)
                if time.monotonic()>=deadline:raise OwnedAgentContainerError("timeout")
                expected={k:v for k,v in frame.items() if k not in {"action","arguments"}}
                if (type(response) is not dict or set(response)!={*expected,"result"}
                        or any(response.get(k)!=v for k,v in expected.items())):
                    raise OwnedAgentContainerError("response_invalid")
                value=response["result"]
                if self._owned_auth is not None and not self._auth_writeback_seen:
                    raise OwnedAgentContainerError("authentication_required")
                if type(value) is not dict or value.get("reason")!="completed":
                    raise OwnedAgentContainerError("eof" if type(value) is dict and value.get("reason")=="eof" else "timeout")
                if (set(value)!={"reason","returncode","stdout","stderr"}
                        or type(value["returncode"]) is not int or not -255<=value["returncode"]<=255
                        or any(type(value[k]) is not str for k in ("stdout","stderr"))
                        or len(value["stdout"].encode())+len(value["stderr"].encode())>32768):
                    raise OwnedAgentContainerError("response_invalid")
                if self._owned_auth is not None and value["returncode"] != 0:
                    raise OwnedAgentContainerError("authentication_required")
                self.owner._verify_agent_container(running=True)
                if self._revoked.is_set():raise OwnedAgentContainerError("cancelled")
                if self._owned_auth is not None:
                    value={**value,**{key:self._owned_auth.redact_output(value[key]) for key in ("stdout","stderr")}}
                result["value"]=value
            except BaseException as error:
                result["error"]=error
                code=getattr(error,"agent_code",None)
                allowed={"SCOPE","ENV","PROCESS_CONFIG","CAPABILITIES","HOST_EXPOSURE","NETWORK","SECURITY_OPT",
                         "RESTART_POLICY","MOUNTS","PROCESS_STATE","RESOURCE_TMPFS","RESOURCE_MEMORY",
                         "RESOURCE_PIDSLIMIT","RESOURCE_NANOCPUS","RESOURCE_SHMSIZE","RESOURCE_LOGCONFIG"}
                result["diagnostic"]={"phase":phase,"exception":type(error).__name__ if type(error).__name__ in
                    {"PermissionError","ValueError","TimeoutError","EOFError","BrokenPipeError","OSError","OwnedAgentContainerError"} else "OTHER",
                    "code":code if code in allowed else "UNKNOWN"}
            finally:
                bootstrap=getattr(self.owner,"_linux_bootstrap",None)
                if bootstrap is not None:bootstrap.pop("auth_cache",None)
                self._done.set()
        from contextvars import copy_context
        context=copy_context()
        thread=threading.Thread(target=lambda:context.run(worker),name="curis-owned-agent-container",daemon=True)
        thread.start()
        try:
            while not self._done.wait(.02):
                if cancelled():
                    self.revoke("cancelled");break
                if time.monotonic()>=deadline:
                    self.revoke("timeout");break
        finally:
            try:self._stop()
            except BaseException as error:
                raise OwnedAgentContainerError("cleanup_unknown",self.stop_receipt) from error
            thread.join(.2)
        if not self._done.is_set():raise OwnedAgentContainerError("worker_unknown",self.stop_receipt)
        # Normal cleanup revokes the transport too; only external cancellation invalidates the result.
        try: stopped_after = bool(should_stop()) or bool(self._owned_auth is not None and self._owned_auth.cancelled.is_set())
        except Exception: stopped_after = True
        if stopped_after and self._reason is None:self._reason="cancelled"
        if self._reason is not None:raise OwnedAgentContainerError(self._reason,self.stop_receipt)
        if "error" in result:
            error=result["error"]
            reason=error.reason if isinstance(error,OwnedAgentContainerError) else "eof" if isinstance(error,(EOFError,BrokenPipeError)) else "execution_unknown"
            raise OwnedAgentContainerError(reason,self.stop_receipt,result.get("diagnostic")) from error
        if self.stop_receipt is None:raise OwnedAgentContainerError("cleanup_unknown")
        return {**result["value"],"stop_receipt":self.stop_receipt}


def load_owned_linux_profile(*, authentication=False):
    """Use the existing bundled pinned lock; absent or unaccepted Agent data stays held."""
    import re
    from .agent_adapter import AgentExecutionError,require_codex_execution_available,require_owned_container_execution_available
    from .agent_browser_runtime import load_trusted_reader_lock
    from .agent_work_resources import scoped_codex_model_catalog
    if type(authentication) is not bool:raise ValueError("Authentication purpose must be explicit")
    if not authentication:require_codex_execution_available();require_owned_container_execution_available()
    try:lock=load_trusted_reader_lock()
    except (ValueError,OSError) as error:
        raise AgentExecutionError("Linux Codex 运行锁尚未接受。",status="container_execution_held") from error
    profile=lock.get("linuxCodex")
    if (type(profile) is not dict or set(profile)!={"imageDigest","binarySha256","guestSha256","modelCatalog",
            "egressPurpose","authenticationOwner","complete","executionAuthorized"}
            or profile.get("complete") is not True or profile.get("executionAuthorized") is not True
            or not re.fullmatch(r"sha256:[0-9a-f]{64}",str(profile.get("imageDigest")))
            or profile.get("binarySha256")!="57a159f67999794494a172e71c12c6b5a211542ea90c66ea2ce9e6ac1edec6b1"
            or profile.get("guestSha256")!=hashlib.sha256(_AGENT_CODEX_SOURCE.encode()).hexdigest()
            or profile.get("egressPurpose")!="CODEX_PROVIDER_CONNECT_V1"
            or profile.get("authenticationOwner")!="CURIS_KEYCHAIN_TMPFS_AUTH_V1"):
        raise AgentExecutionError("Linux Codex 镜像、认证及出口尚未接受。",status="container_execution_held")
    scoped_codex_model_catalog(profile["modelCatalog"],"gpt-5.6-sol")
    return profile


def open_owned_agent_container(identity):
    # A private Reader release never releases real Agent code/auth/tool egress.
    from .agent_adapter import require_owned_container_execution_available
    require_owned_container_execution_available()
    profile=load_owned_linux_profile()
    session = _OwnedAgentContainerSession(identity,profile["imageDigest"],_linux_profile=True)
    parent = _WORK_OWNER_SCOPE.get()
    if parent is not None: parent.bind(session.owner, "agent")
    return session
