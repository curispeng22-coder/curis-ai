import json
import subprocess
import sys
import time

import pytest

from app.agent_adapter import AgentExecutionError, CodexCliAdapter, validate_agent_manifest


def test_codex_adapter_separates_new_and_resume_access_snapshots(tmp_path):
    events = "\n".join(
        [
            json.dumps({"type": "thread.started", "thread_id": "thread-1"}),
            json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": "done"}}),
            json.dumps({"type": "turn.completed", "usage": {"input_tokens": 10, "output_tokens": 2}}),
        ]
    )
    commands = []

    def runner(command, **kwargs):
        commands.append(command)
        return subprocess.CompletedProcess(command, 0, events, "")

    adapter = CodexCliAdapter(
        cwd=str(tmp_path),
        requested_intent="AUTO_WITHIN_BOUNDARY",
        executable="/bin/echo",
        runner=runner,
    )
    first = adapter.execute("work")
    resumed = adapter.execute("continue", session_id=first["session_id"])
    assert first["output"] == "done"
    assert first["total_tokens"] == 12
    assert "--sandbox" in commands[0]
    assert "workspace-write" in commands[0]
    assert "--skip-git-repo-check" in commands[0]
    assert first["computer_access"]["requested_intent"] == "AUTO_WITHIN_BOUNDARY"
    assert first["computer_access"]["configured_state"] == "CONFIGURED"
    assert first["computer_access"]["effective_state"] == "UNKNOWN"
    assert first["computer_access"]["verification_state"] == "UNVERIFIED"
    assert first["computer_access"]["verified_at"] is None
    assert first["permissions"]["effective_state"] == "UNKNOWN"
    assert "resume" in commands[1]
    assert "--sandbox" not in commands[1]
    assert resumed["session_id"] == "thread-1"
    assert resumed["computer_access"]["configured_state"] == "NOT_CONFIGURABLE"
    assert resumed["computer_access"]["effective_state"] == "UNKNOWN"
    assert resumed["computer_access"]["verification_state"] == "UNVERIFIED"
    assert resumed["computer_access"]["drift"] == "RESUME_ACCESS_UNVERIFIED"
    assert resumed["computer_access"]["native_mapping"]["state"] == "NOT_CONFIGURABLE"


def test_codex_adapter_rejects_full_access_without_starting_a_process(tmp_path):
    calls = []

    def runner(command, **kwargs):
        calls.append(command)
        return subprocess.CompletedProcess(command, 0, "", "")

    adapter = CodexCliAdapter(
        cwd=str(tmp_path),
        requested_intent="REQUEST_WIDEST_NATIVE_ACCESS",
        executable="/bin/echo",
        runner=runner,
    )
    with pytest.raises(AgentExecutionError, match="does not support Full") as error:
        adapter.execute("work")

    assert calls == []
    snapshot = error.value.computer_access
    assert snapshot["configured_state"] == "UNSUPPORTED"
    assert snapshot["effective_state"] == "UNKNOWN"
    assert snapshot["verification_state"] == "NOT_APPLICABLE"
    assert snapshot["native_mapping"]["state"] == "UNSUPPORTED"
    assert snapshot["verified_at"] is None


def test_custom_manifest_keeps_only_opaque_references():
    manifest = validate_agent_manifest(
        {
            "id": "agent.example",
            "name": "Example",
            "adapter": "http",
            "capabilities": ["research"],
            "credential_ref": "vault://tenant/t/credential/c",
            "external_ref": "published-agent-1",
        }
    )
    assert "secret" not in manifest
    assert manifest["external_ref"] == "published-agent-1"


@pytest.mark.skip(reason="Real process execution is held until stop ownership is proven")
def test_owned_process_streams_progress_and_bounds_environment(tmp_path):
    seen = []
    adapter = CodexCliAdapter(cwd=str(tmp_path), environment={"PATH": "/usr/bin:/bin"}, on_progress=seen.append)
    script = "import json,os,sys; assert 'OPENAI_API_KEY' not in os.environ; print(json.dumps({'type':'turn.started'}),flush=True); assert sys.stdin.read()=='hello'; print(json.dumps({'type':'turn.completed'}))"
    result = adapter._run_process([sys.executable, "-I", "-S", "-B", "-c", script], input="hello", timeout=3)
    assert result.returncode == 0
    assert seen == ["turn.started", "turn.completed"]


@pytest.mark.skip(reason="Real process execution is held until stop ownership is proven")
def test_cancel_reaps_process_group_and_marks_effect_unknown(tmp_path):
    stop = []
    adapter = CodexCliAdapter(cwd=str(tmp_path), environment={"PATH": "/usr/bin:/bin"},
                             should_stop=lambda: bool(stop), on_progress=stop.append)
    marker = tmp_path / "late-effect"
    child = "import time,pathlib; time.sleep(0.7); pathlib.Path('late-effect').write_text('wrong')"
    script = f"import subprocess,sys,time; subprocess.Popen([sys.executable,'-I','-S','-B','-c',{child!r}]); print('{{\"type\":\"turn.started\"}}',flush=True); time.sleep(30)"
    started = time.monotonic()
    with pytest.raises(AgentExecutionError) as caught:
        adapter._run_process([sys.executable, "-I", "-S", "-B", "-c", script], input="", timeout=5)
    assert caught.value.status == "cancelled"
    assert caught.value.outbound_attempted
    assert time.monotonic() - started < 3
    time.sleep(0.8)
    assert not marker.exists()


def test_native_resume_without_current_access_never_starts_process(tmp_path, monkeypatch):
    adapter = CodexCliAdapter(cwd=str(tmp_path), executable=sys.executable, environment={})
    monkeypatch.setattr(subprocess, "Popen", lambda *a, **k: pytest.fail("resume spawned process"))
    with pytest.raises(AgentExecutionError) as caught:
        adapter.execute("continue", session_id="old-session")
    assert caught.value.status == "codex_execution_held"
    assert not caught.value.outbound_attempted


@pytest.mark.skip(reason="Real process execution is held until stop ownership is proven")
def test_output_flood_terminates_owned_process(tmp_path):
    adapter = CodexCliAdapter(cwd=str(tmp_path), environment={})
    with pytest.raises(AgentExecutionError) as caught:
        adapter._run_process([sys.executable, "-I", "-S", "-B", "-c", "import sys; sys.stdout.write('x' * (9*1024*1024))"], input="", timeout=4)
    assert caught.value.status == "response_invalid"


def test_real_execution_is_held_before_discovery_and_spawn(tmp_path, monkeypatch):
    import app.agent_adapter as module
    def unexpected(*args, **kwargs):
        pytest.fail("real execution or discovery was attempted")
    monkeypatch.setattr(module, "local_codex_executable", unexpected)
    monkeypatch.setattr(subprocess, "Popen", unexpected)
    adapter = CodexCliAdapter(cwd=str(tmp_path), environment={})
    with pytest.raises(AgentExecutionError, match="真实 Agent 执行暂不可用") as error:
        adapter.execute("work")
    assert error.value.status == "codex_execution_held"
    assert error.value.outbound_attempted is False


def test_stop_after_reservation_does_not_spawn(tmp_path, monkeypatch):
    states = iter([False, True])
    reserved = []
    monkeypatch.setattr(subprocess, 'Popen', lambda *a, **k: pytest.fail('spawn after stop'))
    adapter = CodexCliAdapter(cwd=str(tmp_path), environment={}, supervisor_command=['/test/supervisor'],
                              before_launch=lambda: reserved.append(True), should_stop=lambda: next(states))
    with pytest.raises(AgentExecutionError) as error:
        adapter._run_process_candidate(['/test/agent'], input='synthetic', timeout=2)
    assert reserved == [True]
    assert error.value.status == 'cancelled' and error.value.outbound_attempted is False


