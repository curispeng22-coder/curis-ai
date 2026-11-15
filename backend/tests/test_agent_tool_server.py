import base64
import hashlib
import json
from types import SimpleNamespace
import pytest

from app.agent_tool_server import AgentToolSessions
from app.agent_work_resources import AgentWorkResources
from app.skill_package import inspect_package, install_package
from backend.tests.test_skill_package import archive, REPO, COMMIT


def session(tmp_path, *, clock=lambda: 0, stop=lambda: False):
    manifest, files = inspect_package(REPO, COMMIT, "skills/research", fetch=lambda _: archive())
    package = {"manifest": manifest, "path": str(install_package(tmp_path / "packages", manifest, files)),
               "skill_template_id": "pinned-fixture"}
    resources = AgentWorkResources(tmp_path / "agent-work", tenant_id="tenant", company_id="company",
                                   work_ref="original-work", task_id="original-task")
    resources.prepare([package])
    server = AgentToolSessions(clock=clock)
    token = server.register(resources, [package], stop)
    return server, token, resources, manifest


def call(server, token, name, arguments):
    return server.handle(token, {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                                "params": {"name": name, "arguments": arguments}})["result"]


def test_task_tool_can_read_actual_pinned_skill_and_create_hash_bound_file(tmp_path):
    server, token, resources, manifest = session(tmp_path)
    read = call(server, token, "read_skill", {"package_sha256": manifest["package_sha256"], "path": "references/method.md"})
    assert not read["isError"] and "Preserve original URL" in read["content"][0]["text"]
    assert server.evidence(token)[0]["path"] == "references/method.md"
    raw = b"source,value\npublic,7\n"
    output = call(server, token, "write_output", {"name": "research.csv", "encoding": "base64",
                                                 "content": base64.b64encode(raw).decode()})
    assert not output["isError"]
    receipt = resources.collect()[0]
    assert receipt["sha256"] == hashlib.sha256(raw).hexdigest()
    assert resources.read_output(receipt) == raw
    assert receipt["work_ref"] == "original-work" and receipt["task_id"] == "original-task"
    assert call(server, token, "write_output", {"name": "research.csv", "encoding": "utf8", "content": "overwrite"})["isError"]
    assert resources.read_output(receipt) == raw


@pytest.mark.parametrize("name,args", [
    ("read_skill", {"package_sha256": "foreign-package", "path": "SKILL.md"}),
    ("read_skill", {"package_sha256": "known", "path": "../../auth.json"}),
    ("write_output", {"name": "../outside.csv", "encoding": "utf8", "content": "escape"}),
    ("browser", {"action": "navigate", "url": "https://example.com/"}),
    ("shell", {"command": "anything"}),
])
def test_task_tool_rejects_unbound_resources_and_unknown_actions(tmp_path, name, args):
    server, token, resources, manifest = session(tmp_path)
    if args.get("package_sha256") == "known":
        args = {**args, "package_sha256": manifest["package_sha256"]}
    assert call(server, token, name, args)["isError"]
    assert resources.collect() == []


