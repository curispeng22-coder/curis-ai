import importlib.util
import json
import os
from pathlib import Path
import select
import socket
import threading

import pytest

PATH = Path(__file__).resolve().parents[2] / "desktop/runtime/reader_guest_vsock_bridge.py"
spec = importlib.util.spec_from_file_location("reader_guest_vsock_bridge", PATH)
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)

IDENTITY = {"tenant_id":"tenant", "company_id":"company", "work_ref":"work", "task_id":"task",
            "employee_id":"employee", "binding_ref":"binding"}
BINDING = {"identity": IDENTITY, "nonce":"a" * 48, "boot_id":"boot",
           "container_id":"container", "image_digest":"sha256:fixture"}


def frame(value):
    return (json.dumps(value, separators=(",", ":")) + "\n").encode()


def read_frame(fd):
    result = bytearray()
    while not result.endswith(b"\n"):
        ready, _, _ = select.select([fd], [], [], 2)
        assert ready
        part = os.read(fd, 65536)
        assert part
        result.extend(part)
    return bytes(result)


_KNOWN_LOCAL_SOCKET_IDENTITIES = set()


def local_pair():
    host, guest = socket.socketpair()
    info = os.fstat(guest.fileno())
    _KNOWN_LOCAL_SOCKET_IDENTITIES.add((info.st_dev, info.st_ino))
    return host, guest


@pytest.fixture(autouse=True)
def explicit_unix_socket_probe(monkeypatch):
    # Only test-created AF_UNIX socketpair descriptors may use this wrapper.
    # The production automatic family detection and real AF_VSOCK remain untested.
    from types import SimpleNamespace
    _KNOWN_LOCAL_SOCKET_IDENTITIES.clear()
    def probe(*args, **kwargs):
        if args or set(kwargs) != {"fileno"}:
            raise PermissionError("only the fixture probe is allowed")
        fd = kwargs["fileno"]
        info = os.fstat(fd)
        if (info.st_dev, info.st_ino) not in _KNOWN_LOCAL_SOCKET_IDENTITIES:
            raise PermissionError("probe does not own a test socketpair")
        return socket.socket(socket.AF_UNIX, socket.SOCK_STREAM, fileno=fd)
    values = {"socket": probe, "AF_UNIX": socket.AF_UNIX, "SOCK_STREAM": socket.SOCK_STREAM,
              "SOL_SOCKET": socket.SOL_SOCKET, "SO_TYPE": socket.SO_TYPE}
    if hasattr(socket, "AF_VSOCK"):
        values["AF_VSOCK"] = socket.AF_VSOCK
    monkeypatch.setattr(bridge, "socket", SimpleNamespace(**values))
    yield
    _KNOWN_LOCAL_SOCKET_IDENTITIES.clear()


def launch():
    host, guest = local_pair()
    guest_in, bridge_out = os.pipe()
    bridge_in, guest_out = os.pipe()
    owned = (guest.detach(), bridge_out, bridge_in)
    errors = []
    def run():
        try:
            bridge.serve_bridge(*owned, BINDING, alive=lambda: True, seconds=2)
        except (EOFError, ValueError, PermissionError, TimeoutError, OSError) as error:
            errors.append(error)
    worker = threading.Thread(target=run)
    worker.start()
    return host, guest_in, guest_out, owned, worker, errors


def cleanup(host, guest_in, guest_out, worker):
    host.close()
    worker.join(timeout=3)
    os.close(guest_in)
    os.close(guest_out)
    assert not worker.is_alive()


def test_bridge_preserves_one_request_and_response_bytes():
    host, guest_in, guest_out, owned, worker, errors = launch()
    request = frame({**BINDING, "sequence":1, "action":"start", "arguments":{}})
    response = frame({**BINDING, "sequence":1, "result":{"ready":True}})
    try:
        host.sendall(request[:7])
        host.sendall(request[7:])
        assert read_frame(guest_in) == request
        os.write(guest_out, response)
        assert read_frame(host.fileno()) == response
    finally:
        cleanup(host, guest_in, guest_out, worker)
    assert errors and isinstance(errors[0], EOFError)
    for fd in owned:
        with pytest.raises(OSError):
            os.fstat(fd)