@pytest.mark.parametrize('stop_first', [True, False])
def test_owned_task_cancel_and_supervisor_spawn_are_serialized(tmp_path, monkeypatch, stop_first):
    import threading
    import app.agent_adapter as module
    from app.evolution_event_log import EvolutionEventLog
    from app.result_store import ResultStore
    from app.task_execution_control import TaskExecutionControlService
    from app.tenant_context import TenantContext
    from test_employee_execution_identity import _seed, TENANT, COMPANY

    db, _, _ = _seed(tmp_path / 'agent.sqlite')
    def scope():
        return TenantContext.scope(TENANT, company_id=COMPANY, ceo_id='ceo-trust', role='ceo')
    with scope():
        task = ResultStore(db).create_task('fixture', company_id=COMPANY)
        ResultStore(db).transition(task['task_id'], 'RUNNING')
    control = TaskExecutionControlService(db, EvolutionEventLog(db))
    before_spawn = threading.Event()
    attempted_spawn = threading.Event()
    allow_spawn_return = threading.Event()
    stop_entering = threading.Event()
    stop_finished = threading.Event()
    observed = {}

    def stopped():
        return control.get_state(task['task_id'])['task_status'] == 'CANCELLED'
    def fake_spawn(*_args, **_kwargs):
        attempted_spawn.set()
        if stop_first:
            raise AssertionError('spawn after committed stop')
        if not allow_spawn_return.wait(5):
            raise AssertionError('fixture spawn was not released')
        raise OSError('synthetic spawn outcome is unknown')
    monkeypatch.setattr(module.subprocess, 'Popen', fake_spawn)
    adapter = CodexCliAdapter(cwd=str(tmp_path), environment={}, supervisor_command=['fixture-supervisor'],
                              should_stop=stopped, before_launch=before_spawn.set)
    def launch():
        with scope():
            try:
                adapter._run_process_candidate(['fixture-agent'], input='fixture', timeout=2)
            except BaseException as error:
                observed['launch'] = error
    def stop():
        with scope():
            try:
                stop_entering.set()
                control.cancel(task['task_id'], 'fixture stop')
            except BaseException as error:
                observed['stop_error'] = error
            finally:
                stop_finished.set()

    if stop_first:
        with module._AGENT_STOP_SPAWN_LOCK:
            worker = threading.Thread(target=launch)
            worker.start()
            assert before_spawn.wait(5)
            stop()
        worker.join(5)
        assert not worker.is_alive() and not attempted_spawn.is_set()
        assert isinstance(observed.get('launch'), AgentExecutionError)
        assert observed['launch'].status == 'cancelled' and observed['launch'].outbound_attempted is False
    else:
        worker = threading.Thread(target=launch)
        worker.start()
        assert attempted_spawn.wait(5)
        stopper = threading.Thread(target=stop)
        stopper.start()
        assert stop_entering.wait(5)
        assert not stop_finished.wait(0.05)
        allow_spawn_return.set()
        worker.join(5); stopper.join(5)
        assert not worker.is_alive() and not stopper.is_alive()
        assert isinstance(observed.get('launch'), AgentExecutionError)
        assert observed['launch'].status == 'outcome_unknown' and observed['launch'].outbound_attempted is True
    assert stop_finished.is_set() and 'stop_error' not in observed
    with scope():
        assert control.get_state(task['task_id'])['task_status'] == 'CANCELLED'


def test_failed_final_stop_check_never_spawns(tmp_path, monkeypatch):
    calls = iter([False, RuntimeError('synthetic read failure')])
    def stop_check():
        value = next(calls)
        if isinstance(value, Exception):
            raise value
        return value
    monkeypatch.setattr(subprocess, 'Popen', lambda *_args, **_kwargs: pytest.fail('spawn after unreadable stop state'))
    adapter = CodexCliAdapter(cwd=str(tmp_path), environment={}, supervisor_command=['fixture-supervisor'],
                              should_stop=stop_check)
    with pytest.raises(RuntimeError, match='synthetic read failure'):
        adapter._run_process_candidate(['fixture-agent'], input='fixture', timeout=2)


def test_successful_fake_spawn_is_retained_before_task_cancel(tmp_path, monkeypatch):
    import threading
    from types import SimpleNamespace
    import app.agent_adapter as module
    from app.evolution_event_log import EvolutionEventLog
    from app.result_store import ResultStore
    from app.task_execution_control import TaskExecutionControlService
    from app.tenant_context import TenantContext
    from test_employee_execution_identity import _seed, TENANT, COMPANY

    db, _, _ = _seed(tmp_path / 'agent.sqlite')
    def scope():
        return TenantContext.scope(TENANT, company_id=COMPANY, ceo_id='ceo-trust', role='ceo')
    with scope():
        task = ResultStore(db).create_task('fixture', company_id=COMPANY)
        ResultStore(db).transition(task['task_id'], 'RUNNING')
    control = TaskExecutionControlService(db, EvolutionEventLog(db))
    process = SimpleNamespace(stdin=None, stdout=None, stderr=None, returncode=0)
    in_selector = threading.Event()
    release = threading.Event()
    observed = {}
    def fake_selector():
        in_selector.set()
        if not release.wait(5):
            raise AssertionError('fixture selector was not released')
        raise OSError('synthetic selector failure')
    monkeypatch.setattr(module.subprocess, 'Popen', lambda *_args, **_kwargs: process)
    monkeypatch.setattr(module.selectors, 'DefaultSelector', fake_selector)
    adapter = CodexCliAdapter(cwd=str(tmp_path), environment={}, supervisor_command=['fixture-supervisor'],
                              should_stop=lambda: control.get_state(task['task_id'])['task_status'] == 'CANCELLED')
    def launch():
        with scope():
            try:
                adapter._run_process_candidate(['fixture-agent'], input='fixture', timeout=2)
            except BaseException as error:
                observed['launch'] = error
    worker = threading.Thread(target=launch)
    worker.start()
    assert in_selector.wait(5)
    try:
        with module._UNRESOLVED_SUPERVISORS_LOCK:
            assert process in module._UNRESOLVED_SUPERVISORS
        with scope():
            control.cancel(task['task_id'], 'fixture stop')
    finally:
        release.set()
        worker.join(5)
    assert not worker.is_alive()
    assert isinstance(observed.get('launch'), AgentExecutionError)
    assert observed['launch'].status == 'outcome_unknown' and observed['launch'].outbound_attempted is True
    with module._UNRESOLVED_SUPERVISORS_LOCK:
        assert process not in module._UNRESOLVED_SUPERVISORS


def test_direct_process_entry_is_held(tmp_path, monkeypatch):
    monkeypatch.setattr(subprocess, "Popen", lambda *a, **k: pytest.fail("spawn attempted"))
    adapter = CodexCliAdapter(cwd=str(tmp_path), environment={})
    with pytest.raises(AgentExecutionError, match="真实 Agent 执行暂不可用") as error:
        adapter._run_process(["/bin/echo"], input="", timeout=1)
    assert error.value.status == "codex_execution_held"
    assert error.value.outbound_attempted is False


@pytest.mark.parametrize('case', ['valid', 'wrong_nonce', 'wrong_type', 'duplicate', 'truncated',
                                 'duplicate_key', 'oversize', 'invalid_pid', 'invalid_code', 'wrong_supervisor_exit'])
def test_child_exit_receipt_requires_owned_attempt_and_complete_message(case):
    import hashlib
    import signal
    from app.agent_adapter import _verified_child_exit_receipt
    nonce = 'ab' * 16
    value = {'type': 'curis.supervisor.child_reaped', 'nonce': nonce, 'child_pid': 123,
             'returncode': -signal.SIGTERM}
    if case == 'wrong_nonce': value['nonce'] = 'cd' * 16
    if case == 'wrong_type': value['type'] = 'other'
    if case == 'invalid_pid': value['child_pid'] = 1
    if case == 'invalid_code': value['returncode'] = True
    data = (json.dumps(value) + '\n').encode()
    if case == 'duplicate': data += data
    if case == 'duplicate_key': data = data.replace(b'"child_pid": 123', b'"child_pid": 123, "child_pid": 123')
    if case == 'truncated': data = data[:-1]
    if case == 'oversize': data = b'x' * 4097 + b'\n'
    result = _verified_child_exit_receipt(data, nonce, 0 if case == 'wrong_supervisor_exit' else -signal.SIGKILL)
    if case == 'valid':
        assert result == {'child_pid': 123, 'returncode': -signal.SIGTERM,
                          'attempt_sha256': hashlib.sha256(nonce.encode()).hexdigest()}
    else:
        assert result is None


