import json
import sqlite3
from contextlib import contextmanager
from types import SimpleNamespace

import pytest

from app.credential_vault import CredentialError, CredentialVaultService, CredentialWriteNotStarted
from app.tenant_context import TenantContext


IDENTITY = {"tenant_id": "synthetic-tenant", "company_id": "company", "work_ref": "work",
            "task_id": "task", "employee_id": "employee", "binding_ref": "binding"}


class AuthDatabase:
    def __init__(self, path):
        self.path = str(path)
        with self.connect() as connection:
            connection.execute("""create table credential_metadata (
                credential_id text primary key, tenant_id text, name text, provider text,
                credential_type text, credential_ref text, status text, encrypted_metadata text,
                created_at text default current_timestamp, updated_at text, disabled_at text)""")

    @contextmanager
    def connect(self):
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
        finally: connection.close()

    def list_credential_metadata(self, tenant):
        with self.connect() as connection:
            rows = connection.execute("select * from credential_metadata where tenant_id=?", (tenant,)).fetchall()
        return [{**dict(row), "encrypted_metadata": json.loads(row["encrypted_metadata"])} for row in rows]

    def get_credential_metadata(self, tenant, credential_id):
        return next((r for r in self.list_credential_metadata(tenant) if r["credential_id"] == credential_id), None)


class SyntheticKeychain:
    def __init__(self): self.items, self.events, self.on_store = {}, [], None
    def store(self, tenant, credential_id, secret):
        self.events.append(("store", tenant, credential_id))
        self.items[tenant, credential_id] = secret
        if self.on_store: self.on_store()
    def resolve(self, tenant, credential_id):
        self.events.append(("resolve", tenant, credential_id))
        return self.items[tenant, credential_id]
    def delete(self, tenant, credential_id):
        self.events.append(("delete", tenant, credential_id))
        self.items.pop((tenant, credential_id), None)
    def redact(self, value): return str(value)


@pytest.fixture
def owned_auth(tmp_path):
    database, keychain, audit = AuthDatabase(tmp_path / "owned-auth.sqlite"), SyntheticKeychain(), []
    service = CredentialVaultService(database, SimpleNamespace(record=lambda **kw: audit.append(kw)),
        environment="production", backend_mode="macos-keychain", vault_backend=keychain)
    with TenantContext.scope(IDENTITY["tenant_id"]): yield service, database, keychain, audit


def cache(version="A"):
    return json.dumps({"auth_mode": "chatgpt", "OPENAI_API_KEY": None, "last_refresh": "2026-11-04T00:00:00Z",
        "tokens": {"access_token": "SYNTHETIC_ACCESS_" + version, "refresh_token": "SYNTHETIC_REFRESH_" + version,
                   "id_token": "SYNTHETIC_ID_" + version, "account_id": "synthetic-account"}})


def binding(identity=None):
    return {"identity": dict(identity or IDENTITY), "nonce": "a" * 48, "parent_attempt": "b" * 48,
        "boot_id": "01234567-0123-0123-0123-0123456789ab", "container_id": "c" * 64, "image_digest": "sha256:" + "d" * 64}


def closed(runtime):
    child = {k: v for k, v in runtime.items() if k != "parent_attempt"}
    child.update(proxy_id="e" * 64, ledger_state="CLOSED_VERIFIED", exit_codes={"c" * 64: 0, "e" * 64: 0})
    return {"identity": runtime["identity"], "parent_attempt": runtime["parent_attempt"], "boot_id": runtime["boot_id"],
        "ledger_state": "CLOSED_VERIFIED", "children": [child]}


def connected(service):
    lease = service.begin_codex_lease("company", "capability", IDENTITY, intent="login")
    runtime = binding()
    assert lease.restore(runtime) is None
    lease.persist(runtime, cache(), authenticated=True)
    lease.finish(closed(runtime))
    return lease


def test_owned_cache_refresh_round_trip_uses_keychain_only_and_no_plaintext_metadata(owned_auth):
    service, database, keychain, audit = owned_auth
    first = connected(service)
    assert service.codex_connection("company", "capability")["state"] == "CONNECTED"
    identity = {**IDENTITY, "work_ref": "new-work", "task_id": "new-task"}
    lease = service.begin_codex_lease("company", "capability", identity)
    runtime = binding(identity)
    assert lease.restore(runtime) == cache()
    lease.persist(runtime, cache("B"), authenticated=True)
    assert service.codex_connection("company", "capability")["state"] == "CACHE_SAVED"
    lease.finish(closed(runtime))
    following = service.begin_codex_lease("company", "capability", IDENTITY)
    assert following.restore(binding()) == cache("B")
    following.abort()
    metadata = json.dumps(database.list_credential_metadata(IDENTITY["tenant_id"]))
    assert "SYNTHETIC_" not in metadata and "SYNTHETIC_" not in json.dumps(audit)
    assert set(keychain.items) == {(IDENTITY["tenant_id"], first.credential_id)}


