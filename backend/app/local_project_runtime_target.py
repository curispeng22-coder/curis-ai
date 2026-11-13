from __future__ import annotations

import json
import os
from pathlib import Path
import socket
import sqlite3
import uuid


_ROOT = Path(__file__).resolve().parents[2]
TARGET_DB = _ROOT / "deploy/curis/gateway/.generated/data/quality.sqlite"
LOOPBACK = "127.0.0.1"
PORTS = (3000, 3100, 8001, 8002, 8080)
OPERATION_KEY = "macos-google-oidc-project-runtime-v1"


class ProvisioningRejected(RuntimeError):
    pass


def _new_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _assert_ports_closed() -> None:
    for port in PORTS:
        with socket.socket() as client:
            client.settimeout(0.05)
            if client.connect_ex((LOOPBACK, port)) == 0:
                raise ProvisioningRejected("local_ports_open")


def _row(connection: sqlite3.Connection, authorization_id: str) -> dict[str, str]:
    row = connection.execute(
        "select authorization_id, tenant_id, company_id, ceo_id, project_id, status "
        "from local_owner_preauthorizations where authorization_id = ?",
        (authorization_id,),
    ).fetchone()
    if row is None:
        raise ProvisioningRejected("preauthorization_missing")
    return dict(row)


def _validate_target(connection: sqlite3.Connection, target: dict[str, str]) -> None:
    chain = connection.execute(
        "select 1 from tenants t "
        "join companies c on c.tenant_id = t.tenant_id "
        "join projects p on p.tenant_id = c.tenant_id and p.company_id = c.company_id "
        "where t.tenant_id = ? and c.company_id = ? and c.ceo_id = ? "
        "and c.default_project_id = ? and p.project_id = ?",
        (
            target["tenant_id"],
            target["company_id"],
            target["ceo_id"],
            target["project_id"],
            target["project_id"],
        ),
    ).fetchone()
    active_owner = connection.execute(
        "select count(*) from tenant_memberships where tenant_id = ? and company_id = ? "
        "and ceo_id = ? and status = 'active' and role in ('owner', 'ceo')",
        (target["tenant_id"], target["company_id"], target["ceo_id"]),
    ).fetchone()[0]
    if chain is None or active_owner != 0 or target["status"] != "pending":
        raise ProvisioningRejected("target_inconsistent")


def provision() -> dict[str, str]:
    if os.getenv("CURIS_ENV", "").strip().lower() not in {"local", "development"}:
        raise ProvisioningRejected("local_environment_required")
    if not TARGET_DB.is_file():
        raise ProvisioningRejected("quality_database_missing")
    _assert_ports_closed()

    connection = sqlite3.connect(TARGET_DB)
    connection.row_factory = sqlite3.Row
    try:
        connection.execute("begin immediate")
        connection.execute(
            "create table if not exists local_owner_preauthorizations ("
            "authorization_id text primary key, operation_key text not null unique, "
            "tenant_id text not null, company_id text not null, ceo_id text not null, "
            "project_id text not null, material_digest text, "
            "status text not null check (status in ('pending','consumed','revoked')), "
            "created_at text not null default current_timestamp, consumed_at text)"
        )
        existing = connection.execute(
            "select authorization_id from local_owner_preauthorizations where operation_key = ?",
            (OPERATION_KEY,),
        ).fetchone()
        if existing is not None:
            target = _row(connection, existing["authorization_id"])
            _validate_target(connection, target)
            connection.commit()
            return target

        target = {
            "authorization_id": _new_id("local-owner-preauth"),
            "tenant_id": _new_id("local-tenant"),
            "company_id": _new_id("local-company"),
            "ceo_id": _new_id("local-ceo"),
            "project_id": _new_id("local-project"),
            "status": "pending",
        }
        connection.execute(
            "insert into tenants (tenant_id, name, status, description) values (?, ?, 'active', ?)",
            (target["tenant_id"], "Local Project Runtime", "Local-only Google OIDC target"),
        )
        connection.execute(
            "insert into companies "
            "(company_id, tenant_id, ceo_id, name, description, status, is_default) "
            "values (?, ?, ?, ?, ?, 'active', 0)",
            (
                target["company_id"],
                target["tenant_id"],
                target["ceo_id"],
                "Local Project Runtime Company",
                "Local-only Google OIDC target",
            ),
        )
        connection.execute(
            "insert into projects "
            "(project_id, tenant_id, company_id, name, goal, description, status) "
            "values (?, ?, ?, ?, ?, ?, 'planned')",
            (
                target["project_id"],
                target["tenant_id"],
                target["company_id"],
                "Project Runtime Local",
                "通过 Project Runtime 提交目标并运行",
                "Local-only Google OIDC target",
            ),
        )
        connection.execute(
            "update companies set default_project_id = ? where company_id = ? and tenant_id = ?",
            (target["project_id"], target["company_id"], target["tenant_id"]),
        )
        connection.execute(
            "insert into local_owner_preauthorizations "
            "(authorization_id, operation_key, tenant_id, company_id, ceo_id, project_id, status) "
            "values (?, ?, ?, ?, ?, ?, 'pending')",
            (
                target["authorization_id"],
                OPERATION_KEY,
                target["tenant_id"],
                target["company_id"],
                target["ceo_id"],
                target["project_id"],
            ),
        )
        created = _row(connection, target["authorization_id"])
        _validate_target(connection, created)
        connection.commit()
        return created
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


if __name__ == "__main__":
    print(json.dumps(provision(), sort_keys=True))