@pytest.mark.parametrize('case', ['valid', 'wrong_nonce', 'truncated', 'duplicate', 'lost', 'timeout'])
def test_stop_receipt_is_only_recorded_after_owned_supervisor_wait(tmp_path, monkeypatch, case):
    import types
    import app.agent_adapter as module
    class Pipe:
        def __init__(self, number): self.number, self.closed = number, False
        def fileno(self): return self.number
        def close(self): self.closed = True
    class Process:
        def __init__(self):
            self.stdin, self.stdout, self.stderr = Pipe(10), Pipe(11), Pipe(12)
            self.returncode = None
        def terminate(self): pass
        def poll(self): return self.returncode
        def wait(self, timeout):
            if case == 'timeout': raise module.subprocess.TimeoutExpired('fixture', timeout)
            self.returncode = -module.signal.SIGKILL
            return self.returncode
    class Selector:
        def register(self, *_args): pass
        def get_map(self): return {1: True}
        def close(self): pass
    nonce = '78' * 16
    marker = {'type': 'curis.supervisor.child_reaped', 'nonce': '00' * 16 if case == 'wrong_nonce' else nonce,
              'child_pid': 123, 'returncode': -15}
    data = (json.dumps(marker) + '\n').encode()
    if case == 'truncated': data = data[:-1]
    if case == 'duplicate': data += data
    if case == 'lost': data = b''
    reads = [data, b'']
    recorded = []
    checks = iter([False, False, True])
    process = Process()
    monkeypatch.setattr(module.os, 'urandom', lambda _n: b'x' * 16)
    monkeypatch.setattr(module.os, 'set_blocking', lambda *_args: None)
    monkeypatch.setattr(module.os, 'read', lambda *_args: reads.pop(0))
    monkeypatch.setattr(module.selectors, 'DefaultSelector', Selector)
    monkeypatch.setattr(module.subprocess, 'Popen', lambda *_args, **_kwargs: process)
    monkeypatch.setattr(module, '_UNRESOLVED_SUPERVISORS', [])
    adapter = CodexCliAdapter(cwd=str(tmp_path), environment={}, supervisor_command=['fixture-supervisor'],
        should_stop=lambda: next(checks), on_local_state=recorded.append)
    with pytest.raises(AgentExecutionError) as error:
        adapter._run_process_candidate(['fixture-agent'], input='fixture', timeout=2)
    assert error.value.status == 'outcome_unknown' and error.value.outbound_attempted is True
    assert len(recorded) == (1 if case == 'valid' else 0)
    assert (module._UNRESOLVED_SUPERVISORS == [process]) is (case == 'timeout')


@pytest.mark.parametrize('case', ['already_exited', 'guard_refused', 'wait_unknown', 'receipt_callback_failed',
                                 'stop_interrupt', 'stdin_interrupt', 'wait_interrupt', 'receipt_interrupt',
                                 'selector_interrupt', 'stdout_interrupt', 'stop_system_exit'])
def test_stop_cleanup_closes_owned_channels_despite_guard_or_receipt_errors(tmp_path, monkeypatch, case):
    import app.agent_adapter as module
    events, recorded = [], []
    class Pipe:
        def __init__(self, number): self.number, self.closed = number, False
        def fileno(self): return self.number
        def close(self):
            events.append(('close', self.number))
            if case == 'stdin_interrupt' and self.number == 10 and events.count(('close', 10)) == 1:
                raise KeyboardInterrupt('stdin close interrupted')
            if case == 'stdout_interrupt' and self.number == 11:
                raise KeyboardInterrupt('stdout close interrupted')
            self.closed = True
    class Process:
        def __init__(self):
            self.stdin, self.stdout, self.stderr = Pipe(10), Pipe(11), Pipe(12)
            self.returncode = None
        def poll(self):
            if case == 'already_exited': self.returncode = -9
            return self.returncode
        def terminate(self):
            if case == 'already_exited': pytest.fail('already exited held process was signalled')
            events.append('stop-request')
            if case == 'guard_refused': raise RuntimeError('identity mismatch; no signal sent')
            if case == 'stop_interrupt': raise KeyboardInterrupt('stop interrupted')
            if case == 'stop_system_exit': raise SystemExit(7)
        def wait(self, timeout):
            assert ('close', 10) in events and 0 <= timeout <= 2
            events.append('wait')
            if case == 'wait_unknown': raise subprocess.TimeoutExpired('held supervisor', timeout)
            if case == 'wait_interrupt': raise KeyboardInterrupt('wait interrupted')
            self.returncode = -9
            return self.returncode
    class Selector:
        def register(self, *args): pass
        def get_map(self): return {1: True}
        def close(self):
            events.append('selector-closed')
            if case == 'selector_interrupt': raise KeyboardInterrupt('selector close interrupted')
    nonce = '78' * 16
    data = (json.dumps({'type': 'curis.supervisor.child_reaped', 'nonce': nonce,
                       'child_pid': 123, 'returncode': -15}) + '\n').encode()
    reads = [data, b'']
    stopped = iter([False, False, True])
    process = Process()
    monkeypatch.setattr(module.os, 'urandom', lambda _: b'x' * 16)
    monkeypatch.setattr(module.os, 'set_blocking', lambda *a: None)
    monkeypatch.setattr(module.os, 'read', lambda *a: reads.pop(0))
    monkeypatch.setattr(module.subprocess, 'Popen', lambda *a, **k: process)
    monkeypatch.setattr(module.selectors, 'DefaultSelector', Selector)
    monkeypatch.setattr(module, '_UNRESOLVED_SUPERVISORS', [])
    def record(value):
        recorded.append(value)
        if case == 'receipt_callback_failed': raise RuntimeError('receipt persistence unknown')
        if case == 'receipt_interrupt': raise KeyboardInterrupt('receipt persistence interrupted')
    adapter = CodexCliAdapter(cwd=str(tmp_path), environment={}, supervisor_command=['fixture-supervisor'],
                              should_stop=lambda: next(stopped), on_local_state=record)
    interrupted = case.endswith('_interrupt') or case == 'stop_system_exit'
    expected_error = SystemExit if case == 'stop_system_exit' else KeyboardInterrupt if interrupted else AgentExecutionError
    with pytest.raises(expected_error) as caught:
        adapter._run_process_candidate(['/synthetic/agent'], input='synthetic', timeout=2)
    if not interrupted:
        assert caught.value.status == 'outcome_unknown' and caught.value.outbound_attempted is True
    elif case == 'stop_system_exit':
        assert caught.value.code == 7
    assert all(('close', number) in events for number in (10, 11, 12))
    assert all(p.closed for p in (process.stdin, process.stdout, process.stderr) if not (case == 'stdout_interrupt' and p.number == 11))
    assert 'selector-closed' in events
    assert len(recorded) == (0 if case in {'wait_unknown', 'wait_interrupt'} else 1)
    assert module._UNRESOLVED_SUPERVISORS == ([] if case == 'already_exited' else [process])
    if case == 'guard_refused': assert events.count('stop-request') == 1 and 'wait' in events
    if interrupted: assert 'wait' in events
    assert module.CODEX_STOP_VERIFIED is False