def test_persisted_lease_blocks_second_service_before_any_secret_read(owned_auth):
    service, database, keychain, audit = owned_auth
    first = service.begin_codex_lease("company", "capability", IDENTITY, intent="login")
    other = CredentialVaultService(database, SimpleNamespace(record=lambda **kw: None),
        environment="production", backend_mode="macos-keychain", vault_backend=keychain)
    with pytest.raises(CredentialError): other.begin_codex_lease("company", "capability", IDENTITY, intent="login")
    assert not keychain.events
    first.abort()


@pytest.mark.parametrize("field", list(IDENTITY))
def test_restore_rejects_changed_original_identity_before_keychain_access(owned_auth, field):
    service, database, keychain, audit = owned_auth
    connected(service)
    lease = service.begin_codex_lease("company", "capability", IDENTITY)
    before = list(keychain.events)
    with pytest.raises(CredentialError): lease.restore(binding({**IDENTITY, field: "foreign"}))
    assert keychain.events == before
    lease.abort()


@pytest.mark.parametrize("field", ["nonce", "boot_id", "container_id", "image_digest", "parent_attempt"])
def test_writeback_rejects_changed_runtime_before_native_store(owned_auth, field):
    service, database, keychain, audit = owned_auth
    lease = service.begin_codex_lease("company", "capability", IDENTITY, intent="login")
    runtime = binding(); lease.restore(runtime)
    with pytest.raises(CredentialError): lease.persist({**runtime, field: "foreign"}, cache(), authenticated=True)
    assert not keychain.events
    lease.abort()


def test_uncertain_writeback_holds_connection_and_reconnect_never_restores_old_cache(owned_auth):
    service, database, keychain, audit = owned_auth
    original = connected(service)
    lease = service.begin_codex_lease("company", "capability", IDENTITY)
    runtime = binding(); assert lease.restore(runtime) == cache()
    keychain.on_store = lambda: (_ for _ in ()).throw(OSError("synthetic native result UNKNOWN"))
    with pytest.raises(CredentialError): lease.persist(runtime, cache("B"), authenticated=True)
    assert service.codex_connection("company", "capability")["state"] == "HELD"
    before = list(keychain.events)
    with pytest.raises(CredentialError): service.begin_codex_lease("company", "capability", IDENTITY)
    assert keychain.events == before
    new = service.begin_codex_lease("company", "capability", IDENTITY, intent="login", expected_generation=original.metadata["generation"])
    assert new.credential_id != original.credential_id and new.restore(binding()) is None
    assert keychain.events == before
    new.abort()


def test_cancel_is_immediate_and_cannot_reconnect_after_late_native_write(owned_auth):
    service, database, keychain, audit = owned_auth
    lease = service.begin_codex_lease("company", "capability", IDENTITY, intent="login")
    runtime = binding(); lease.restore(runtime)
    keychain.on_store = lease.cancel
    with pytest.raises(CredentialError): lease.persist(runtime, cache(), authenticated=True)
    with pytest.raises(CredentialError): lease.finish(closed(runtime))
    assert service.codex_connection("company", "capability")["state"] == "HELD"


@pytest.mark.parametrize("bad", ["{", "{}", '{"auth_mode":"chatgpt","auth_mode":"chatgpt"}', "x" * 32769])
def test_invalid_auth_cache_never_reaches_keychain(owned_auth, bad):
    service, database, keychain, audit = owned_auth
    lease = service.begin_codex_lease("company", "capability", IDENTITY, intent="login")
    runtime = binding(); lease.restore(runtime)
    with pytest.raises(CredentialError): lease.persist(runtime, bad, authenticated=True)
    assert not keychain.events
    lease.abort()


def test_disconnect_clears_only_owned_item_after_official_logout_and_closed_runtime(owned_auth):
    service, database, keychain, audit = owned_auth
    original = connected(service)
    lease = service.begin_codex_lease("company", "capability", IDENTITY, intent="disconnect")
    runtime = binding(); assert lease.restore(runtime) == cache()
    lease.persist(runtime, None, authenticated=False)
    lease.finish(closed(runtime))
    assert not keychain.items and service.codex_connection("company", "capability")["state"] == "DISCONNECTED"
    assert keychain.events[-1] == ("delete", IDENTITY["tenant_id"], original.credential_id)


