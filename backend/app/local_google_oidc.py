from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import hmac
import json
import logging
import os
import secrets
import socket
import sys
import threading
import time
from urllib.parse import urlencode, urlsplit
import uuid

import httpx
from fastapi import Request
from fastapi.responses import JSONResponse, RedirectResponse

from .identity_membership import AuthorizedMembership


ISSUER = "https://accounts.google.com"
LOCAL_ISSUER = "curis://local-desktop"
LOCAL_SUBJECT_ID = "local-owner"
REDIRECT_URI = "http://127.0.0.1:8080/api/auth/google/callback"
FRONTEND = "http://127.0.0.1:3001"
TENANT_ID = "local-tenant-447e9ae9-9e30-477e-8ad0-73db68397ba4"
COMPANY_ID = "local-company-076a4926-4b95-404c-a019-acf36c26108b"
CEO_ID = "local-ceo-660378a5-a637-45ff-b6bd-431cd36c7046"
PROJECT_ID = "local-project-b6f325cc-f347-4a74-a6d6-67528a3889b8"
PREAUTHORIZATION_ID = "local-owner-preauth-589a0ce3-97cf-401b-a54b-fb745b6fe579"
LOGIN_URL = f"{FRONTEND}/login"
_SOCKET = b"\0curis-local-owner-bootstrap"
_LOG = logging.getLogger("curis.security.local_google_oidc")


class LocalOidcRejected(RuntimeError):
    pass