@pytest.mark.parametrize("scenario", ["valid", "wrong_nonce", "duplicate", "cancel_at_wait", "cancel_during_read", "wait_unknown", "close_interrupted", "valid_after_release", "wrong_nonce_after_release", "cancel_during_cleanup"])
def test_unreleased_parent_protocol_checks_result_and_cancellation(tmp_path, monkeypatch, scenario):
    import types
    import app.agent_adapter as module

    class Pipe:
        def __init__(self, number):
            self.number, self.closed = number, False
        def fileno(self):
            return self.number
        def close(self):
            if scenario == "close_interrupted":
                raise KeyboardInterrupt()
            if scenario == "cancel_during_cleanup":
                stopped.append(True)
            self.closed = True

    class Process:
        def __init__(self):
            self.stdin, self.stdout, self.stderr = Pipe(10), Pipe(11), Pipe(12)
            self.returncode = None
            self.stop_requests = 0
        def terminate(self):
            self.stop_requests += 1
        def poll(self): return self.returncode
        def wait(self, timeout):
            if scenario == "wait_unknown":
                raise module.subprocess.TimeoutExpired("supervisor", timeout)
            self.returncode = -module.signal.SIGKILL
            if scenario == "cancel_at_wait":
                stopped.append(True)
            return self.returncode

    process, stopped, launch = Process(), [], []
    marker = {"type": "curis.supervisor.result", "nonce": "78" * 16, "returncode": 0}
    if scenario in {"wrong_nonce", "wrong_nonce_after_release"}:
        marker["nonce"] = "0" * 32
    status = (json.dumps(marker) + "\n").encode()
    if scenario == "duplicate":
        status += status
    reads = {11: [b"{}\n", b""], 12: [status, b""]}

    class Selector:
        def __init__(self):
            self.registered = {}
            self.order = iter([process.stdin, process.stdout, process.stderr, process.stdout, process.stderr])
        def register(self, pipe, event):
            self.registered[pipe.fileno()] = pipe
        def unregister(self, pipe):
            del self.registered[pipe.fileno()]
        def get_map(self):
            return self.registered
        def select(self, timeout):
            if scenario == "cancel_during_read":
                stopped.append(True)
            return [(types.SimpleNamespace(fileobj=next(self.order)), 0)]
        def close(self):
            pass

    monkeypatch.setattr(module.os, "urandom", lambda _: b"x" * 16)
    if scenario in {"valid_after_release", "wrong_nonce_after_release", "cancel_during_cleanup"}:
        monkeypatch.setattr(module, "CODEX_STOP_VERIFIED", True)
    monkeypatch.setattr(module, "_UNRESOLVED_SUPERVISORS", [])
    monkeypatch.setattr(module.os, "set_blocking", lambda *a: None)
    monkeypatch.setattr(module.os, "write", lambda fd, value: len(value))
    monkeypatch.setattr(module.os, "read", lambda fd, size: reads[fd].pop(0))
    monkeypatch.setattr(module.selectors, "DefaultSelector", Selector)
    monkeypatch.setattr(module.subprocess, "Popen", lambda *a, **kw: launch.append(kw) or process)
    monkeypatch.setattr(module.os, "killpg", lambda *a: pytest.fail("parent attempted a signal"))
    adapter = CodexCliAdapter(cwd=str(tmp_path), environment={}, supervisor_command=["/test/supervisor"],
                              should_stop=lambda: bool(stopped))
    if scenario == "close_interrupted":
        with pytest.raises(KeyboardInterrupt):
            adapter._run_process_candidate(["/test/agent"], input="test", timeout=2)
        assert module._UNRESOLVED_SUPERVISORS == [process]
        return
    if scenario == "valid_after_release":
        completed = adapter._run_process_candidate(["/test/agent"], input="test", timeout=2)
        assert completed.returncode == 0 and completed.stdout == "{}\n"
        assert module._UNRESOLVED_SUPERVISORS == [] and process.stop_requests == 0
        return
    with pytest.raises(AgentExecutionError) as error:
        adapter._run_process_candidate(["/test/agent"], input="test", timeout=2)
    assert error.value.outbound_attempted is True
    assert error.value.status == "outcome_unknown"
    assert process.stop_requests == (1 if scenario in {"cancel_during_read", "wait_unknown"} else 0)
    assert module._UNRESOLVED_SUPERVISORS == ([process] if scenario == "wait_unknown" else [])
    assert launch[0]["start_new_session"] is True and launch[0]["close_fds"] is True


@pytest.mark.parametrize('reason', ['cancel', 'deadline', 'parent_eof', 'term_ignored', 'wait_unknown', 'normal',
                                  'parent_budget', 'deadline_before_spawn', 'invalid_deadline'])
def test_supervisor_uses_owned_direct_child_cleanup_on_every_exit(tmp_path, monkeypatch, reason):
    import io
    import stat
    from types import SimpleNamespace
    import app.agent_adapter as module
    class Stream(io.StringIO):
        def fileno(self): return 2
    diagnostic = Stream()
    handlers, calls = {}, []
    clock = [0.0]
    class Child:
        pid = 123
        stdin = SimpleNamespace(fileno=lambda: 10, closed=False)
        def poll(self): return 0 if reason == 'normal' else None
        def terminate(self): calls.append('terminate')
        def kill(self): calls.append('kill')
        def wait(self, timeout):
            calls.append(('wait', timeout))
            assert 0 <= timeout <= 2
            if reason == 'wait_unknown' or (reason == 'term_ignored' and 'kill' not in calls):
                raise subprocess.TimeoutExpired('synthetic child', timeout)
            return -9 if 'kill' in calls else -15
    request = {'command': ['/synthetic/codex'], 'cwd': str(tmp_path), 'environment': {},
               'prompt': '', 'timeout': 2, 'nonce': 'ab' * 16}
    if reason == 'parent_budget': request['deadline'] = 1.5
    if reason == 'deadline_before_spawn': request['deadline'] = -1
    if reason == 'invalid_deadline': request['deadline'] = True
    selects = [0]
    def select_ready(*args):
        selects[0] += 1
        return ([7], [], []) if selects[0] == 1 or (selects[0] > 2 and reason == 'parent_eof') else ([], [], [])
    def spawn(*args, **kwargs):
        assert args[0] == request['command'] and kwargs['start_new_session'] is False
        assert kwargs['env'] == {} and kwargs['close_fds'] is True
        if reason in {'cancel', 'term_ignored', 'wait_unknown'}:
            handlers[module.signal.SIGTERM](None, None)
        elif reason == 'deadline':
            clock[0] = 1.01
        elif reason == 'parent_budget':
            clock[0] = 0.8
        return Child()
    monkeypatch.setattr(module.sys, 'stdin', SimpleNamespace(fileno=lambda: 7))
    monkeypatch.setattr(module.sys, 'stderr', diagnostic)
    monkeypatch.setattr(module.os, 'getpid', lambda: 456)
    monkeypatch.setattr(module.os, 'getsid', lambda _pid: 456)
    monkeypatch.setattr(module.os, 'getpgrp', lambda: 456)
    monkeypatch.setattr(module.os, 'fstat', lambda _fd: SimpleNamespace(st_mode=stat.S_IFIFO))
    monkeypatch.setattr(module.os, 'set_inheritable', lambda *a: None)
    monkeypatch.setattr(module.os, 'set_blocking', lambda *a: None)
    monkeypatch.setattr(module.os, 'read', lambda *a: (json.dumps(request) + '\n').encode())
    monkeypatch.setattr(module.time, 'monotonic', lambda: clock[0])
    monkeypatch.setattr(module.select, 'select', select_ready)
    monkeypatch.setattr(module.signal, 'signal', lambda number, handler: handlers.update({number: handler}))
    monkeypatch.setattr(module.subprocess, 'Popen', spawn)
    monkeypatch.setattr(module.os, 'killpg', lambda pgid, sig: calls.append(('group', pgid, sig)))
    code = module._run_agent_supervisor_candidate()
    if reason in {'deadline_before_spawn', 'invalid_deadline'}:
        assert code == (124 if reason == 'deadline_before_spawn' else 2)
        assert calls == [] and diagnostic.getvalue() == ''
        return
    assert calls[-1] == ('group', 0, module.signal.SIGKILL)
    if reason == 'normal':
        assert code == 0 and 'terminate' not in calls
        assert json.loads(diagnostic.getvalue())['type'] == 'curis.supervisor.result'
    else:
        assert code in {124, 130} and 'terminate' in calls
        if reason == 'wait_unknown':
            assert diagnostic.getvalue() == '', 'failed wait must never emit a reap receipt'
        else:
            value = json.loads(diagnostic.getvalue())
            assert value == {'type': 'curis.supervisor.child_reaped', 'nonce': request['nonce'],
                             'child_pid': 123, 'returncode': -9 if reason == 'term_ignored' else -15}


def test_reservation_delay_cannot_restart_the_original_process_budget(tmp_path, monkeypatch):
    import app.agent_adapter as module
    clock = [0.0]
    monkeypatch.setattr(module.time, 'monotonic', lambda: clock[0])
    monkeypatch.setattr(module.subprocess, 'Popen', lambda *a, **k: pytest.fail('expired launch created a process'))
    def reserve(): clock[0] = 90
    adapter = CodexCliAdapter(cwd=str(tmp_path), environment={}, supervisor_command=['fixture-supervisor'],
                              before_launch=reserve)
    with pytest.raises(AgentExecutionError) as caught:
        adapter._run_process_candidate(['/synthetic/codex'], input='synthetic', timeout=90)
    assert caught.value.status == 'cancelled' and caught.value.outbound_attempted is False


def test_candidate_admission_rejects_a_second_local_owner(tmp_path, monkeypatch):
    import app.agent_adapter as module
    monkeypatch.setattr(module, "CODEX_STOP_VERIFIED", True)
    monkeypatch.setattr(module, "_UNRESOLVED_SUPERVISORS", [])
    monkeypatch.setattr(module, "_SUPERVISOR_ADMISSION", module.threading.Lock())
    monkeypatch.setattr(module.subprocess, "Popen", lambda *a, **k: pytest.fail("spawn attempted"))
    adapter = CodexCliAdapter(cwd=str(tmp_path), environment={}, supervisor_command=["/test/supervisor"])
    assert module._SUPERVISOR_ADMISSION.acquire(blocking=False)
    try:
        with pytest.raises(AgentExecutionError) as error:
            adapter._run_process(["/test/agent"], input="test", timeout=2)
        assert error.value.status == "supervisor_unavailable"
        assert error.value.outbound_attempted is False
    finally:
        module._SUPERVISOR_ADMISSION.release()