@pytest.mark.parametrize("action", ["resolve", "update", "disable", "delete"])
def test_generic_vault_paths_cannot_expose_or_modify_managed_codex_cache(owned_auth, action):
    service, database, keychain, audit = owned_auth
    lease = connected(service); before = list(keychain.events)
    row = database.get_credential_metadata(IDENTITY["tenant_id"], lease.credential_id)
    with pytest.raises(CredentialError):
        getattr(service, action)(row["credential_ref"] if action == "resolve" else lease.credential_id)
    assert keychain.events == before
    with pytest.raises(CredentialWriteNotStarted): service.create(name="invalid", provider="codex-cli", credential_type="codex-managed-auth-v1", secret=cache())


@pytest.mark.parametrize("intent", ["login", "use", "status", "disconnect"])
@pytest.mark.parametrize("failure", [None, "foreign", "missing-writeback", "duplicate-writeback", "tool-after-writeback", "native-unknown", "cancel-writeback", "nonzero-completion", "coerced-authenticated"])
def test_original_pair_auth_rpc_keychain_roundtrip_and_physical_lock_span(owned_auth, monkeypatch, intent, failure):
    import test_reader_vm_host as fixtures
    from app import reader_vm_host as host
    service, database, keychain, audit = owned_auth
    if intent != "login": connected(service)
    monkeypatch.setattr(fixtures, "IDENTITY", IDENTITY)
    reader, unused, events, networks, containers, root, prefix = fixtures.paired_original_work_fixture(monkeypatch)
    base = host._DockerAttachChannel
    calls, reservations, sessions = [], [], []
    if failure == "native-unknown": keychain.on_store = lambda: (_ for _ in ()).throw(OSError("synthetic unknown native write"))
    class Channel(base):
        def request(self, frame):
            if "action" not in frame: return super().request(frame)
            action = frame["action"]; calls.append(action)
            bound = {k: v for k, v in frame.items() if k not in {"action", "arguments"}}
            if action == "bootstrap":
                assert frame["arguments"]["auth_mode"] == intent
                assert frame["arguments"]["auth_cache"] == (None if intent == "login" else cache())
                value = {"ready": True, "authenticated": intent != "login", "resource_sha256": frame["arguments"]["resources"]["sha256"],
                    "binary_sha256": "57a159f67999794494a172e71c12c6b5a211542ea90c66ea2ce9e6ac1edec6b1"}
                if failure == "coerced-authenticated": value["authenticated"] = int(value["authenticated"])
            elif action == "authenticate": value = {"device_login": {"verification_url": "https://auth.openai.com/codex/device", "user_code": "ABCD-1234"}}
            elif action == "login_ack": value = {"authenticated": True}
            elif action in {"execute", "auth_finish"}:
                assert action == ("execute" if intent == "use" else "auth_finish")
                assert bool(reservations) is (intent == "use")
                if failure == "missing-writeback": value = {"reason": "completed", "returncode": 0, "stdout": "unconfirmed", "stderr": ""}
                else: value = {"auth_writeback": {"authenticated": intent != "disconnect", "cache": None if intent == "disconnect" else cache("B")}}
                if failure == "foreign": bound["nonce"] = "f" * 48
                if failure == "cancel-writeback": lease.cancel()
            elif action == "auth_saved":
                assert frame["arguments"] == {"accepted": True}
                with pytest.raises(BlockingIOError): host._OwnerJournal()
                if failure == "duplicate-writeback": value = {"auth_writeback": {"authenticated": True, "cache": cache("B")}}
                elif failure == "tool-after-writeback": value = {"tool_request": {}}
                else: value = {"reason": "completed", "returncode": 1 if failure == "nonzero-completion" else 0, "stdout": "SYNTHETIC_ACCESS_B" if intent == "use" else json.dumps({"authenticated": intent != "disconnect", "operation": intent}), "stderr": ""}
            else: raise AssertionError(action)
            return {**bound, "result": value}
    monkeypatch.setattr(host, "_DockerAttachChannel", Channel)
    def run():
        nonlocal lease
        with host.original_work_owners(IDENTITY) as parent:
            parent.preflight(reader.image_digest)
            with service.begin_codex_lease("company", "capability", IDENTITY, intent=intent, parent=parent) as lease:
                try:
                    session = host._OwnedAgentContainerSession(IDENTITY, reader.image_digest, _linux_profile=True)
                    sessions.append(session)
                    parent.bind(session.owner, "agent"); session.bind_owned_auth(lease, "capability")
                    if intent == "use":
                        parent.bind(reader, "reader"); reader.prepare("a" * 48, hosts=["example.com"]); reader.start_runtime()
                        descriptor = {"resources": {"identity": {k: IDENTITY[k] for k in ("tenant_id", "company_id", "work_ref", "task_id")}, "skills": []}, "sha256": "d" * 64}
                        session.bind_work_tools(SimpleNamespace(identity=IDENTITY, descriptor=descriptor, bind=lambda runtime: None, revoke=lambda: None))
                        result = session.run_linux_candidate("synthetic", fixtures.linux_catalog_fixture(), timeout=2, should_stop=lambda: False, before_launch=lambda: reservations.append(True))
                    else:
                        result = session.run_linux_control(fixtures.linux_catalog_fixture(), timeout=2, should_stop=lambda: False, on_device_login=lambda challenge: True)
                    assert "SYNTHETIC_" not in result["stdout"]
                finally: parent.close(retain_lease=True)
                with pytest.raises(BlockingIOError): host._OwnerJournal()
            assert lease.finished and service.codex_connection("company", "capability")["state"] == ("DISCONNECTED" if intent == "disconnect" else "CONNECTED")
            with pytest.raises(BlockingIOError): host._OwnerJournal()
    lease = None
    # A logout performs a native delete, not a write; a synthetic store error is irrelevant to it.
    failed = failure is not None and not (failure == "native-unknown" and intent == "disconnect")
    if failed:
        with pytest.raises((CredentialError, host.OwnedAgentContainerError)): run()
        assert service.codex_connection("company", "capability")["state"] == "HELD"
    else:
        run()
        if intent != "disconnect": assert list(keychain.items.values()) == [cache("B")]
    assert networks == {} and all(not value["running"] for value in containers.values())
    assert sessions and "auth_cache" not in sessions[0].owner._linux_bootstrap
    journal = host._OwnerJournal(); journal.close()
    assert "SYNTHETIC_" not in json.dumps(database.list_credential_metadata(IDENTITY["tenant_id"]))