class LocalGoogleOidc:
    def __init__(self, database):
        self.database = database
        self.google_enabled = os.getenv("CURIS_LOCAL_GOOGLE_OIDC_ENABLED", "") == "1"
        self.local_owner_enabled = os.getenv("CURIS_LOCAL_OWNER_ENABLED", "") == "1"
        self.enabled = self.google_enabled or self.local_owner_enabled
        environment = os.getenv("CURIS_ENV", "").strip().lower()
        product = os.getenv("CURIS_PRODUCT", "").strip().lower()
        if self.enabled and (environment not in {"local", "development"} or product != "workspace"):
            if self.google_enabled:
                raise RuntimeError("local Google OIDC requires local/development Workspace")
            raise RuntimeError("local Owner requires local/development Workspace")
        self._lock = threading.Lock()
        self._client_id = ""
        self._client_secret = ""
        self._bootstrap_digest = ""
        self._session_key = b""
        self._states: dict[str, tuple[str, float, str]] = {}
        self._sessions: dict[str, tuple[AuthorizedMembership, float]] = {}
        self._listener: socket.socket | None = None

    @property
    def ready(self) -> bool:
        return bool(self._client_id and self._client_secret and self._bootstrap_digest and self._session_key)

    def inject(self, payload: dict[str, str]) -> None:
        if set(payload) != {"google_client_id", "google_client_secret", "bootstrap_material"}:
            raise LocalOidcRejected("bootstrap_payload_invalid")
        client_id = payload["google_client_id"].strip()
        client_secret = payload["google_client_secret"].strip()
        material = payload["bootstrap_material"]
        if not client_id or len(client_secret) < 8 or len(material) < 32:
            raise LocalOidcRejected("bootstrap_payload_invalid")
        digest = hashlib.sha256(material.encode()).hexdigest()
        with self.database.connect() as connection:
            connection.execute("begin immediate")
            row = connection.execute(
                "select * from local_owner_preauthorizations where authorization_id=? "
                "and tenant_id=? and company_id=? and ceo_id=? and project_id=?",
                (PREAUTHORIZATION_ID, TENANT_ID, COMPANY_ID, CEO_ID, PROJECT_ID),
            ).fetchone()
            active_owner_count = connection.execute(
                "select count(*) from tenant_memberships where issuer=? and tenant_id=? "
                "and company_id=? and ceo_id=? and role='owner' and status='active'",
                (ISSUER, TENANT_ID, COMPANY_ID, CEO_ID),
            ).fetchone()[0]
            if (
                row is None
                or row["status"] not in {"pending", "consumed"}
                or not self._target_exists(connection)
                or active_owner_count != (1 if row["status"] == "consumed" else 0)
            ):
                raise LocalOidcRejected("preauthorization_missing")
            if row["material_digest"] not in (None, digest):
                raise LocalOidcRejected("preauthorization_conflict")
            connection.execute(
                "update local_owner_preauthorizations set material_digest=? "
                "where authorization_id=? and material_digest is null",
                (digest, PREAUTHORIZATION_ID),
            )
        with self._lock:
            self._client_id = client_id
            self._client_secret = client_secret
            self._bootstrap_digest = digest
            self._session_key = secrets.token_bytes(32)

    def reset_pending_bootstrap(self) -> None:
        with self.database.connect() as connection:
            connection.execute("begin immediate")
            row = connection.execute(
                "select status from local_owner_preauthorizations where authorization_id=? "
                "and tenant_id=? and company_id=? and ceo_id=? and project_id=?",
                (PREAUTHORIZATION_ID, TENANT_ID, COMPANY_ID, CEO_ID, PROJECT_ID),
            ).fetchone()
            if row is None or row["status"] not in {"pending", "consumed"}:
                raise LocalOidcRejected("preauthorization_not_pending")
            if row["status"] == "consumed":
                active_owner_count = connection.execute(
                    "select count(*) from tenant_memberships where issuer=? and tenant_id=? "
                    "and company_id=? and ceo_id=? and role='owner' and status='active'",
                    (ISSUER, TENANT_ID, COMPANY_ID, CEO_ID),
                ).fetchone()[0]
                if active_owner_count != 1 or not self._target_exists(connection):
                    raise LocalOidcRejected("preauthorization_not_pending")
            connection.execute(
                "update local_owner_preauthorizations set material_digest=null where authorization_id=?",
                (PREAUTHORIZATION_ID,),
            )
        with self._lock:
            self._client_id = ""
            self._client_secret = ""
            self._bootstrap_digest = ""
            self._session_key = b""

    def install(self, app) -> None:
        if not self.enabled:
            return

        if self.local_owner_enabled:
            @app.get("/api/auth/local/status")
            def local_status(request: Request):
                return {
                    "mode": "local_desktop",
                    "initialized": self._local_membership() is not None,
                    "authenticated": self.authorize(request, True) is not None,
                }

            @app.post("/api/auth/local/initialize")
            def initialize_local_owner(request: Request, next: str = ""):
                if not self._local_request_allowed(request):
                    return JSONResponse({"detail": "local_origin_rejected"}, status_code=403)
                try:
                    membership, first_login = self._initialize_local_owner()
                except LocalOidcRejected as error:
                    return JSONResponse({"detail": str(error)}, status_code=409)
                target = (
                    f"/onboarding?{urlencode({'next': self._safe_return_to(next)})}"
                    if first_login
                    else self._safe_return_to(next)
                )
                return self._session_response(membership, target, 201 if first_login else 200)

            @app.post("/api/auth/local/session")
            def create_local_session(request: Request, next: str = ""):
                if not self._local_request_allowed(request):
                    return JSONResponse({"detail": "local_origin_rejected"}, status_code=403)
                membership = self._local_membership()
                if membership is None:
                    return JSONResponse({"detail": "local_owner_not_initialized"}, status_code=409)
                return self._session_response(membership, self._safe_return_to(next))

            @app.post("/api/auth/local/logout")
            def logout_local_owner(request: Request):
                if not self._local_request_allowed(request):
                    return JSONResponse({"detail": "local_origin_rejected"}, status_code=403)
                return self._logout(request)

        @app.on_event("startup")
        def _start_local_bootstrap() -> None:
            self.start_listener()

        @app.on_event("shutdown")
        def _stop_local_bootstrap() -> None:
            self.close()

        @app.get("/api/auth/google/status")
        def status(request: Request):
            return {"owner_binding_ready": self.ready, "authenticated": self.authorize(request, True) is not None}

        @app.get("/api/auth/google/login")
        def login(next: str = ""):
            if not self.ready:
                return RedirectResponse(f"{LOGIN_URL}?error=owner_binding_not_ready", status_code=303)
            state, nonce = secrets.token_urlsafe(32), secrets.token_urlsafe(32)
            return_to = self._safe_return_to(next)
            with self._lock:
                self._states[state] = (nonce, time.time() + 300, return_to)
            target = "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(
                {
                    "client_id": self._client_id,
                    "redirect_uri": REDIRECT_URI,
                    "response_type": "code",
                    "scope": "openid email profile",
                    "state": state,
                    "nonce": nonce,
                }
            )
            response = RedirectResponse(target, status_code=303)
            response.set_cookie(
                "curis_oidc_state", state, max_age=300, path="/api/auth/google",
                httponly=True, samesite="lax",
            )
            return response

        @app.get("/api/auth/google/callback")
        def callback(request: Request, code: str = "", state: str = "", error: str = ""):
            request.scope["query_string"] = b""
            if error:
                rejection = "provider_error"
            elif not code:
                rejection = "code_missing"
            elif not state:
                rejection = "state_missing"
            elif request.cookies.get("curis_oidc_state") != state:
                rejection = "state_cookie_mismatch"
            else:
                rejection = ""
            if rejection:
                _LOG.warning("local_google_oidc_callback_rejected reason=%s", rejection)
                return self._failure("login_failed")
            with self._lock:
                saved = self._states.pop(state, None)
            if saved is None or saved[1] <= time.time():
                return self._failure("login_expired")
            try:
                claims = self._google_claims(code, saved[0])
                membership, first_login = self._consume_or_authorize(claims["sub"])
            except LocalOidcRejected:
                return self._failure("owner_activation_not_pre_authorized")
            if first_login:
                target = f"{FRONTEND}/onboarding?{urlencode({'next': saved[2]})}"
            else:
                target = f"{FRONTEND}{saved[2]}"
            return self._session_response(membership, target, redirect=True)

        @app.post("/api/auth/google/logout")
        def logout(request: Request):
            return self._logout(request)

    def is_auth_path(self, path: str) -> bool:
        return (
            self.local_owner_enabled and path.startswith("/api/auth/local/")
        ) or (
            self.google_enabled and path.startswith("/api/auth/google/")
        )

    def authorize(self, request: Request, trusted_source: bool) -> AuthorizedMembership | None:
        if not self.enabled or not trusted_source:
            return None
        session_id = request.cookies.get("curis_local_session", "")
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None:
                return None
            if session[1] <= time.time():
                self._sessions.pop(session_id, None)
                return None
            return session[0]

    def _initialize_local_owner(self) -> tuple[AuthorizedMembership, bool]:
        with self.database.connect() as connection:
            connection.execute("begin immediate")
            connection.execute(
                "insert or ignore into tenants (tenant_id, name) values (?, 'Local Workspace')",
                (TENANT_ID,),
            )
            row = connection.execute(
                "select * from tenant_memberships where issuer=? and subject_id=? "
                "and tenant_id=? order by created_at desc limit 1",
                (LOCAL_ISSUER, LOCAL_SUBJECT_ID, TENANT_ID),
            ).fetchone()
            first_login = row is None
            if row is None:
                connection.execute(
                    "insert into tenant_memberships "
                    "(membership_id, issuer, subject_id, tenant_id, company_id, ceo_id, role, status) "
                    "values (?, ?, ?, ?, '', ?, 'owner', 'active')",
                    (
                        f"membership-{uuid.uuid4()}",
                        LOCAL_ISSUER,
                        LOCAL_SUBJECT_ID,
                        TENANT_ID,
                        CEO_ID,
                    ),
                )
            elif row["status"] != "active" or row["role"] != "owner" or row["ceo_id"] != CEO_ID:
                raise LocalOidcRejected("local_owner_membership_mismatch")
        membership = self._local_membership()
        if membership is None:
            raise LocalOidcRejected("local_owner_initialization_failed")
        return membership, first_login

    def _local_membership(self) -> AuthorizedMembership | None:
        if not self.local_owner_enabled:
            return None
        with self.database.connect() as connection:
            row = connection.execute(
                "select * from tenant_memberships where issuer=? and subject_id=? "
                "and tenant_id=? order by created_at desc limit 1",
                (LOCAL_ISSUER, LOCAL_SUBJECT_ID, TENANT_ID),
            ).fetchone()
            tenant = connection.execute(
                "select 1 from tenants where tenant_id=?", (TENANT_ID,)
            ).fetchone()
        if (
            row is None
            or tenant is None
            or row["status"] != "active"
            or row["role"] != "owner"
            or row["ceo_id"] != CEO_ID
        ):
            return None
        return AuthorizedMembership(
            LOCAL_SUBJECT_ID, TENANT_ID, row["company_id"], CEO_ID,
            "owner", "active", str(uuid.uuid4()),
        )

    def _session_response(
        self,
        membership: AuthorizedMembership,
        target: str,
        status_code: int = 200,
        *,
        redirect: bool = False,
    ):
        session_id = secrets.token_urlsafe(32)
        with self._lock:
            self._sessions[session_id] = (membership, time.time() + 8 * 3600)
        response = (
            RedirectResponse(target, status_code=303)
            if redirect
            else JSONResponse({"authenticated": True, "next": target}, status_code=status_code)
        )
        response.set_cookie(
            "curis_local_session", session_id, max_age=8 * 3600,
            httponly=True, samesite="lax",
        )
        return response

    def _logout(self, request: Request):
        session_id = request.cookies.get("curis_local_session", "")
        with self._lock:
            self._sessions.pop(session_id, None)
        response = JSONResponse({"status": "signed_out"})
        response.delete_cookie("curis_local_session")
        return response

    @staticmethod
    def _local_request_allowed(request: Request) -> bool:
        return request.headers.get("origin", "") in {"", FRONTEND}

    def _google_claims(self, code: str, nonce: str) -> dict[str, str]:
        if not self.ready:
            raise LocalOidcRejected("owner_binding_not_ready")
        try:
            with httpx.Client(timeout=10, trust_env=False) as client:
                token_response = client.post(
                    "https://oauth2.googleapis.com/token",
                    data={
                        "client_id": self._client_id,
                        "client_secret": self._client_secret,
                        "code": code,
                        "grant_type": "authorization_code",
                        "redirect_uri": REDIRECT_URI,
                    },
                )
                token_response.raise_for_status()
                id_token = token_response.json().get("id_token", "")
                claim_response = client.get(
                    "https://oauth2.googleapis.com/tokeninfo", params={"id_token": id_token}
                )
                claim_response.raise_for_status()
                claims = claim_response.json()
        except Exception as error:
            raise LocalOidcRejected("google_validation_failed") from error
        if (
            claims.get("iss") != ISSUER
            or claims.get("aud") != self._client_id
            or claims.get("nonce") != nonce
            or not claims.get("sub")
            or int(claims.get("exp", 0)) <= int(time.time())
        ):
            raise LocalOidcRejected("google_claims_invalid")
        return {"sub": str(claims["sub"])}

    def _consume_or_authorize(self, subject_id: str) -> tuple[AuthorizedMembership, bool]:
        with self.database.connect() as connection:
            connection.execute("begin immediate")
            preauth = connection.execute(
                "select * from local_owner_preauthorizations where authorization_id=? "
                "and tenant_id=? and company_id=? and ceo_id=? and project_id=?",
                (PREAUTHORIZATION_ID, TENANT_ID, COMPANY_ID, CEO_ID, PROJECT_ID),
            ).fetchone()
            membership = connection.execute(
                "select * from tenant_memberships where issuer=? and subject_id=? and tenant_id=? "
                "and company_id=? order by created_at desc limit 1",
                (ISSUER, subject_id, TENANT_ID, COMPANY_ID),
            ).fetchone()
            active_owner_count = connection.execute(
                "select count(*) from tenant_memberships where tenant_id=? and company_id=? "
                "and ceo_id=? and issuer=? and role='owner' and status='active'",
                (TENANT_ID, COMPANY_ID, CEO_ID, ISSUER),
            ).fetchone()[0]
            if not self._target_exists(connection):
                raise LocalOidcRejected("target_missing")
            first_login = membership is None
            if membership is not None:
                if (
                    preauth is None
                    or preauth["status"] != "consumed"
                    or membership["status"] != "active"
                    or membership["role"] != "owner"
                    or membership["ceo_id"] != CEO_ID
                    or active_owner_count != 1
                ):
                    raise LocalOidcRejected("membership_mismatch")
            else:
                if (
                    preauth is None
                    or preauth["status"] != "pending"
                    or not self._bootstrap_digest
                    or not hmac.compare_digest(preauth["material_digest"] or "", self._bootstrap_digest)
                    or active_owner_count != 0
                ):
                    raise LocalOidcRejected("preauthorization_missing")
                connection.execute(
                    "insert into tenant_memberships "
                    "(membership_id, issuer, subject_id, tenant_id, company_id, ceo_id, role, status) "
                    "values (?, ?, ?, ?, ?, ?, 'owner', 'active')",
                    (f"membership-{uuid.uuid4()}", ISSUER, subject_id, TENANT_ID, COMPANY_ID, CEO_ID),
                )
                updated = connection.execute(
                    "update local_owner_preauthorizations set status='consumed', consumed_at=current_timestamp "
                    "where authorization_id=? and status='pending'",
                    (PREAUTHORIZATION_ID,),
                ).rowcount
                if updated != 1:
                    raise LocalOidcRejected("preauthorization_conflict")
        return (
            AuthorizedMembership(
                subject_id, TENANT_ID, COMPANY_ID, CEO_ID, "owner", "active", str(uuid.uuid4())
            ),
            first_login,
        )

    @staticmethod
    def _safe_return_to(value: str) -> str:
        candidate = (value or "").strip()
        if (
            not candidate.startswith("/")
            or candidate.startswith("//")
            or "\\" in candidate
            or "\r" in candidate
            or "\n" in candidate
            or len(candidate) > 2048
        ):
            return "/ceo-office"
        parsed = urlsplit(candidate)
        if parsed.scheme or parsed.netloc:
            return "/ceo-office"
        return candidate

    @staticmethod
    def _target_exists(connection) -> bool:
        return connection.execute(
            "select 1 from tenants t join companies c on c.tenant_id=t.tenant_id "
            "join projects p on p.tenant_id=c.tenant_id and p.company_id=c.company_id "
            "where t.tenant_id=? and c.company_id=? and c.ceo_id=? "
            "and c.default_project_id=? and p.project_id=?",
            (TENANT_ID, COMPANY_ID, CEO_ID, PROJECT_ID, PROJECT_ID),
        ).fetchone() is not None

    def _failure(self, code: str):
        response = RedirectResponse(f"{LOGIN_URL}?error={code}", status_code=303)
        response.delete_cookie("curis_oidc_state", path="/api/auth/google")
        return response

    def start_listener(self) -> None:
        if not self.google_enabled or sys.platform != "linux" or self._listener is not None:
            return
        listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        listener.bind(_SOCKET)
        listener.listen(1)
        self._listener = listener

        def serve() -> None:
            while self._listener is listener:
                try:
                    client, _ = listener.accept()
                    with client:
                        chunks = []
                        while True:
                            chunk = client.recv(8193)
                            if not chunk:
                                break
                            chunks.append(chunk)
                            if sum(map(len, chunks)) > 8192:
                                raise LocalOidcRejected("bootstrap_payload_invalid")
                        data = b"".join(chunks)
                        if len(data) > 8192:
                            raise LocalOidcRejected("bootstrap_payload_invalid")
                        payload = json.loads(data)
                        if payload == {"action": "reset"}:
                            self.reset_pending_bootstrap()
                            client.sendall(b"OWNER_BINDING_RESET=true\n")
                        else:
                            self.inject(payload)
                            client.sendall(b"OWNER_BINDING_READY=true\n")
                except (OSError, ValueError, TypeError, LocalOidcRejected):
                    continue

        threading.Thread(target=serve, name="curis-local-owner-bootstrap", daemon=True).start()

    def close(self) -> None:
        listener, self._listener = self._listener, None
        if listener is not None:
            listener.close()