def test_expiry_revocation_and_close_disable_same_token_without_new_task(tmp_path):
    now, revoked = [0], [False]
    server, token, _, _ = session(tmp_path, clock=lambda: now[0], stop=lambda: revoked[0])
    request = {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
    assert len(server.handle(token, request)["result"]["tools"]) == 2
    revoked[0] = True
    with pytest.raises(PermissionError):
        server.handle(token, request)
    revoked[0], now[0] = False, 90
    with pytest.raises(PermissionError):
        server.handle(token, request)
    now[0] = 0
    server.close(token)
    with pytest.raises(PermissionError):
        server.handle(token, request)


@pytest.mark.parametrize('cancel_first', [False, True])
def test_final_output_commit_and_cancel_have_one_local_order(tmp_path, monkeypatch, cancel_first):
    import threading
    import app.agent_tool_server as module
    from app.agent_adapter import _AGENT_STOP_SPAWN_LOCK
    stopped = [False]
    server, token, resources, _ = session(tmp_path, stop=lambda: stopped[0])
    entered, release, cancel_entered, cancelled = (threading.Event() for _ in range(4))
    result, errors = [], []
    original_call, original_write = server._call, module.write_output
    if cancel_first:
        def paused_call(*args):
            entered.set()
            assert release.wait(5)
            return original_call(*args)
        monkeypatch.setattr(server, '_call', paused_call)
    else:
        def paused_write(*args, **kwargs):
            entered.set()
            assert release.wait(5)
            return original_write(*args, **kwargs)
        monkeypatch.setattr(module, 'write_output', paused_write)
    def write():
        try:
            result.append(call(server, token, 'write_output', {'name': 'ordered.txt', 'encoding': 'utf8', 'content': 'synthetic'}))
        except Exception as error:
            errors.append(error)
    def cancel():
        cancel_entered.set()
        with _AGENT_STOP_SPAWN_LOCK:
            stopped[0] = True
            cancelled.set()
    writer = threading.Thread(target=write)
    writer.start()
    assert entered.wait(5)
    stopper = threading.Thread(target=cancel)
    stopper.start()
    assert cancel_entered.wait(5)
    try:
        if cancel_first:
            assert cancelled.wait(5)
        else:
            assert not cancelled.wait(0.05), 'cancel cannot commit in the middle of this backend write'
    finally:
        release.set()
        writer.join(5)
        stopper.join(5)
    assert not writer.is_alive() and not stopper.is_alive() and not errors
    assert cancelled.is_set() and len(result) == 1
    files = resources.collect()
    if cancel_first:
        assert result[0]['isError'] and files == []
    else:
        assert len(files) == 1 and resources.read_output(files[0]) == b'synthetic'
    with pytest.raises(PermissionError):
        call(server, token, 'write_output', {'name': 'after-stop.txt', 'encoding': 'utf8', 'content': 'late'})


def test_expiry_during_entered_write_retains_file_but_rejects_late_success(tmp_path, monkeypatch):
    import app.agent_tool_server as module
    now = [0]
    server, token, resources, _ = session(tmp_path, clock=lambda: now[0])
    original = module.write_output
    def expires(*args, **kwargs):
        receipt = original(*args, **kwargs)
        now[0] = 90
        return receipt
    monkeypatch.setattr(module, 'write_output', expires)
    response = call(server, token, 'write_output', {'name': 'entered.txt', 'encoding': 'utf8', 'content': 'already entered'})
    assert response['isError'] is True
    files = resources.collect()
    assert len(files) == 1 and resources.read_output(files[0]) == b'already entered'


def test_browser_receipt_records_successful_host_tool_call_without_page_body(tmp_path):
    server, _, resources, _ = session(tmp_path)
    closed = []
    browser = SimpleNamespace(session="owned-session", browser_id="owned-browser", tab=7,
        call=lambda arguments, original: {"url": "https://example.com/public", "tab_id": 7},
        close=lambda: closed.append(True))
    token = server.register(resources, [], lambda: False, browser=browser)
    assert server.browser_evidence(token) == []
    result = call(server, token, "browser", {"action": "navigate", "url": "https://example.com/public"})
    assert not result["isError"]
    receipt = server.browser_evidence(token)
    assert len(receipt) == 1 and receipt[0]["session_id"] == "owned-session"
    assert receipt[0]["content_verification"] == "UNVERIFIED"
    assert receipt[0]["result_sha256"] == hashlib.sha256(json.dumps(
        {"url": "https://example.com/public", "tab_id": 7}, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    assert token not in json.dumps(receipt) and "content" not in receipt[0]
    server.close(token)
    assert closed == [True] and server.browser_evidence(token) == []


def test_skill_tool_rechecks_exact_copied_bytes_and_does_not_execute_scripts(tmp_path):
    server, token, resources, manifest = session(tmp_path)
    original = resources.path / ".agents" / "skills" / manifest["package_sha256"] / "SKILL.md"
    original.chmod(0o600)
    original.write_text("tampered")
    assert call(server, token, "read_skill", {"package_sha256": manifest["package_sha256"], "path": "SKILL.md"})["isError"]
    script = call(server, token, "read_skill", {"package_sha256": manifest["package_sha256"], "path": "scripts/format.py"})
    assert not script["isError"] and "raise RuntimeError" in script["content"][0]["text"]
    assert resources.collect() == []

@pytest.mark.parametrize("reason", ["close", "stop", "expiry"])
def test_inflight_browser_response_is_rejected_after_session_loses_authority(tmp_path, reason):
    now, stopped = [0], [False]
    server, _, resources, _ = session(tmp_path, clock=lambda: now[0], stop=lambda: stopped[0])
    token = None
    def late(arguments, original):
        if reason == "close":
            server.close(token)
        elif reason == "stop":
            stopped[0] = True
        else:
            now[0] = 90
        return {"url": "https://example.com/public", "tab_id": 7}
    browser = SimpleNamespace(session="own", browser_id="own", tab=7, call=late, close=lambda: None)
    token = server.register(resources, [], lambda: stopped[0], browser=browser)
    result = call(server, token, "browser", {"action": "navigate", "url": "https://example.com/public"})
    assert result["isError"] is True
    assert server.browser_evidence(token) == []

def real_png():
    import struct
    import zlib
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)
    return (bytes.fromhex("89504e470d0a1a0a")
            + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(bytes([0, 255, 0, 0, 255])))
            + chunk(b"IEND", b""))

def test_capture_is_disabled_across_instances_and_ordinary_writes(tmp_path):
    from concurrent.futures import ThreadPoolExecutor
    from app.agent_tool_server import write_output
    server, token, resources, _ = session(tmp_path)
    second=AgentWorkResources(resources.path.parent, **resources.identity)
    png=real_png()
    with ThreadPoolExecutor(max_workers=2) as pool:
        denied=pool.submit(resources.begin_browser_capture)
        ordinary=pool.submit(write_output, second, "ordinary.png", png)
        with pytest.raises(ValueError, match="截图成果暂不可用"): denied.result()
        receipt=ordinary.result()
    assert "browser_capture" not in second.collect()[0]
    with pytest.raises(ValueError, match="截图成果暂不可用"):
        resources.register_browser_capture(receipt, url="https://example.com/", session_id="session", tab_id="tab")
    assert "browser_capture" not in resources.collect()[0]
    assert call(server, token, "register_browser_capture", {"relative_path":"ordinary.png"})["isError"]


def owner_tool_relay(tmp_path):
    server,token,resources,manifest=session(tmp_path)
    identity={**resources.identity,'employee_id':'employee','binding_ref':'binding'}
    relay=server.bind_owner_channel(token,identity)
    runtime={'nonce':'a'*48,'boot_id':'01234567-0123-0123-0123-0123456789ab',
             'container_id':'c'*64,'image_digest':'sha256:'+'b'*64}
    relay.bind(runtime)
    return server,token,resources,manifest,relay,identity,runtime


def relay_frame(identity,runtime,sequence,method,params=None):
    return {'identity':identity,**runtime,'sequence':sequence,
            'request':{'jsonrpc':'2.0','id':sequence,'method':method,'params':params or {}}}


def test_original_work_channel_descriptor_has_only_verified_relative_resource_metadata(tmp_path):
    server,token,resources,manifest,relay,identity,runtime=owner_tool_relay(tmp_path)
    descriptor=relay.descriptor
    raw=json.dumps(descriptor['resources'],sort_keys=True,separators=(',',':')).encode()
    assert descriptor['sha256']==hashlib.sha256(raw).hexdigest()
    assert str(tmp_path) not in raw.decode() and token not in raw.decode()
    assert descriptor['resources']['identity']==resources.identity
    assert descriptor['resources']['output_directory']=='output'
    files=descriptor['resources']['skills'][0]['files']
    assert files==[{k:item[k] for k in ('path','sha256','bytes')} for item in manifest['files']]
    read=relay.dispatch(relay_frame(identity,runtime,1,'tools/call',{'name':'read_skill','arguments':
        {'package_sha256':manifest['package_sha256'],'path':'references/method.md'}}))
    assert not read['response']['result']['isError'] and 'Preserve original URL' in json.dumps(read)
    saved=relay.dispatch(relay_frame(identity,runtime,2,'tools/call',{'name':'write_output','arguments':
        {'name':'channel.txt','encoding':'utf8','content':'original result'}}))
    assert not saved['response']['result']['isError']
    assert resources.read_output(resources.collect()[0])==b'original result'
    with pytest.raises(PermissionError):relay.dispatch(relay_frame(identity,runtime,2,'ping'))
    relay.revoke()
    with pytest.raises(PermissionError):server.handle(token,{'jsonrpc':'2.0','id':1,'method':'tools/list'})
    with pytest.raises(PermissionError):relay.dispatch(relay_frame(identity,runtime,3,'ping'))


@pytest.mark.parametrize('change',['tenant_id','company_id','work_ref','task_id','employee_id','binding_ref',
    'nonce','boot_id','container_id','image_digest','sequence','bool-sequence','extra','method','tool','oversize'])
def test_owner_tool_channel_rejects_cross_scope_runtime_replay_and_unbounded_surface(tmp_path,change):
    server,token,resources,manifest,relay,identity,runtime=owner_tool_relay(tmp_path)
    frame=relay_frame(dict(identity),runtime,1,'tools/list')
    if change in identity:frame['identity'][change]='foreign'
    elif change in runtime:frame[change]='foreign'
    elif change=='sequence':frame['sequence']=2
    elif change=='bool-sequence':frame['sequence']=True
    elif change=='extra':frame['token']=token
    elif change=='method':frame['request']['method']='resources/read'
    elif change=='tool':frame['request'].update(method='tools/call',params={'name':'shell','arguments':{}})
    elif change=='oversize':frame['request']['params']={'large':'x'*32768}
    with pytest.raises((PermissionError,ValueError)):relay.dispatch(frame)
    assert resources.collect()==[] and server.evidence(token)==[]


def test_work_owner_channel_cannot_be_bound_to_foreign_identity_or_rebound(tmp_path):
    server,token,resources,manifest=session(tmp_path)
    identity={**resources.identity,'employee_id':'employee','binding_ref':'binding'}
    with pytest.raises(PermissionError):server.bind_owner_channel(token,{**identity,'work_ref':'foreign'})
    relay=server.bind_owner_channel(token,identity)
    with pytest.raises(PermissionError):server.bind_owner_channel(token,identity)
    runtime={'nonce':'a'*48,'boot_id':'01234567-0123-0123-0123-0123456789ab',
             'container_id':'c'*64,'image_digest':'sha256:'+'b'*64}
    with pytest.raises(PermissionError):relay.bind({**runtime,'nonce':int('1'*48)})
    relay.bind(runtime)
    with pytest.raises(PermissionError):relay.bind(runtime)
    server.close(token)
    with pytest.raises(PermissionError):relay.dispatch(relay_frame(identity,runtime,1,'tools/list'))


def test_changed_pinned_resource_prevents_owner_channel_binding_and_revokes_token(tmp_path):
    server,token,resources,manifest=session(tmp_path)
    key=manifest['package_sha256'];path=resources.path/'.agents'/'skills'/key/manifest['files'][0]['path']
    path.chmod(0o600);path.write_bytes(b'changed fixture')
    identity={**resources.identity,'employee_id':'employee','binding_ref':'binding'}
    with pytest.raises(ValueError):server.bind_owner_channel(token,identity)
    with pytest.raises(PermissionError):server.handle(token,{'jsonrpc':'2.0','id':1,'method':'ping'})


def test_owner_tool_channel_rechecks_revocation_during_a_call_and_refuses_late_result(tmp_path):
    server,token,resources,manifest,relay,identity,runtime=owner_tool_relay(tmp_path)
    original=server.handle
    def stop_during_call(token,request):
        value=original(token,request);relay.revoke();return value
    server.handle=stop_during_call
    with pytest.raises(PermissionError):relay.dispatch(relay_frame(identity,runtime,1,'tools/list'))
    assert relay.revoked and resources.collect()==[]


def test_owned_container_execution_relays_only_bound_tools_then_original_result(tmp_path):
    import time
    import app.reader_vm_host as host
    server,token,resources,manifest=session(tmp_path)
    identity={**resources.identity,'employee_id':'employee','binding_ref':'binding'}
    relay=server.bind_owner_channel(token,identity)
    session_owner=host._OwnedAgentContainerSession(identity)
    owner=session_owner.owner
    owner.nonce='a'*48;owner.boot_id='01234567-0123-0123-0123-0123456789ab';owner.container_id='c'*64
    session_owner.bind_work_tools(relay)
    frame=owner.agent_frame(1,'execute',{})
    class Channel:
        calls=[]
        def request(self,frame):
            self.calls.append(frame)
            binding={k:v for k,v in frame.items() if k not in {'action','arguments'}}
            if frame['sequence']==1:
                return {**binding,'result':{'tool_request':relay_frame(identity,
                    {k:getattr(owner,k) for k in ('nonce','boot_id','container_id','image_digest')},1,'tools/list')}}
            assert frame['action']=='tool_response'
            assert [x['name'] for x in frame['arguments']['response']['result']['tools']]==['read_skill','write_output']
            return {**binding,'result':{'reason':'completed','returncode':0,'stdout':'done','stderr':''}}
    channel=Channel()
    response,last=session_owner._execute_with_tools(channel,frame,time.monotonic()+2)
    assert response['result']['stdout']=='done' and last['sequence']==2
    session_owner.revoke('eof')
    assert relay.revoked
    with pytest.raises(PermissionError):server.handle(token,{'jsonrpc':'2.0','id':1,'method':'ping'})


def test_browser_text_snapshot_is_host_written_and_bound_to_original_work(tmp_path):
    server, _, resources, _ = session(tmp_path)
    value = {"url": "https://example.com/public", "result": {"text": "controlled source text"}}
    browser = SimpleNamespace(identity=resources.identity, session="owned", browser_id="owned", tab=1,
        call=lambda arguments, original: value, close=lambda: None)
    token = server.register(resources, [], lambda: False, browser=browser)
    result = call(server, token, "browser", {"action": "observe"})
    assert not result["isError"]
    audit = server.browser_evidence(token)[0]
    assert audit["capture_kind"] == "HOST_BROWSER_TEXT_V1"
    assert audit["identity"] == resources.identity and audit["captured_at"].endswith("+00:00")
    raw = resources.read_output(audit["snapshot_receipt"])
    assert json.loads(raw) == value
    assert hashlib.sha256(raw).hexdigest() == audit["result_sha256"]
    # A model cannot supply trusted capture metadata through the browser schema.
    assert call(server, token, "browser", {"action": "observe", "captured_at": "forged"})["isError"]
    assert len(server.browser_evidence(token)) == 1



def test_browser_snapshot_refuses_foreign_work_before_file_creation(tmp_path):
    server, _, resources, _ = session(tmp_path)
    browser = SimpleNamespace(identity={**resources.identity, "work_ref": "foreign"}, session="owned", browser_id="owned", tab=1,
        call=lambda a, r: {"url": "https://example.com/public", "result": "text"}, close=lambda: None)
    token = server.register(resources, [], lambda: False, browser=browser)
    assert call(server, token, "browser", {"action": "observe"})["isError"]
    assert not resources.collect() and not server.browser_evidence(token)


@pytest.mark.parametrize('reason', ['url', 'stop', 'expiry'])
def test_text_capture_refuses_invalid_or_late_bytes_before_creating_file(tmp_path, reason):
    now, stopped = [0], [False]
    server, _, resources, _ = session(tmp_path, clock=lambda: now[0], stop=lambda: stopped[0])
    def capture(arguments, original):
        if reason == 'stop': stopped[0] = True
        if reason == 'expiry': now[0] = 90
        return {'url': 'file:///private/source' if reason == 'url' else 'https://example.org/public', 'result': {'text': 'fixture'}}
    browser = SimpleNamespace(identity=resources.identity, session='owned', browser_id='owned', tab=1, call=capture, close=lambda: None)
    token = server.register(resources, [], lambda: stopped[0], browser=browser)
    assert call(server, token, 'browser', {'action': 'observe'})['isError']
    assert resources.collect() == [] and server.browser_evidence(token) == []