def test_normal_context_exit_cannot_silently_accept_cancelled_cache(owned_auth):
    service, database, keychain, audit = owned_auth
    with pytest.raises(CredentialError):
        with service.begin_codex_lease("company", "capability", IDENTITY, intent="login") as lease:
            lease.restore(binding()); lease.persist(binding(), cache(), authenticated=True); lease.cancel()
    assert service.codex_connection("company", "capability")["state"] == "HELD"


def auth_controller_namespace(service, monkeypatch):
    import ast, sys, threading, types
    from pathlib import Path
    from app.runtime import RuntimeScopeError
    # Execute the production nested handlers without importing main/create_app or opening a product DB.
    class HttpError(ValueError):
        def __init__(self, *, status_code, detail): self.status_code, self.detail = status_code, detail
    class Policy:
        def __init__(self, database): pass
        def actor(self, company):
            actor = TenantContext.current_identity()
            if company != "company" or actor["tenant_id"] != IDENTITY["tenant_id"] or actor["company_id"] not in {"", company}:
                raise RuntimeScopeError("synthetic denied owner")
        def agent_binding_snapshot(self, connection, company, binding_ref):
            if binding_ref not in {"binding", "other-binding"}: raise ValueError("synthetic unknown binding")
            return {"employee_ref": "employee", "capability_id": "capability"}
    module = types.ModuleType("app.company_execution_policy"); module.CompanyExecutionPolicy = Policy
    monkeypatch.setitem(sys.modules, "app.company_execution_policy", module)
    service.database.get_tenant_private_capability = lambda *args: {"metadata": {"kind": "codex-cli"}}
    namespace = {"__package__": "app", "TenantContext": TenantContext, "credential_vault": service,
        "database": service.database, "threading": threading, "codex_auth_lock": threading.RLock(),
        "codex_auth_runs": {}, "codex_auth_requests": set(), "HTTPException": HttpError,
        "RuntimeScopeError": RuntimeScopeError, "CodexConnectionIn": SimpleNamespace}
    names = {"agent_browser_target", "agent_auth_target", "codex_auth_actor", "codex_auth_state", "read_agent_auth",
        "begin_agent_auth", "connect_agent_auth", "disconnect_agent_auth", "track_owned_codex_session", "release_owned_codex_session", "close_owned_codex_sessions"}
    nodes = [node for node in ast.walk(ast.parse((Path(__file__).parents[1] / "app/main.py").read_text())) if isinstance(node, ast.FunctionDef) and node.name in names]
    assert len(nodes) == len(names)
    for node in nodes: node.decorator_list = []
    exec(compile(ast.Module(body=nodes, type_ignores=[]), "main-auth-controller", "exec"), namespace)
    return namespace