def inject_from_stdin() -> None:
    payload = sys.stdin.buffer.read(8193)
    if len(payload) > 8192:
        raise SystemExit(1)
    values = payload.split(b"\0")
    if len(values) != 3:
        raise SystemExit(1)
    payload = json.dumps(
        dict(zip(("google_client_id", "google_client_secret", "bootstrap_material"),
                 (value.decode() for value in values)))
    ).encode()
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        client.connect(_SOCKET)
        client.sendall(payload)
        client.shutdown(socket.SHUT_WR)
        result = client.recv(128)
    finally:
        client.close()
    if result != b"OWNER_BINDING_READY=true\n":
        raise SystemExit(1)
    sys.stdout.buffer.write(result)


def reset_from_cli() -> None:
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        client.connect(_SOCKET)
        client.sendall(b'{"action":"reset"}')
        client.shutdown(socket.SHUT_WR)
        result = client.recv(128)
    finally:
        client.close()
    if result != b"OWNER_BINDING_RESET=true\n":
        raise SystemExit(1)
    sys.stdout.buffer.write(result)


if __name__ == "__main__":
    if sys.argv[1:] == ["inject"]:
        inject_from_stdin()
    elif sys.argv[1:] == ["reset"]:
        reset_from_cli()
    else:
        raise SystemExit(2)