@pytest.mark.parametrize("payload", [
    b'{"identity":{},"identity":{}}\n',
    b'{"result":NaN}\n',
    b'{"result":1e999}\n',
    b'{"result":"\xff"}\n',
    b'{}\n{}\n',
])
def test_bridge_rejects_ambiguous_frames_and_closes_owned_fds(payload):
    host, guest_in, guest_out, owned, worker, errors = launch()
    try:
        host.sendall(payload)
        worker.join(timeout=3)
        assert not worker.is_alive() and errors
        assert select.select([guest_in], [], [], 1)[0]
        assert os.read(guest_in, 1024) == b""
    finally:
        cleanup(host, guest_in, guest_out, worker)
    for fd in owned:
        with pytest.raises(OSError):
            os.fstat(fd)


def test_bridge_rejects_late_second_frame_while_response_pending():
    host, guest_in, guest_out, owned, worker, errors = launch()
    request = frame({**BINDING, "sequence":1, "action":"start", "arguments":{}})
    try:
        host.sendall(request)
        assert read_frame(guest_in) == request
        host.sendall(frame({**BINDING, "sequence":2, "action":"start", "arguments":{}}))
        worker.join(timeout=3)
        assert not worker.is_alive() and errors and isinstance(errors[0], ValueError)
    finally:
        cleanup(host, guest_in, guest_out, worker)



def test_bridge_detects_peer_half_close_while_response_pending():
    host, guest_in, guest_out, owned, worker, errors = launch()
    request = frame({**BINDING, "sequence":1, "action":"start", "arguments":{}})
    try:
        host.sendall(request)
        assert read_frame(guest_in) == request
        host.shutdown(socket.SHUT_WR)
        worker.join(timeout=3)
        assert not worker.is_alive() and errors
    finally:
        cleanup(host, guest_in, guest_out, worker)
    for fd in owned:
        with pytest.raises(OSError):
            os.fstat(fd)


def test_bridge_rejects_same_fifo_and_closes_transferred_fds():
    host, guest = local_pair()
    read_end, write_end = os.pipe()
    owned = (guest.detach(), write_end, read_end)
    try:
        first, second = os.fstat(read_end), os.fstat(write_end)
        if (first.st_dev, first.st_ino) != (second.st_dev, second.st_ino):
            pytest.skip("anonymous pipe endpoints expose different inode identities on this platform")
        with pytest.raises(ValueError, match="distinct"):
            bridge.serve_bridge(*owned, BINDING, alive=lambda: True, seconds=1)
        for fd in owned:
            with pytest.raises(OSError):
                os.fstat(fd)
    finally:
        host.close()
        for fd in owned:
            try:
                os.close(fd)
            except OSError:
                pass


def test_bridge_rejects_duplicated_fifo_endpoint():
    host, guest = local_pair()
    read_end, write_end = os.pipe()
    alias = os.dup(read_end)
    owned = (guest.detach(), read_end, alias)
    try:
        with pytest.raises(ValueError, match="distinct"):
            bridge.serve_bridge(*owned, BINDING, alive=lambda: True, seconds=1)
        for fd in owned:
            with pytest.raises(OSError):
                os.fstat(fd)
    finally:
        host.close()
        os.close(write_end)


def test_bridge_keeps_caller_fds_when_binding_validation_fails():
    host, guest = local_pair()
    guest_in, bridge_out = os.pipe()
    bridge_in, guest_out = os.pipe()
    owned = (guest.detach(), bridge_out, bridge_in)
    try:
        with pytest.raises(ValueError, match="binding"):
            bridge.serve_bridge(*owned, {**BINDING, "nonce":"bad"}, alive=lambda: True, seconds=1)
        for fd in owned:
            os.fstat(fd)
    finally:
        host.close()
        for fd in (*owned, guest_in, guest_out):
            os.close(fd)


def test_bridge_rejects_oversized_request():
    host, guest_in, guest_out, owned, worker, errors = launch()
    try:
        try:
            host.sendall(b"x" * (bridge.MAX_REQUEST + 1))
        except (BrokenPipeError, ConnectionResetError):
            pass
        worker.join(timeout=3)
        assert not worker.is_alive() and errors and isinstance(errors[0], ValueError)
    finally:
        cleanup(host, guest_in, guest_out, worker)