@pytest.mark.parametrize("change", ["role", "company", "tenant", "binding", "unreleased", "request", "backend"])
def test_auth_api_rejects_changed_scope_or_unreleased_profile_before_native_access(owned_auth, monkeypatch, change):
    from app import reader_vm_host as host
    service, database, keychain, audit = owned_auth
    ns = auth_controller_namespace(service, monkeypatch)
    def profile(**options):
        assert options == {"authentication": True}
        if change == "unreleased": raise ValueError("synthetic unreleased runtime")
        return {}
    monkeypatch.setattr(host, "load_owned_linux_profile", profile)
    if change == "backend": service.backend_mode = "local-dev"
    with TenantContext.scope("foreign" if change == "tenant" else IDENTITY["tenant_id"], role="member" if change == "role" else "ceo", company_id="company", subject_id="actor"):
        with pytest.raises(ns["HTTPException"]) as error:
            ns["connect_agent_auth"]("foreign" if change == "company" else "company", "unknown" if change == "binding" else "binding",
                SimpleNamespace(request_id="x" * 36 if change == "request" else "12345678-1234-1234-1234-123456789abc", expected_generation=None))
        assert error.value.status_code == 422 and "synthetic" not in error.value.detail
    assert not keychain.events and not database.list_credential_metadata(IDENTITY["tenant_id"]) and not ns["codex_auth_runs"]


def test_auth_api_challenge_actor_binding_and_original_work_disconnect_are_isolated(owned_auth, monkeypatch):
    import threading
    from app import reader_vm_host as host
    service, database, keychain, audit = owned_auth
    connected(service)
    ns = auth_controller_namespace(service, monkeypatch)
    monkeypatch.setattr(host, "load_owned_linux_profile", lambda **options: {})
    stopped = []
    with TenantContext.scope(IDENTITY["tenant_id"], role="ceo", company_id="company", subject_id="actor"):
        record = ns["track_owned_codex_session"](IDENTITY, "capability", None)
        session = SimpleNamespace(revoke=lambda reason: stopped.append(reason), _done=threading.Event(), _owned_auth=None)
        assert ns["track_owned_codex_session"](IDENTITY, "capability", session) is record
        assert ns["read_agent_auth"]("company", "binding")["state"] == "IN_USE"
        with pytest.raises(ValueError): ns["track_owned_codex_session"](IDENTITY, "capability", None)
        ns["release_owned_codex_session"](IDENTITY, "capability", dict(record))
        assert not record["done"].is_set()
        result = ns["disconnect_agent_auth"]("company", "binding", SimpleNamespace(request_id="12345678-1234-1234-1234-123456789abc", expected_generation=None))
        assert result["state"] == "DISCONNECTING" and stopped == ["cancelled"] and record["stop"].is_set()
        record["stop"].clear(); record.update(kind="connect", actor=ns["codex_auth_actor"](), challenge={"verification_url": "https://auth.openai.com/codex/device", "user_code": "ABCD-1234"})
        assert ns["read_agent_auth"]("company", "binding")["state"] == "WAITING_FOR_LOGIN"
        assert "user_code" not in ns["read_agent_auth"]("company", "other-binding")
        with TenantContext.scope(IDENTITY["tenant_id"], role="owner", company_id="company", subject_id="other-actor"):
            assert "user_code" not in ns["read_agent_auth"]("company", "binding")
        ns["release_owned_codex_session"](IDENTITY, "capability", record)
        assert record["done"].is_set()


def test_main_auth_shutdown_revokes_all_original_sessions_before_any_close(owned_auth, monkeypatch):
    service, database, keychain, audit = owned_auth
    ns = auth_controller_namespace(service, monkeypatch); events = []
    for index in range(2):
        session = SimpleNamespace(revoke=lambda reason, i=index: events.append(("revoke", i)), close=lambda i=index: events.append(("close", i)))
        ns["track_owned_codex_session"](IDENTITY, "capability-" + str(index), session)
    ns["close_owned_codex_sessions"]()
    assert events == [("revoke", 0), ("revoke", 1), ("close", 0), ("close", 1)]