def test_unresolved_supervisor_rejects_new_work_without_claiming_outcome(tmp_path, monkeypatch):
    import app.agent_adapter as module
    monkeypatch.setattr(module, "CODEX_STOP_VERIFIED", True)
    monkeypatch.setattr(module, "_UNRESOLVED_SUPERVISORS", [object()])
    monkeypatch.setattr(module.subprocess, "Popen", lambda *a, **k: pytest.fail("spawn attempted"))
    adapter = CodexCliAdapter(cwd=str(tmp_path), environment={}, supervisor_command=["/test/supervisor"])
    with pytest.raises(AgentExecutionError) as error:
        adapter._run_process(["/test/agent"], input="test", timeout=2)
    assert error.value.status == "supervisor_unavailable"
    assert error.value.outbound_attempted is False


def _fixture_verified_terminate(process, original, identity, terminate, diagnostics):
    observation = {'stage': 'stop-check', 'pid': process.pid, 'original_identity': original}
    diagnostics.append(observation)
    observation['poll_returncode'] = process.poll()
    if observation['poll_returncode'] is not None:
        observation['stage'] = 'already-exited-no-signal'
        return False
    observation['observed_identity'] = identity(process.pid)
    if observation['observed_identity'] != original:
        observation['poll_after_identity'] = process.poll()
        if observation['poll_after_identity'] is not None:
            observation['stage'] = 'exited-during-identity-check-no-signal'
            return False
        observation['stage'] = 'live-identity-refused-no-signal'
        raise RuntimeError('fixture supervisor identity changed; no signal sent')
    terminate()
    observation['stage'] = 'owned-termination-requested'
    return True


@pytest.mark.parametrize('case', ['already_exited', 'exited_during_check', 'live_mismatch', 'live_match'])
def test_fixture_stop_distinguishes_exit_from_live_identity_mismatch(case):
    from types import SimpleNamespace
    original = (123, 1, 501, 123, 100, 200)
    polls = iter([-9] if case == 'already_exited' else [None, -9] if case == 'exited_during_check' else [None, None])
    process = SimpleNamespace(pid=123, poll=lambda: next(polls))
    observations, signals = [], []
    def identity(pid):
        assert pid == 123
        if case == 'already_exited': pytest.fail('exited child queried for signal identity')
        return original if case == 'live_match' else None
    invoke = lambda: _fixture_verified_terminate(process, original, identity, lambda: signals.append(True), observations)
    if case == 'live_mismatch':
        with pytest.raises(RuntimeError, match='no signal sent'): invoke()
    else:
        assert invoke() is (case == 'live_match')
    assert signals == ([True] if case == 'live_match' else [])
    assert observations[0]['original_identity'] == original


@pytest.mark.parametrize('reason', ['cancel', 'timeout', 'parent_eof'])
def test_owned_supervisor_stops_after_real_task_cancel(tmp_path, monkeypatch, reason):
    """Opt-in fixture: production gate remains closed; no real Codex or network."""
    import ctypes
    import os
    from types import SimpleNamespace
    import app.agent_adapter as module
    from app.evolution_event_log import EvolutionEventLog
    from app.result_store import ResultStore
    from app.task_execution_control import TaskExecutionControlService
    from app.tenant_context import TenantContext
    from test_employee_execution_identity import _seed, TENANT, COMPANY, COMPANY_EMPLOYEE

    if os.environ.get("CURIS_AGENT_STOP_LIVE_FIXTURE") != "1":
        pytest.skip("Requires the dedicated one-shot owned-process release")
    assert module.CODEX_STOP_VERIFIED is False
    class BSDInfo(ctypes.Structure):
        _fields_ = [(n, ctypes.c_uint32) for n in
            ("flags", "status", "xstatus", "pid", "ppid", "uid", "gid", "ruid",
             "rgid", "svuid", "svgid", "reserved")] + [("comm", ctypes.c_char * 16), ("name", ctypes.c_char * 32)] + [
            (n, ctypes.c_uint32) for n in ("nfiles", "pgid", "pjobc", "tdev", "tpgid", "nice")] + [
            ("start_sec", ctypes.c_uint64), ("start_usec", ctypes.c_uint64)]
    def identity(pid):
        library = ctypes.CDLL("/usr/lib/libproc.dylib", use_errno=True)
        library.proc_pidinfo.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_uint64, ctypes.c_void_p, ctypes.c_int]
        info = BSDInfo()
        size = library.proc_pidinfo(pid, 3, 0, ctypes.byref(info), ctypes.sizeof(info))
        if size != ctypes.sizeof(info) or info.pid != pid or not info.start_sec:
            return None
        return (info.pid, info.ppid, info.uid, info.pgid, info.start_sec, info.start_usec)
    worker = """import sys

def guard(event,args):
    if event in {'subprocess.Popen','os.system','os.exec','os.posix_spawn','os.fork','os.forkpty','os.kill','os.killpg','socket.__new__'}:
        raise PermissionError('fixture worker cannot launch, signal or use sockets')
sys.addaudithook(guard)
import json,time
print(json.dumps({'type':'turn.started'}),flush=True)
time.sleep(4)
"""
    supervisor = """import sys,os,ctypes
worker=WORKER_SOURCE
class BSDInfo(ctypes.Structure):
    _fields_ = [(n, ctypes.c_uint32) for n in ('flags','status','xstatus','pid','ppid','uid','gid','ruid','rgid','svuid','svgid','reserved')] + [
        ('comm',ctypes.c_char*16),('name',ctypes.c_char*32)] + [(n,ctypes.c_uint32) for n in ('nfiles','pgid','pjobc','tdev','tpgid','nice')] + [
        ('start_sec',ctypes.c_uint64),('start_usec',ctypes.c_uint64)]
def guard(event,args):
    if event == 'subprocess.Popen' and args[1] != [sys.executable,'-I','-S','-B','-c',worker]:
        raise PermissionError('only the fixed fixture worker may launch')
    if event == 'os.killpg' and args != (0,9):
        raise PermissionError('only the current owned group may be signalled')
    if event == 'os.kill':
        pid, sig = args
        info=BSDInfo(); lib=ctypes.CDLL('/usr/lib/libproc.dylib',use_errno=True)
        lib.proc_pidinfo.argtypes=[ctypes.c_int,ctypes.c_int,ctypes.c_uint64,ctypes.c_void_p,ctypes.c_int]
        if (sig != 15 or lib.proc_pidinfo(pid,3,0,ctypes.byref(info),ctypes.sizeof(info)) != ctypes.sizeof(info)
                or info.pid != pid or info.ppid != os.getpid() or info.uid != os.getuid()
                or info.pgid != os.getpgrp() or not info.start_sec):
            raise PermissionError('only the verified owned direct child may be signalled')
    if event in {'os.system','os.exec','os.posix_spawn','os.fork','os.forkpty','socket.__new__'}:
        raise PermissionError('unexpected fixture process or network action')
sys.addaudithook(guard)
sys.path.insert(0,BACKEND_PATH)
from app.agent_adapter import _run_agent_supervisor_candidate
raise SystemExit(_run_agent_supervisor_candidate())
""".replace("WORKER_SOURCE", repr(worker)).replace("BACKEND_PATH", repr(str(__import__('pathlib').Path(__file__).resolve().parents[1])))
    expected = [sys.executable, "-I", "-S", "-B", "-c", supervisor]
    command = [sys.executable, "-I", "-S", "-B", "-c", worker]
    actual_popen = subprocess.Popen
    processes, terminations, reservations, local_evidence = [], [], [], []
    progress, eof_requests, diagnostics = [], [], []
    def owned_popen(argv, **kwargs):
        assert argv == expected and kwargs["cwd"] == str(tmp_path)
        assert kwargs["start_new_session"] is True and kwargs["close_fds"] is True
        process = actual_popen(argv, **kwargs)
        observation = {'stage': 'spawn', 'pid': process.pid}
        diagnostics.append(observation)
        try:
            original = identity(process.pid)
            observation['original_identity'] = original
            if (not original or original[1] != os.getpid() or original[2] != os.getuid()
                    or original[3] != process.pid or os.getsid(process.pid) != process.pid):
                raise RuntimeError("fixture supervisor ownership not established")
        except BaseException as error:
            # No identity means no signalling; close the held channel and wait.
            close_failed = False
            try:
                process.stdin.close()
            except Exception:
                close_failed = True
            try:
                process.wait(timeout=6)
            except Exception as wait_error:
                raise RuntimeError("fixture child exit UNKNOWN; no signal sent") from wait_error
            if close_failed:
                raise RuntimeError("fixture channel close UNKNOWN; no signal sent") from error
            raise
        actual_terminate = process.terminate
        def checked_terminate():
            if _fixture_verified_terminate(process, original, identity, actual_terminate, diagnostics):
                terminations.append(original)
        process.terminate = checked_terminate
        processes.append((process, original))
        return process
    db, _, _ = _seed(tmp_path / "stop-fixture.sqlite")
    with TenantContext.scope(TENANT, subject_id="fixture-subject", company_id=COMPANY, ceo_id="ceo-trust", role="ceo"):
        events = EvolutionEventLog(db)
        store = ResultStore(db, events)
        task = store.create_task("fixture", company_id=COMPANY, employee_id=COMPANY_EMPLOYEE,
            work_ref="work-a", capability_source="tenant_private", capability_type="agent", capability_id="agent.fixture")
        task_id = task["task_id"]
        control = TaskExecutionControlService(db, events)
        def stopped():
            return control.get_state(task_id)["task_status"] == "CANCELLED"
        def on_progress(kind):
            if kind == "turn.started" and not progress:
                progress.append(kind)
                if reason == 'cancel':
                    control.cancel(task_id)
                elif reason == 'parent_eof':
                    process, original = processes[0]
                    if identity(process.pid) != original:
                        raise RuntimeError('fixture supervisor identity changed; channel not closed')
                    process.stdin.close()  # EOF only; leave the actual parent alive and send no signal.
                    eof_requests.append(original)
        monkeypatch.setattr(module, "CODEX_STOP_VERIFIED", True)
        monkeypatch.setattr(module.subprocess, "Popen", owned_popen)
        adapter = CodexCliAdapter(cwd=str(tmp_path), environment={}, supervisor_command=expected,
            should_stop=stopped, on_progress=on_progress, before_launch=lambda: reservations.append(True),
            on_local_state=local_evidence.append)
        budget = 3 if reason == 'timeout' else 5
        started = time.monotonic()
        try:
            with pytest.raises(AgentExecutionError) as caught:
                adapter._run_process(command, input="fixture", timeout=budget)
        finally:
            print(json.dumps({'fixture_reason': reason, 'stage': 'post-attempt-observation',
                'elapsed_seconds': round(time.monotonic() - started, 6), 'held_identity_checks': diagnostics,
                'held_supervisors': [{'pid': process.pid, 'original_identity': original,
                                      'cached_returncode': process.returncode,
                                      'control_channel_closed': process.stdin.closed} for process, original in processes],
                'direct_receipts_observed': local_evidence,
                'descendants_and_external_effects': 'UNKNOWN'}), flush=True)
        elapsed = time.monotonic() - started
        assert caught.value.status == "outcome_unknown" and caught.value.outbound_attempted is True
        task_status = control.get_state(task_id)["task_status"]
        assert (task_status == "CANCELLED") is (reason == 'cancel')
        assert len(processes) == len(reservations) == len(progress) == 1
        assert elapsed < budget + 1, 'retain a late fixture as failure, never claim a hard realtime guarantee'
        if reason == 'cancel':
            assert len(terminations) == 1 and not eof_requests
        elif reason == 'timeout':
            assert not eof_requests and len(terminations) <= 1
            assert elapsed >= budget / 2 - 0.25, 'timeout must be driven by the original deadline'
        else:
            assert len(eof_requests) == 1 and not terminations, 'EOF must clean up without parent SIGTERM'
        assert processes[0][0].returncode == -9
        assert len(local_evidence) == 1 and local_evidence[0]['child_pid'] > 1
        assert local_evidence[0]['returncode'] == -15 and len(local_evidence[0]['attempt_sha256']) == 64
        if reason == 'cancel':
            with pytest.raises(AgentExecutionError) as replay:
                adapter._run_process(command, input="fixture", timeout=5)
            assert replay.value.status == "cancelled" and len(processes) == len(reservations) == 1
        print(json.dumps({'fixture_reason': reason, 'elapsed_seconds': round(elapsed, 6),
            'task_status': task_status, 'supervisor_returncode': processes[0][0].returncode,
            'direct_child_returncode': local_evidence[0]['returncode'],
            'attempt_sha256': local_evidence[0]['attempt_sha256'],
            'parent_term_requests': len(terminations), 'parent_eof_requests': len(eof_requests),
            'spawn_count': len(processes), 'codex_or_network': False,
            'gate_override_scope': 'TEST_PROCESS_ONLY', 'descendants_and_external_effects': 'UNKNOWN'}), flush=True)