def test_bridge_revocation_during_pending_reply_is_unknown():
    running = [True]
    host, guest = local_pair()
    guest_in, bridge_out = os.pipe()
    bridge_in, guest_out = os.pipe()
    owned = (guest.detach(), bridge_out, bridge_in)
    errors = []
    def run():
        try:
            bridge.serve_bridge(*owned, BINDING, alive=lambda: running[0], seconds=2)
        except (EOFError, ValueError, PermissionError, TimeoutError, OSError) as error:
            errors.append(error)
    worker = threading.Thread(target=run)
    worker.start()
    try:
        host.sendall(frame({**BINDING, "sequence":1, "action":"start", "arguments":{}}))
        read_frame(guest_in)
        running[0] = False
        worker.join(timeout=3)
        assert not worker.is_alive() and errors and isinstance(errors[0], PermissionError)
    finally:
        cleanup(host, guest_in, guest_out, worker)



@pytest.mark.parametrize("response", [
    b'{"result":1,"result":2}\n',
    b'{"result":NaN}\n',
    frame({**BINDING, "sequence":2, "result":{"ready":True}}),
    frame({**BINDING, "nonce":"b" * 48, "sequence":1, "result":{"ready":True}}),
])
def test_bridge_rejects_bad_response_without_forwarding(response):
    host, guest_in, guest_out, owned, worker, errors = launch()
    try:
        host.sendall(frame({**BINDING, "sequence":1, "action":"start", "arguments":{}}))
        read_frame(guest_in)
        os.write(guest_out, response)
        worker.join(timeout=3)
        assert not worker.is_alive() and errors
        assert host.recv(1024) == b""
    finally:
        cleanup(host, guest_in, guest_out, worker)


def test_bridge_accepts_request_at_exact_frame_limit():
    host, guest_in, guest_out, owned, worker, errors = launch()
    raw = frame({**BINDING, "sequence":1, "action":"start", "arguments":{}})
    request = raw[:-1] + b" " * (bridge.MAX_REQUEST - len(raw)) + b"\n"
    response = frame({**BINDING, "sequence":1, "result":{"ready":True}})
    try:
        host.sendall(request)
        assert read_frame(guest_in) == request
        os.write(guest_out, response)
        assert read_frame(host.fileno()) == response
    finally:
        cleanup(host, guest_in, guest_out, worker)


def test_bridge_rejects_wrong_fifo_direction_and_closes_owned():
    host, guest = local_pair()
    first_read, first_write = os.pipe()
    second_read, second_write = os.pipe()
    owned = (guest.detach(), first_read, second_read)
    try:
        with pytest.raises(ValueError, match="direction"):
            bridge.serve_bridge(*owned, BINDING, alive=lambda: True, seconds=1)
        for fd in owned:
            with pytest.raises(OSError):
                os.fstat(fd)
    finally:
        host.close()
        os.close(first_write)
        os.close(second_write)


def test_bridge_response_eof_is_unknown():
    host, guest_in, guest_out, owned, worker, errors = launch()
    try:
        host.sendall(frame({**BINDING, "sequence":1, "action":"start", "arguments":{}}))
        read_frame(guest_in)
        os.close(guest_out)
        guest_out = None
        worker.join(timeout=3)
        assert not worker.is_alive() and errors and isinstance(errors[0], EOFError)
    finally:
        host.close()
        worker.join(timeout=3)
        os.close(guest_in)
        if guest_out is not None:
            os.close(guest_out)


def test_bridge_does_not_claim_retained_alias_is_closed():
    host, guest = local_pair()
    alias = os.dup(guest.fileno())
    guest_in, bridge_out = os.pipe()
    bridge_in, guest_out = os.pipe()
    owned = (guest.detach(), bridge_out, bridge_in)
    errors = []
    def run():
        try:
            bridge.serve_bridge(*owned, BINDING, alive=lambda: True, seconds=2)
        except (EOFError, ValueError, PermissionError, TimeoutError, OSError) as error:
            errors.append(error)
    worker = threading.Thread(target=run)
    worker.start()
    try:
        host.shutdown(socket.SHUT_WR)
        worker.join(timeout=3)
        assert not worker.is_alive() and errors
        assert not select.select([host.fileno()], [], [], 0.1)[0]
        os.close(alias)
        alias = None
        assert select.select([host.fileno()], [], [], 1)[0]
        assert host.recv(1) == b""
    finally:
        host.close()
        if alias is not None:
            os.close(alias)
        os.close(guest_in)
        os.close(guest_out)