def test_actual_auth_controller_worker_login_logout_replay_and_stale_generation(owned_auth, monkeypatch):
    import test_reader_vm_host as fixtures
    from app import reader_vm_host as host
    service, database, keychain, audit = owned_auth
    monkeypatch.setattr(fixtures, "IDENTITY", IDENTITY)
    reader, unused, events, networks, containers, root, prefix = fixtures.paired_original_work_fixture(monkeypatch)
    ns = auth_controller_namespace(service, monkeypatch)
    profile = {"imageDigest": reader.image_digest, "modelCatalog": fixtures.linux_catalog_fixture()}
    monkeypatch.setattr(host, "load_owned_linux_profile", lambda **options: profile)
    base = host._DockerAttachChannel
    class Channel(base):
        def request(self, frame):
            if "action" not in frame: return super().request(frame)
            binding = {k: v for k, v in frame.items() if k not in {"action", "arguments"}}
            action = frame["action"]
            if action == "bootstrap":
                self.mode = frame["arguments"]["auth_mode"]
                assert frame["arguments"]["auth_cache"] == (None if self.mode == "login" else cache())
                value = {"ready": True, "authenticated": self.mode != "login", "resource_sha256": frame["arguments"]["resources"]["sha256"],
                    "binary_sha256": "57a159f67999794494a172e71c12c6b5a211542ea90c66ea2ce9e6ac1edec6b1"}
            elif action == "authenticate": value = {"device_login": {"verification_url": "https://auth.openai.com/codex/device", "user_code": "ABCD-1234"}}
            elif action == "login_ack": value = {"authenticated": True}
            elif action == "auth_finish": value = {"auth_writeback": {"authenticated": self.mode == "login", "cache": cache() if self.mode == "login" else None}}
            elif action == "auth_saved": value = {"reason": "completed", "returncode": 0, "stdout": json.dumps({"authenticated": self.mode == "login", "operation": self.mode}), "stderr": ""}
            else: raise AssertionError("Authentication controller must never issue a model/tool request")
            return {**binding, "result": value}
    monkeypatch.setattr(host, "_DockerAttachChannel", Channel)
    key = (IDENTITY["tenant_id"], "company", "capability")
    def control(operation, request_id, generation=None):
        result = ns[operation + "_agent_auth"]("company", "binding", SimpleNamespace(request_id=request_id, expected_generation=generation))
        record = ns["codex_auth_runs"][key]; record["thread"].join(2)
        assert record["done"].is_set() and record["session"] is None
        return ns["read_agent_auth"]("company", "binding")
    with TenantContext.scope(IDENTITY["tenant_id"], role="ceo", company_id="company", subject_id="actor"):
        request = "12345678-1234-1234-1234-123456789abc"
        state = control("connect", request); assert state["state"] == "CONNECTED"
        assert "challenge" not in ns["codex_auth_runs"][key]
        before = list(keychain.events)
        with pytest.raises(ns["HTTPException"]): control("connect", request)
        assert keychain.events == before
        stale = control("disconnect", "12345678-1234-1234-1234-123456789abd", "f" * 48)
        assert stale["state"] == "CONNECTED" and keychain.events == before
        state = control("disconnect", "12345678-1234-1234-1234-123456789abe", state["generation"])
        assert state["state"] == "DISCONNECTED" and not keychain.items
    assert networks == {} and all(not value["running"] for value in containers.values())


