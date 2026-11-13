"""Unreleased Reader guest bridge; caller must independently authenticate its peer."""
from __future__ import annotations

import json
import math
import os
import select
import socket
import stat
import time

MAX_REQUEST = 262144
MAX_RESPONSE = 16 * 1024 * 1024
_BINDING = ("identity", "nonce", "boot_id", "container_id", "image_digest")


def _unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate frame key")
        result[key] = value
    return result


def _finite(value):
    result = float(value)
    if not math.isfinite(result):
        raise ValueError("non-finite frame number")
    return result


def _constant(_value):
    raise ValueError("non-finite frame number")


def _decode(frame):
    value = json.loads(frame[:-1].decode("utf-8"), object_pairs_hook=_unique,
                       parse_float=_finite, parse_constant=_constant)
    if not isinstance(value, dict):
        raise ValueError("frame must be an object")
    return value


def _wait(fd, writing, deadline, alive, clock, guard_socket=None):
    while True:
        if not alive():
            raise PermissionError("bridge authorization revoked")
        remaining = deadline - clock()
        if remaining <= 0:
            raise TimeoutError("bridge deadline")
        reads = [] if writing else [fd]
        if guard_socket is not None and guard_socket not in reads:
            reads.append(guard_socket)
        readable, writable, _ = select.select(reads, [fd] if writing else [], [], min(remaining, 0.05))
        if guard_socket is not None and guard_socket in readable:
            raise ValueError("pipelined request or peer closed")
        if writable if writing else readable:
            return


def _read_frame(fd, limit, deadline, alive, clock, guard_socket=None):
    pending = bytearray()
    while True:
        _wait(fd, False, deadline, alive, clock, guard_socket)
        try:
            chunk = os.read(fd, min(65536, limit + 1 - len(pending)))
        except BlockingIOError:
            continue
        if not chunk:
            raise EOFError("bridge closed before complete frame")
        pending.extend(chunk)
        if len(pending) > limit:
            raise ValueError("bridge frame exceeds limit")
        if b"\n" in pending:
            if pending[-1:] != b"\n" or pending.count(b"\n") != 1:
                raise ValueError("pipelined or extra frame data")
            return bytes(pending)


def _write_frame(fd, data, deadline, alive, clock, guard_socket=None):
    remaining = memoryview(data)
    while remaining:
        _wait(fd, True, deadline, alive, clock, guard_socket)
        try:
            count = os.write(fd, remaining)
        except BlockingIOError:
            continue
        if count <= 0:
            raise EOFError("bridge closed during frame")
        remaining = remaining[count:]


def serve_bridge(socket_fd, to_guest_fd, from_guest_fd, binding, *, alive, seconds=90, clock=time.monotonic,
                 handoff=None):
    """Take exclusive ownership of three FDs and relay one candidate session.

    Ownership transfers after argument, binding, and FD existence validation; a
    one-byte handoff receipt becomes 1 at transfer. Before that the caller owns all
    three FDs, and afterwards this function closes them. The caller must retain
    no aliases after transfer. The OS may still have
    aliases this function cannot observe. Local close is not proof of remote stop.
    Peer identity and platform authorization must be independently established.
    On some systems anonymous pipe endpoints have distinct inode values even when
    paired; the inode check alone cannot prove their ownership or independence.
    """
    if (any(type(fd) is not int for fd in (socket_fd, to_guest_fd, from_guest_fd))
            or len({socket_fd, to_guest_fd, from_guest_fd}) != 3
            or not callable(alive) or not 0 < seconds <= 90 or type(binding) is not dict
            or (handoff is not None and (type(handoff) is not bytearray or handoff != b"\x00"))):
        raise ValueError("bridge configuration invalid")
    binding = binding.copy()
    if any(type(k) is not str for k in binding) or set(binding) != set(_BINDING):
        raise ValueError("bridge configuration invalid")
    identity = binding["identity"]
    if type(identity) is dict:
        identity = identity.copy()
    required = ("tenant_id", "company_id", "work_ref", "task_id", "employee_id", "binding_ref")
    if (type(identity) is not dict or any(type(k) is not str for k in identity) or set(identity) != set(required)
            or any(type(identity[k]) is not str or not identity[k] for k in required)
            or any(type(binding[k]) is not str or not binding[k] for k in _BINDING if k != "identity")
            or len(binding["nonce"]) != 48
            or any(c not in "0123456789abcdef" for c in binding["nonce"])):
        raise ValueError("bridge binding invalid")
    fixed = {**binding, "identity": identity.copy()}
    for fd in (socket_fd, to_guest_fd, from_guest_fd):
        os.fstat(fd)
    owned = [socket_fd, to_guest_fd, from_guest_fd]
    try:
        if handoff is not None:
            handoff[0] = 1
        sock, to_guest, from_guest = owned
        if (not stat.S_ISSOCK(os.fstat(sock).st_mode)
                or not stat.S_ISFIFO(os.fstat(to_guest).st_mode)
                or not stat.S_ISFIFO(os.fstat(from_guest).st_mode)):
            raise ValueError("bridge requires a socket and two FIFO ends")
        if (os.fstat(to_guest).st_dev, os.fstat(to_guest).st_ino) == (os.fstat(from_guest).st_dev, os.fstat(from_guest).st_ino):
            raise ValueError("bridge FIFO endpoints must be distinct")
        probe_fd = os.dup(sock)
        try:
            probe = socket.socket(fileno=probe_fd)
        except BaseException:
            os.close(probe_fd)
            raise
        try:
            families = {socket.AF_UNIX}
            if hasattr(socket, "AF_VSOCK"):
                families.add(socket.AF_VSOCK)
            if probe.family not in families or probe.getsockopt(socket.SOL_SOCKET, socket.SO_TYPE) != socket.SOCK_STREAM:
                raise ValueError("bridge requires a local stream socket")
        finally:
            probe.close()
        import fcntl
        if ((fcntl.fcntl(to_guest, fcntl.F_GETFL) & os.O_ACCMODE) != os.O_WRONLY
                or (fcntl.fcntl(from_guest, fcntl.F_GETFL) & os.O_ACCMODE) != os.O_RDONLY):
            raise ValueError("bridge FIFO direction invalid")
        for fd in owned:
            os.set_blocking(fd, False)
        deadline = clock() + seconds
        sequence = 0
        while True:
            request = _read_frame(sock, MAX_REQUEST, deadline, alive, clock)
            frame = _decode(request)
            if (set(frame) != {*_BINDING, "sequence", "action", "arguments"}
                    or any(frame.get(k) != fixed[k] for k in _BINDING)
                    or type(frame.get("sequence")) is not int
                    or frame["sequence"] != sequence + 1):
                raise ValueError("bridge request binding mismatch")
            _write_frame(to_guest, request, deadline, alive, clock, guard_socket=sock)
            response = _read_frame(from_guest, MAX_RESPONSE, deadline, alive, clock, guard_socket=sock)
            reply = _decode(response)
            if (set(reply) != {*_BINDING, "sequence", "result"}
                    or any(reply.get(k) != fixed[k] for k in _BINDING)
                    or type(reply.get("sequence")) is not int
                    or reply["sequence"] != frame["sequence"]):
                raise ValueError("bridge response binding mismatch")
            _write_frame(sock, response, deadline, alive, clock, guard_socket=sock)
            sequence += 1
    finally:
        if handoff is None or handoff[0] == 1:
            for fd in owned:
                try:
                    os.close(fd)
                except OSError:
                    pass