def test_bridge_partial_response_eof_does_not_forward():
    host, guest_in, guest_out, owned, worker, errors = launch()
    try:
        host.sendall(frame({**BINDING, "sequence":1, "action":"start", "arguments":{}}))
        read_frame(guest_in)
        os.write(guest_out, b'{"result":')
        os.close(guest_out)
        guest_out = None
        worker.join(timeout=3)
        assert not worker.is_alive() and errors and isinstance(errors[0], EOFError)
        assert host.recv(1024) == b""
    finally:
        host.close()
        worker.join(timeout=3)
        os.close(guest_in)
        if guest_out is not None:
            os.close(guest_out)


def test_bridge_invalid_fd_is_rejected_before_transfer():
    host, guest = local_pair()
    guest_in, bridge_out = os.pipe()
    owned_socket = guest.detach()
    try:
        with pytest.raises(OSError):
            bridge.serve_bridge(owned_socket, bridge_out, -1, BINDING, alive=lambda: True, seconds=1)
        os.fstat(owned_socket)
        os.fstat(bridge_out)
    finally:
        host.close()
        for fd in (owned_socket, guest_in, bridge_out):
            os.close(fd)



def test_bridge_rejects_same_named_fifo_when_identity_is_observable(tmp_path):
    host, guest = local_pair()
    path = tmp_path / "shared-fifo"
    os.mkfifo(path, 0o600)
    read_end = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
    write_end = os.open(path, os.O_WRONLY | os.O_NONBLOCK)
    owned = (guest.detach(), write_end, read_end)
    try:
        first, second = os.fstat(read_end), os.fstat(write_end)
        if (first.st_dev, first.st_ino) != (second.st_dev, second.st_ino):
            pytest.skip("named FIFO endpoints expose different inode identities")
        with pytest.raises(ValueError, match="distinct"):
            bridge.serve_bridge(*owned, BINDING, alive=lambda: True, seconds=1)
    finally:
        host.close()
        for fd in owned:
            try:
                os.close(fd)
            except OSError:
                pass


def test_bridge_invalid_binding_retains_untransferred_fds(monkeypatch):
    closed, receipt = [], bytearray(1)
    monkeypatch.setattr(bridge.os, "close", lambda fd: closed.append(fd))
    with pytest.raises(ValueError):
        bridge.serve_bridge(9001, 9002, 9003, {**BINDING, "nonce": "bad"},
                            alive=lambda: True, handoff=receipt)
    assert receipt == b"\x00" and closed == []


def test_bridge_closes_transferred_fds_after_type_rejection(monkeypatch):
    from types import SimpleNamespace
    closed, receipt = [], bytearray(1)
    monkeypatch.setattr(bridge.os, "fstat", lambda fd: SimpleNamespace(st_mode=0))
    monkeypatch.setattr(bridge.os, "close", lambda fd: closed.append(fd))
    with pytest.raises(ValueError, match="socket"):
        bridge.serve_bridge(9001, 9002, 9003, BINDING, alive=lambda: True, handoff=receipt)
    assert receipt == b"\x01" and closed == [9001, 9002, 9003]


def test_bridge_interrupt_before_take_keeps_caller_ownership(monkeypatch):
    closed, receipt = [], bytearray(1)
    monkeypatch.setattr(bridge.os, "fstat", lambda fd: (_ for _ in ()).throw(KeyboardInterrupt()))
    monkeypatch.setattr(bridge.os, "close", lambda fd: closed.append(fd))
    with pytest.raises(KeyboardInterrupt):
        bridge.serve_bridge(9001, 9002, 9003, BINDING, alive=lambda: True, handoff=receipt)
    assert receipt == b"\x00" and closed == []


def test_bridge_interrupt_after_take_closes_transferred_fds(monkeypatch):
    from types import SimpleNamespace
    calls, closed, receipt = [], [], bytearray(1)
    def fstat(fd):
        calls.append(fd)
        if len(calls) > 3:
            raise KeyboardInterrupt()
        return SimpleNamespace(st_mode=0)
    monkeypatch.setattr(bridge.os, "fstat", fstat)
    monkeypatch.setattr(bridge.os, "close", lambda fd: closed.append(fd))
    with pytest.raises(KeyboardInterrupt):
        bridge.serve_bridge(9001, 9002, 9003, BINDING, alive=lambda: True, handoff=receipt)
    assert receipt == b"\x01" and closed == [9001, 9002, 9003]