@pytest.mark.parametrize("cancel_after_result", [False, True])
def test_actual_main_original_work_reader_agent_auth_and_close_order(owned_auth, monkeypatch, cancel_after_result):
    import ast, hashlib, os, sys, types
    from pathlib import Path
    import test_reader_vm_host as fixtures
    from app import reader_vm_host as host
    import app.agent_browser_runtime as browser_runtime
    from app.agent_adapter import CodexCliAdapter
    from app.agent_tool_server import AgentToolSessions
    service, database, keychain, audit = owned_auth
    connected(service)
    monkeypatch.setattr(fixtures, "IDENTITY", IDENTITY)
    reader, unused, events, networks, containers, root, prefix = fixtures.paired_original_work_fixture(monkeypatch)
    ns = auth_controller_namespace(service, monkeypatch)
    monkeypatch.setattr(host, "load_owned_linux_profile", lambda **options: {"imageDigest": reader.image_digest})
    base = host._DockerAttachChannel
    class Channel(base):
        def request(self, frame):
            if "action" not in frame: return super().request(frame)
            bound = {k: v for k, v in frame.items() if k not in {"action", "arguments"}}
            if frame["action"] == "bootstrap":
                assert frame["arguments"]["auth_cache"] == cache() and frame["arguments"]["auth_mode"] == "use"
                value = {"ready": True, "authenticated": True, "resource_sha256": frame["arguments"]["resources"]["sha256"],
                    "binary_sha256": "57a159f67999794494a172e71c12c6b5a211542ea90c66ea2ce9e6ac1edec6b1"}
            elif frame["action"] == "execute": value = {"auth_writeback": {"authenticated": True, "cache": cache("B")}}
            elif frame["action"] == "auth_saved": value = {"reason": "completed", "returncode": 0, "stdout": "synthetic result", "stderr": ""}
            else: raise AssertionError(frame["action"])
            return {**bound, "result": value}
    monkeypatch.setattr(host, "_DockerAttachChannel", Channel)
    def opened(identity):
        assert identity == IDENTITY
        session = host._OwnedAgentContainerSession(identity, reader.image_digest, _linux_profile=True)
        host._WORK_OWNER_SCOPE.get().bind(session.owner, "agent")
        return session
    monkeypatch.setattr(host, "open_owned_agent_container", opened)
    work = {"data": {"cycleRef": "cycle"}}
    cycle = {"data": {"contract": {"agentBrowser": {"hosts": ["example.com"]}}}}
    class Foundation:
        def __init__(self, db): pass
        def get(self, ref): return work if ref == "work" else cycle
    for name, attributes in [("app.runtime", {"RuntimeFoundation": Foundation}),
        ("app.api.team_operating_router", {"verified_prior_for_work": lambda *args: None, "prior_binding_digest": lambda value: "none"}),
        ("app.conversation_service", {"ConversationService": lambda db: SimpleNamespace(foundation=Foundation(db))})]:
        module = types.ModuleType(name); module.__dict__.update(attributes); monkeypatch.setitem(sys.modules, name, module)
    class Browser:
        def close(self):
            reader.revoke_bound_and_stop(reader.identity, reader.nonce, {"complete": False, "executionAuthorized": False,
                "boot_id": reader.boot_id, "container_id": reader.container_id, "image_digest": reader.image_digest})
    def open_browser(identity, hosts, should_stop):
        assert identity == IDENTITY and not should_stop()
        parent = host._WORK_OWNER_SCOPE.get(); parent.bind(reader, "reader"); reader.prepare("a" * 48, hosts=hosts); reader.start_runtime()
        return Browser()
    monkeypatch.setattr(browser_runtime, "load_trusted_reader_lock", lambda: {"runtimeKind": "VM"})
    monkeypatch.setattr(browser_runtime, "open_reader_for_work", open_browser)
    identity = {k: IDENTITY[k] for k in ("tenant_id", "company_id", "work_ref", "task_id")}
    data = {"identity": identity, "skills": []}
    descriptor = {"resources": data, "sha256": hashlib.sha256(json.dumps(data, sort_keys=True, separators=(',', ':')).encode()).hexdigest()}
    resources = SimpleNamespace(identity=identity, path=Path('/synthetic-owned/work'), owner_channel_descriptor=lambda manifests: descriptor,
        prepare=lambda packages, **options: {"environment": {}, "receipt": {"skills": []}})
    reservations = []
    def reserve():
        assert service.codex_connection("company", "capability")["state"] == "LEASED"
        assert len(containers) == 4 and all(value["running"] for value in containers.values())
        reservations.append(True)
    def build(metadata, **options):
        executor = object.__new__(CodexCliAdapter)
        def execute(prompt):
            result = executor.container_session_factory().run_linux_candidate(prompt, fixtures.linux_catalog_fixture(), timeout=2,
                should_stop=options["execution_context"]["should_stop"], before_launch=options["execution_context"]["before_launch"])
            return result
        executor.execute = execute
        return executor
    key = (IDENTITY["tenant_id"], "company", "capability")
    def accept(response, scoped, token, executor):
        assert response["stop_receipt"]["ledger_state"] == "CLOSED_VERIFIED"
        assert service.codex_connection("company", "capability")["state"] == "CACHE_SAVED"
        with pytest.raises(BlockingIOError): host._OwnerJournal()
        if cancel_after_result: ns["codex_auth_runs"][key]["session"].revoke("cancelled")
        return response
    tools = AgentToolSessions()
    ns.update(Path=Path, os=os, json=json, require_agent_position=lambda capability: None,
        runtime_capability={"id": "capability", "company_id": "company", "work_ref": "work"}, metadata={"kind": "codex-cli"},
        agent_task="task", agent_employee="employee", agent_binding="binding", resources=resources, packages=[], database=database,
        agent_stopped=lambda: False, agent_tools=tools, build_agent_executor=build, resolved_api_key=None, default_executor=None,
        agent_progress=lambda *args: None, agent_local_state=lambda *args: None, allowance={"max_seconds": 90},
        accept_agent_response=accept, reserve_original_agent_call=reserve, event_log=SimpleNamespace(record=lambda **kwargs: None))
    node = next(n for n in ast.walk(ast.parse((Path(__file__).parents[1] / "app/main.py").read_text())) if isinstance(n, ast.FunctionDef) and n.name == "run_scoped_agent")
    exec(compile(ast.Module(body=[node], type_ignores=[]), "main-original-codex-work", "exec"), ns)
    if cancel_after_result:
        with pytest.raises(CredentialError): ns["run_scoped_agent"]("synthetic original Work")
        assert service.codex_connection("company", "capability")["state"] == "HELD"
    else:
        result = ns["run_scoped_agent"]("synthetic original Work")
        assert result["stdout"] == "synthetic result" and service.codex_connection("company", "capability")["state"] == "CONNECTED"
    assert reservations == [True] and tools.sessions == {} and ns["codex_auth_runs"][key]["done"].is_set()
    assert networks == {} and all(not value["running"] for value in containers.values())
    journal = host._OwnerJournal(); journal.close()