@pytest.mark.parametrize('mode',['completed','cancelled','timeout','eof','no-proof'])
def test_container_adapter_keeps_result_behind_closed_receipt_and_never_reports_host_child(tmp_path,mode):
    from app.reader_vm_host import OwnedAgentContainerError
    events=[];cid='c'*64
    receipt={'ledger_state':'CLOSED_VERIFIED','container_id':cid,'exit_codes':{cid:137},'effects':'UNKNOWN','descendants':'UNKNOWN'}
    class Session:
        stop_receipt=None
        def run(self,command,**options):
            events.append('run')
            self.stop_receipt=None if mode=='no-proof' else receipt
            if mode in {'cancelled','timeout','eof'}:raise OwnedAgentContainerError(mode,receipt)
            return {'returncode':0,'stdout':'self-authored','stderr':''}
    adapter=CodexCliAdapter(cwd=str(tmp_path),container_session_factory=Session,
        before_launch=lambda:events.append('reserve'),on_local_state=lambda e:(_ for _ in ()).throw(AssertionError('false host child receipt')))
    adapter.on_container_state=lambda e:events.append('closed')
    if mode=='completed':
        result=adapter._run_container_process_candidate(['/usr/bin/python3','-I','-B','-c','print(1)'],input='',timeout=1)
        assert result.stdout=='self-authored' and events==['reserve','run','closed']
    else:
        with pytest.raises(AgentExecutionError) as error:
            adapter._run_container_process_candidate(['/usr/bin/python3','-I','-B','-c','print(1)'],input='',timeout=1)
        assert error.value.status=={'eof':'channel_closed','no-proof':'outcome_unknown'}.get(mode,mode)
        assert error.value.outbound_attempted is False


def test_public_container_execution_remains_held_before_reservation_or_allocation(monkeypatch,tmp_path):
    import app.agent_adapter as adapter_module
    monkeypatch.setattr(adapter_module,'CODEX_STOP_VERIFIED',True)
    monkeypatch.setattr(adapter_module,'AGENT_CONTAINER_EXECUTION_VERIFIED',False)
    def forbidden():raise AssertionError('allocated or reserved while held')
    adapter=CodexCliAdapter(cwd=str(tmp_path),container_session_factory=forbidden,before_launch=forbidden)
    with pytest.raises(AgentExecutionError) as error:
        adapter._run_process(['/usr/bin/python3','-I','-B','-c','print(1)'],input='',timeout=1)
    assert error.value.status=='container_execution_held'


def test_container_candidate_rejects_host_command_before_reserving_or_allocating(tmp_path):
    def forbidden():raise AssertionError('reserved or allocated unsupported host command')
    adapter=CodexCliAdapter(cwd=str(tmp_path),container_session_factory=forbidden,before_launch=forbidden)
    with pytest.raises(AgentExecutionError) as error:
        adapter._run_container_process_candidate(['/host/codex','exec'],input='',timeout=1)
    assert error.value.status=='configuration_rejected' and error.value.outbound_attempted is False


