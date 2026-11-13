#!/usr/bin/env python3
"""本地一键复跑真实研发闭环（RealRDExecutor）CLI。

加载 deploy/new-api/.env 注入模型网关环境（不写死密钥），构造
ModelGatewayAdapter（本地 New API）+ 真实 LocalRDToolset + RealRDExecutor，
针对一个 issue 规格运行「读→改→测→交付 Diff」闭环，并打印
status / rounds / test_exit_code / diff_text。

用法：
    # 从 JSON 文件读取 issue 规格
    python backend/scripts/run_real_rd.py --issue spec.json
    # 从 stdin 读取
    echo '{"issue_id":"rd-001","target_file":"tools/real_rd_fixture/target_a.py",\
          "issue":"Change BETA = 2 to BETA = 3",\
          "expected_test":"backend/tests/test_real_rd_fixture_a.py"}' \
        | python backend/scripts/run_real_rd.py --issue -

    # 关闭 sandbox 网络隔离（仅本地开发 / 受信 CI）
    python backend/scripts/run_real_rd.py --issue spec.json --no-sandbox

issue 规格（JSON）字段：
    issue_id      : str，可选，默认 "rd-local-run"
    target_file   : str | list[str]，目标源码文件（相对仓库根）
    target_files  : str | list[str]，同上（target_file 的别名）
    issue         : str，问题 / 修改指令（映射到 instructions）
    instructions  : str，同上（issue 的别名）
    expected_test : str，受验 pytest 用例路径（须位于 backend/tests/ 下）
    test_command_id: str，可选，默认 "rd_verify"
    max_rounds    : int，可选，默认 3

安全说明：``--no-sandbox``（或环境变量 CURIS_RD_SANDBOX=off）会关闭网络隔离，
仅限本地开发 / 受信 CI；生产多租户环境必须确保 sandbox-exec 存在或 ENFORCE。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

# 将 backend/ 加入 sys.path，便于以脚本方式直接运行（python backend/scripts/...）。
_REPO_ROOT = Path(__file__).resolve().parents[2]
_BACKEND_ROOT = _REPO_ROOT / "backend"
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

from app.database import Database  # noqa: E402
from app.evolution_event_log import EvolutionEventLog  # noqa: E402
from app.local_rd_toolset import SandboxMode  # noqa: E402
from app.model_gateway import ModelGatewayAdapter  # noqa: E402
from app.real_rd_executor import RealRDExecutor  # noqa: E402


def _load_dotenv(path: Path) -> None:
    """将 .env 文件中的键值对注入 os.environ（不覆盖已有变量）。

    不写死任何密钥；密钥仅在 deploy/new-api/.env 中维护。
    """
    if not path.is_file():
        print(f"[warn] .env 未找到：{path}", file=sys.stderr)
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip()
        if key and key not in os.environ:
            os.environ[key] = value


def _read_issue_spec(source: str) -> dict:
    if source == "-":
        data = sys.stdin.read()
    else:
        data = Path(source).read_text(encoding="utf-8")
    try:
        return json.loads(data)
    except json.JSONDecodeError as error:
        raise SystemExit(f"issue 规格不是合法 JSON：{error}") from error


def _build_issue_spec(raw: dict) -> dict:
    issue_id = str(raw.get("issue_id") or "rd-local-run")

    target_file = raw.get("target_file") or raw.get("target_files")
    if isinstance(target_file, str):
        target_files = [target_file]
    elif isinstance(target_file, (list, tuple)):
        target_files = [str(item) for item in target_file]
    else:
        raise SystemExit("issue 规格缺少 target_file / target_files")
    if not target_files:
        raise SystemExit("issue 规格缺少 target_file / target_files")

    expected_test = raw.get("expected_test")
    if not expected_test:
        raise SystemExit("issue 规格缺少 expected_test（pytest 用例路径）")

    instructions = raw.get("issue") or raw.get("instructions") or ""
    test_command_id = raw.get("test_command_id") or "rd_verify"

    return {
        "issue_id": issue_id,
        "target_files": target_files,
        "instructions": instructions,
        "test_command_id": test_command_id,
        "test_command_argv": ["pytest", str(expected_test)],
        "allow_paths": [str(expected_test), *target_files],
        "max_rounds": int(raw.get("max_rounds") or 3),
    }


def _make_event_log() -> EvolutionEventLog:
    tmp_dir = tempfile.mkdtemp(prefix="real-rd-run-")
    db_path = os.path.join(tmp_dir, "evo.sqlite")
    db = Database(db_path)
    with db.connect() as conn:
        conn.execute(
            """
            create table if not exists evolution_events (
                event_id integer primary key autoincrement,
                correlation_id text not null,
                event_type text not null,
                payload text not null,
                tenant_id text,
                idempotency_key text,
                created_at text not null default current_timestamp
            )
            """
        )
    return EvolutionEventLog(db)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="本地复跑真实研发闭环（RealRDExecutor）")
    parser.add_argument(
        "--issue", required=True,
        help="issue 规格 JSON 文件路径，或 '-' 从 stdin 读取",
    )
    parser.add_argument(
        "--no-sandbox", action="store_true",
        help="关闭 sandbox 网络隔离（仅本地开发 / 受信 CI）",
    )
    parser.add_argument(
        "--env", default=str(_REPO_ROOT / "deploy" / "new-api" / ".env"),
        help="模型网关 .env 路径（默认 deploy/new-api/.env）",
    )
    parser.add_argument("--max-rounds", type=int, default=None, help="覆盖 issue 规格的 max_rounds")
    args = parser.parse_args(argv)

    _load_dotenv(Path(args.env))

    # sandbox 模式：--no-sandbox → OFF；否则透传 None（LocalRDToolset 解析
    # CURIS_RD_SANDBOX 环境变量，默认 auto）。
    sandbox_mode: SandboxMode | None = SandboxMode.OFF if args.no_sandbox else None

    # 真实模型网关（本地 New API，密钥来自 .env，不写死）。
    model = ModelGatewayAdapter(
        base_url=os.getenv("CURIS_MODEL_GATEWAY_BASE_URL") or "http://127.0.0.1:3000",
        api_key=os.getenv("CURIS_MODEL_GATEWAY_API_KEY") or "",
        gateway_id=os.getenv("CURIS_MODEL_GATEWAY_ID") or "newapi-local",
        model_name=os.getenv("CURIS_MODEL_GATEWAY_MODEL") or "deepseek-v4-pro",
    )

    event_log = _make_event_log()
    raw_spec = _read_issue_spec(args.issue)
    if args.max_rounds is not None:
        raw_spec["max_rounds"] = args.max_rounds
    issue_spec = _build_issue_spec(raw_spec)

    executor = RealRDExecutor(model, event_log, sandbox_mode=sandbox_mode)
    result = executor.run(issue_spec)

    print("=" * 64)
    print(f"issue_id       : {result['issue_id']}")
    print(f"status         : {result['status']}")
    print(f"rounds         : {result['rounds']}")
    print(f"test_exit_code : {result['test_exit_code']}")
    print(f"files          : {[item['path'] for item in result['files']]}")
    print(f"model_name     : {result.get('model_name')}")
    print("-" * 64)
    print("diff_text:")
    print(result["diff_text"] or "(no diff)")
    print("=" * 64)

    return 0 if result["status"] == "succeeded" else 1


if __name__ == "__main__":
    raise SystemExit(main())