def test_unresolved_metadata_can_reseed_only_after_new_parent_verifies_both_histories(owned_auth, monkeypatch):
    import test_reader_vm_host as fixtures
    from app import reader_vm_host as host
    service, database, keychain, audit = owned_auth
    monkeypatch.setattr(fixtures, "IDENTITY", IDENTITY)
    reader, unused, events, networks, containers, root, prefix = fixtures.paired_original_work_fixture(monkeypatch)
    with host.original_work_owners(IDENTITY) as old_parent:
        old_parent.preflight(reader.image_digest)
        old = service.begin_codex_lease("company", "capability", IDENTITY, intent="login", parent=old_parent)
        with pytest.raises(BlockingIOError): host._OwnerJournal()
    fresh = {**IDENTITY, "work_ref": "fresh-login", "task_id": "fresh-login-task"}
    with pytest.raises(CredentialError):
        service.begin_codex_lease("company", "capability", fresh, intent="login", expected_generation=old.metadata["generation"])
    with host.original_work_owners(fresh) as parent:
        assert not parent.can_reseed()
        parent.preflight(reader.image_digest); assert parent.can_reseed()
        replacement = service.begin_codex_lease("company", "capability", fresh, intent="login", expected_generation=old.metadata["generation"], parent=parent)
        assert replacement.credential_id != old.credential_id and replacement.metadata["generation"] != old.metadata["generation"]
        assert replacement.restore(binding(fresh)) is None
        replacement.abort()
    assert not keychain.events and not containers and not networks


def test_cancel_does_not_wait_for_blocked_native_store_and_late_write_cannot_restore_connection(owned_auth):
    import threading, time
    service, database, keychain, audit = owned_auth
    lease = service.begin_codex_lease("company", "capability", IDENTITY, intent="login")
    lease.restore(binding())
    entered, released, errors = threading.Event(), threading.Event(), []
    def blocked():
        entered.set(); assert released.wait(1)
    keychain.on_store = blocked
    def write():
        try: lease.persist(binding(), cache(), authenticated=True)
        except CredentialError as error: errors.append(str(error))
    worker = threading.Thread(target=write); worker.start()
    try:
        assert entered.wait(.5)
        started = time.monotonic(); lease.cancel(); assert time.monotonic() - started < .1
        lease.abort()
        assert worker.is_alive() and service.codex_connection("company", "capability")["state"] == "HELD"
        before = list(keychain.events)
        with pytest.raises(CredentialError): service.begin_codex_lease("company", "capability", IDENTITY)
        assert keychain.events == before
    finally: released.set(); worker.join(.5)
    assert not worker.is_alive() and errors and all("SYNTHETIC" not in value for value in errors)
    assert service.codex_connection("company", "capability")["state"] == "HELD"