@pytest.mark.parametrize('authenticated',[True,False])
def test_linux_candidate_reserves_only_after_guest_auth_and_requires_closed_receipt(tmp_path,authenticated):
    from app.reader_vm_host import OwnedAgentContainerError
    events=[];cid='c'*64
    receipt={'ledger_state':'CLOSED_VERIFIED','container_id':cid,'exit_codes':{cid:0}}
    class Session:
        stop_receipt=receipt
        def run_linux_candidate(self,prompt,catalog,**kwargs):
            events.append('auth_check');assert events==['factory','auth_check']
            if not authenticated:raise OwnedAgentContainerError('authentication_required',receipt)
            kwargs['before_launch']();assert events[-1]=='reserve'
            assert kwargs['timeout']==80
            return {'returncode':0,'stdout':'bounded fixture','stderr':''}
    def factory():events.append('factory');return Session()
    adapter=CodexCliAdapter(cwd=str(tmp_path),container_session_factory=factory,before_launch=lambda:events.append('reserve'))
    catalog={'models':[{'slug':'gpt-5.6-sol','tool_mode':'code_mode_only','multi_agent_version':'v2','use_responses_lite':True}]}
    if authenticated:
        result=adapter._run_linux_container_candidate('fixture',catalog,timeout=90)
        assert result.stdout=='bounded fixture' and result.args==['/opt/curis/bin/codex']
    else:
        with pytest.raises(AgentExecutionError) as error:adapter._run_linux_container_candidate('fixture',catalog,timeout=90)
        assert error.value.status=='authentication_required' and not error.value.outbound_attempted
        assert 'reserve' not in events
    assert adapter.container_stop_receipt==receipt


def test_public_owned_linux_path_uses_pinned_guest_and_never_native_auth_or_executable(tmp_path,monkeypatch):
    import app.agent_adapter as module
    import app.reader_vm_host as host
    monkeypatch.setattr(module,'CODEX_STOP_VERIFIED',True)
    monkeypatch.setattr(module,'AGENT_CONTAINER_EXECUTION_VERIFIED',True)
    def forbidden(*a,**k):raise AssertionError('native lookup or sandbox must not run')
    monkeypatch.setattr(module,'local_codex_executable',forbidden)
    catalogue={'models':[{'slug':'gpt-5.6-sol','tool_mode':'code_mode_only','multi_agent_version':'v2','use_responses_lite':True}]}
    monkeypatch.setattr(host,'load_owned_linux_profile',lambda:{'modelCatalog':catalogue,'egressPurpose':'CODEX_PROVIDER_CONNECT_V1'})
    adapter=CodexCliAdapter(cwd=str(tmp_path),container_session_factory=lambda:None)
    adapter._prepare_model_profile=forbidden;adapter._native_file_profile=forbidden
    seen=[]
    def execute(prompt,catalog,**options):
        assert prompt=='original prompt' and catalog==catalogue;seen.append(True)
        return subprocess.CompletedProcess(['/opt/curis/bin/codex'],0,'\n'.join([
            json.dumps({'type':'thread.started','thread_id':'linux-fixture'}),
            json.dumps({'type':'item.completed','item':{'type':'agent_message','text':'bounded result'}}),
            json.dumps({'type':'turn.completed','usage':{'input_tokens':7,'output_tokens':2}})]),'')
    adapter._run_linux_container_candidate=execute
    result=adapter.execute('original prompt')
    assert seen==[True] and result['output']=='bounded result' and result['total_tokens']==9
    assert result['computer_access']['native_mapping']['sandbox']=='read-only'
    assert result['computer_access']['effective_state']=='UNKNOWN'
    assert result['native_model_profile']['runtime']=='LINUX_OWNED_CONTAINER'


@pytest.mark.parametrize("scenario", ["success", "usage", "foreign", "oversize", "permission", "cancel", "bad_version", "close_failure", "stderr_limit", "group_remains", "stdout_open", "timeout", "mcp", "spawn_unknown", "spawn_late", "byte_stdio", "account_success", "account_missing", "account_unconfirmed", "account_drift", "account_grouped"])
def test_acp_official_sdk_memory_protocol_and_owned_cleanup(tmp_path, monkeypatch, scenario):
    """Real fixed SDK messages; synthetic process only, no fork/socket/Agent."""
    import asyncio
    import signal
    from types import SimpleNamespace
    import app.agent_adapter as module
    import app.ai_capability_registry as registry
    import acp
    from acp import schema
    from acp.agent.connection import AgentSideConnection
    from acp._transport import memory_transport_pair
    events = []
    identity = {"agent_id": "deepseek_harness", "installation_ref": "a" * 64,
                "command": ["/synthetic/dsh", "--profile", "acp"], "version": "synthetic",
                "profile_directory": ".dsh/profiles/acp", "profile_environment": {"DSH_HOME": ".dsh"}}
    shared = scenario.startswith("account_")
    home = tmp_path / ("account-home" if shared else ".acp-home")
    (home / ".dsh/profiles/acp").mkdir(parents=True)
    if shared:
        monkeypatch.setattr(module.pwd, "getpwuid", lambda _uid: SimpleNamespace(pw_dir=str(home)))
    monkeypatch.setattr(module, "_UNRESOLVED_ACP_PROCESSES", [])
    monkeypatch.setattr(module, "ACP_LOCAL_EXECUTION_VERIFIED", True)  # Test only; source gate stays False.
    monkeypatch.setattr(registry, "acp_installation", lambda _agent: identity)
    stopped = {"value": False}
    adapter = module.AcpStdioAdapter(installation=identity, cwd=str(tmp_path), profile_home=str(home), shared_account=shared, timeout=4,
        should_stop=lambda: stopped["value"], before_launch=lambda: events.append("reserve"),
        on_progress=lambda stage: events.append(stage), on_local_state=lambda receipt: events.append(receipt))
    if scenario == "oversize": adapter.MAX_OUTPUT = 8
    def group_signal(pid, sig):
        assert pid == 80000001
        if sig == 0:
            if scenario == "group_remains": return
            raise ProcessLookupError()
        events.append(sig)
    monkeypatch.setattr(module.os, "killpg", group_signal)

    async def exercise():
        client_transport, agent_transport = memory_transport_pair()
        cancelled = asyncio.Event()
        peer = None
        account_value = json.dumps(["deepseek-account", "synthetic-account-model"])
        api_value = json.dumps(["deepseek-official", "synthetic-api-model"])
        def model_options(current):
            values = [schema.SessionConfigSelectOption(value=api_value, name="API"),
                      schema.SessionConfigSelectOption(value=account_value, name="Account")]
            if scenario == "account_missing": values = values[:1]
            if scenario == "account_grouped":
                values = [schema.SessionConfigSelectGroup(group="accounts", name="Models", options=values)]
            return [schema.SessionConfigOptionSelect(id="model", name="Model", type="select",
                current_value=current, options=values)]
        class Agent:
            async def initialize(self, protocol_version, client_capabilities=None, **kwargs):
                events.append("initialize")
                assert protocol_version == 1
                assert not client_capabilities.terminal
                return schema.InitializeResponse(protocol_version=2 if scenario == "bad_version" else 1,
                    agent_capabilities=schema.AgentCapabilities(mcp_capabilities=schema.McpCapabilities(http=True), session_capabilities=schema.SessionCapabilities(close=schema.SessionCloseCapabilities())), auth_methods=[])
            async def new_session(self, cwd, mcp_servers=None, **kwargs):
                assert cwd == str(tmp_path)
                if scenario == "mcp":
                    assert len(mcp_servers) == 1 and mcp_servers[0].url == adapter.tool_url
                    assert mcp_servers[0].headers[0].value == "Bearer synthetic-token"
                else: assert mcp_servers == []
                events.append("new")
                return schema.NewSessionResponse(session_id="session-synthetic", config_options=model_options(api_value) if shared else None)
            async def set_config_option(self, config_id, session_id, value, **kwargs):
                assert config_id == "model" and session_id == "session-synthetic" and value == account_value
                events.append("set_account_model")
                return schema.SetSessionConfigOptionResponse(config_options=model_options(
                    api_value if scenario == "account_unconfirmed" else account_value))
            async def prompt(self, session_id, prompt, **kwargs):
                events.append("prompt")
                assert session_id == "session-synthetic" and prompt[0].text == "work"
                if shared:
                    assert events.index("set_account_model") < events.index("acp.account_model.confirmed") < events.index("prompt")
                if scenario == "account_drift":
                    await peer.session_update(session_id=session_id, update=schema.ConfigOptionUpdate(
                        session_update="config_option_update", config_options=model_options(api_value)))
                if scenario == "permission":
                    result = await peer.request_permission(session_id=session_id,
                        tool_call=schema.ToolCallUpdate(tool_call_id="tool"),
                        options=[schema.PermissionOption(option_id="allow", kind="allow_once", name="Allow")])
                    assert result.outcome.outcome == "cancelled"
                    events.append("permission_denied")
                if scenario in {"cancel", "timeout"}:
                    stopped["value"] = scenario == "cancel"
                    await cancelled.wait()
                    return schema.PromptResponse(stop_reason="cancelled")
                await peer.session_update(session_id="foreign" if scenario == "foreign" else session_id,
                    update=schema.AgentMessageChunk(session_update="agent_message_chunk", content=acp.text_block("synthetic result")))
                return schema.PromptResponse(stop_reason="end_turn",
                    usage=schema.Usage(input_tokens=3, output_tokens=4, total_tokens=7) if scenario == "usage" else None)
            async def cancel(self, session_id, **kwargs):
                events.append("cancel"); cancelled.set()
            async def close_session(self, session_id, **kwargs):
                events.append("close_session")
                if scenario == "close_failure": raise acp.RequestError.method_not_found("session/close")
                return schema.CloseSessionResponse()
        if scenario == "byte_stdio":
            readers = [asyncio.StreamReader(limit=262144), asyncio.StreamReader(limit=262144)]
            protocols = [asyncio.StreamReaderProtocol(reader) for reader in readers]
            class Pipe(asyncio.Transport):
                def __init__(self, index): self.index, self.closed = index, False
                def is_closing(self): return self.closed
                def write(self, data): readers[1-self.index].feed_data(data)
                def get_extra_info(self, name, default=None): return default
                def close(self):
                    if not self.closed:
                        self.closed = True
                        readers[1-self.index].feed_eof()
                        protocols[self.index].connection_lost(None)
            pipes = [Pipe(0), Pipe(1)]
            for protocol, pipe in zip(protocols, pipes): protocol.connection_made(pipe)
            writers = [asyncio.StreamWriter(pipe, protocol, reader, asyncio.get_running_loop())
                       for pipe, protocol, reader in zip(pipes, protocols, readers)]
            peer = AgentSideConnection(Agent(), writers[1], readers[1], use_unstable_protocol=True)
        else:
            peer = AgentSideConnection(Agent(), agent_transport, use_unstable_protocol=True)
        class Process:
            pid = 80000001
            returncode = None
            def __init__(self):
                self.stdout = readers[0] if scenario == "byte_stdio" else asyncio.StreamReader()
                self.stderr = asyncio.StreamReader()
                if scenario not in {"stdout_open", "byte_stdio"}: self.stdout.feed_eof()
                if scenario == "stderr_limit": self.stderr.feed_data(b"s" * 17000)
                self.stderr.feed_eof()
                self.stdin = writers[0] if scenario == "byte_stdio" else SimpleNamespace(close=lambda: setattr(self, "returncode", 0))
            async def wait(self):
                while self.returncode is None:
                    if scenario == "byte_stdio" and self.stdin.is_closing(): self.returncode = 0
                    else: await asyncio.sleep(.001)
                return self.returncode
        process = Process()
        async def spawn(*command, **kwargs):
            assert command == tuple(identity["command"])
            assert kwargs["start_new_session"] is True and kwargs["limit"] == 262144
            assert kwargs["env"]["HOME"] == str(home)
            assert kwargs["env"]["DSH_HOME"] == str(home / ".dsh")
            assert "API_KEY" not in kwargs["env"] and "DSH_DESKTOP_NODE_EXECUTABLE" not in kwargs["env"]
            events.append("spawn")
            if scenario == "spawn_unknown": raise OSError("synthetic lost spawn response")
            if scenario == "spawn_late":
                await asyncio.sleep(adapter.timeout - 2 + .02)
                events.append("late_child_handle")
            return process
        if scenario == "mcp":
            adapter.tool_url = "http://127.0.0.1:8002/api/workspace/agent-tools"
            adapter.tool_token = "synthetic-token"
        adapter._spawn = spawn
        if scenario != "byte_stdio":
            adapter._connect = lambda client, _writer, _reader, **kwargs: acp.connect_to_agent(client, client_transport, **kwargs)
        try:
            if scenario in {"success", "usage", "permission", "mcp", "byte_stdio", "account_success", "account_grouped"}:
                result = await adapter._execute("work", adapter._preflight(), module._load_acp_sdk())
                assert result["output"] == "synthetic result" and result["session_id"] == "session-synthetic"
                assert result["total_tokens"] == (7 if scenario == "usage" else None)
                assert result["usage_basis"] == ("PROVIDER_REPORTED" if scenario == "usage" else "UNKNOWN")
                assert result["acp_cleanup"]["state"] == "CLOSED"
                assert result["acp_cleanup"]["external_effects"] == "UNKNOWN"
                if shared:
                    assert result["model_name"] == "synthetic-account-model"
                    assert result["agent_account_provider"] == "deepseek-account" and result["account_model_confirmed"]
            else:
                with pytest.raises(AgentExecutionError) as error:
                    await adapter._execute("work", adapter._preflight(), module._load_acp_sdk())
                assert error.value.outbound_attempted is True
                if scenario == "cancel":
                    assert events.index("cancel") < events.index("close_session")
                if scenario == "close_failure": assert adapter.cleanup["state"] == "UNKNOWN"
                if scenario in {"account_missing", "account_unconfirmed"}:
                    assert "prompt" not in events and "close_session" in events
        finally:
            await peer.close()
    asyncio.run(exercise())
    assert events[:2] == ["reserve", "spawn"]
    if scenario == "spawn_late":
        assert "late_child_handle" in events and "initialize" not in events and "prompt" not in events
        assert adapter.cleanup["parent_returncode"] == 0 and adapter.cleanup["stdout_eof"] and adapter.cleanup["stderr_eof"]
        assert module._UNRESOLVED_ACP_PROCESSES == []
    assert not any(isinstance(event, int) and event in (signal.SIGTERM, signal.SIGKILL) for event in events)


def test_acp_real_gate_rejects_before_install_sdk_allocation_or_reservation(tmp_path, monkeypatch):
    import app.agent_adapter as module
    def forbidden(*args, **kwargs): pytest.fail("allocation while held")
    monkeypatch.setattr(module, "_load_acp_sdk", forbidden)
    adapter = module.AcpStdioAdapter(installation={}, cwd=str(tmp_path), profile_home=str(tmp_path / ".acp-home"), before_launch=forbidden)
    adapter._spawn = forbidden
    with pytest.raises(AgentExecutionError) as error: adapter.execute("work")
    assert error.value.status == "acp_execution_held" and not error.value.outbound_attempted
    with pytest.raises(AgentExecutionError): adapter.execute("work", session_id="old")


def test_acp_shared_account_uses_only_os_default_home_without_opening_configuration(tmp_path, monkeypatch):
    from types import SimpleNamespace
    import app.agent_adapter as module
    import app.ai_capability_registry as registry
    home = tmp_path / "synthetic-account"
    (home / ".dsh").mkdir(parents=True)
    identity = {"agent_id": "deepseek_harness"}
    monkeypatch.setattr(module, "ACP_LOCAL_EXECUTION_VERIFIED", True)
    monkeypatch.setattr(module, "_UNRESOLVED_ACP_PROCESSES", [])
    monkeypatch.setattr(module.pwd, "getpwuid", lambda _uid: SimpleNamespace(pw_dir=str(home)))
    monkeypatch.setattr(registry, "acp_installation", lambda _agent: identity)
    monkeypatch.setenv("DSH_HOME", "/forged")
    monkeypatch.setenv("DEEPSEEK_API_KEY", "synthetic-not-forwarded")
    monkeypatch.setattr(module.Path, "open", lambda *_a, **_k: pytest.fail("Curis read configuration"))
    adapter = module.AcpStdioAdapter(installation=identity, cwd=str(tmp_path),
        profile_home=str(tmp_path / ".acp-home"), shared_account=True)
    env = adapter._preflight()
    assert env["HOME"] == str(home) and env["DSH_HOME"] == str(home / ".dsh")
    assert env["TMPDIR"] == str(tmp_path) and "DEEPSEEK_API_KEY" not in env
    assert not (home / ".dsh/profiles").exists()  # Only DSH may prepare its official profile.
    (home / ".dsh").chmod(0o777)
    with pytest.raises(AgentExecutionError): adapter._preflight()
    (home / ".dsh").chmod(0o700)
    (home / ".dsh").rmdir()
    with pytest.raises(AgentExecutionError) as missing: adapter._preflight()
    assert missing.value.status == "configuration_rejected" and not missing.value.outbound_attempted
    monkeypatch.setattr(module, "ACP_LOCAL_EXECUTION_VERIFIED", False)
    monkeypatch.setattr(module.pwd, "getpwuid", lambda _uid: pytest.fail("home lookup while held"))
    with pytest.raises(AgentExecutionError) as held: adapter._preflight()
    assert held.value.status == "acp_execution_held"
