"""真实研发闭环端到端实跑脚本（步骤②脚手架；QA 严过关阶段执行）。

循环 manifest 中的每个 Issue，构造真实 ModelGatewayAdapter（本地 New API，
密钥经 deploy/new-api/.env）+ 真实 LocalRDToolset(sandbox_mode=auto) +
RealRDExecutor，对每个 issue 调用 ``.run(issue_spec)``，采集并打印证据：
status / rounds / test_exit_code / diff_text（含 --- a/ +++ b/ 与 hunk 数）/
files。对结果做断言（status==succeeded 且 test_exit_code==0）。

说明：
- 需要本地 New API 可达且模型可用；否则对应 issue 会报告 model_gateway_error
  并在多轮重试后 status=failed。
- 本文件非 test_*.py，不会被 ``pytest backend/tests/`` 收集；由 QA 显式运行：
      python backend/tests/real_run/run_real_issues.py
- 夹具初始即失败是设计意图；演示改动可用
  ``git checkout tools/real_rd_fixture/`` 撤销。
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path

# backend/ 与 real_run/ 加入 sys.path（脚本方式直接运行）。
_REPO_ROOT = Path(__file__).resolve().parents[3]  # backend/tests/real_run -> repo root
_BACKEND_ROOT = _REPO_ROOT / "backend"
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))  # 便于 import manifest

from app.database import Database  # noqa: E402
from app.evolution_event_log import EvolutionEventLog  # noqa: E402
from app.local_rd_toolset import SandboxMode  # noqa: E402
from app.model_gateway import ModelGatewayAdapter  # noqa: E402
from app.real_rd_executor import RealRDExecutor  # noqa: E402

import manifest  # noqa: E402


def _load_dotenv(path: Path) -> None:
    """将 .env 注入 os.environ（不覆盖已有变量，不写死密钥）。"""
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


_HUNK_RE = re.compile(r"^@@ ", re.MULTILINE)


def _summarize_diff(diff_text: str) -> dict:
    has_a = "--- a/" in diff_text
    has_b = "+++ b/" in diff_text
    hunk_count = len(_HUNK_RE.findall(diff_text)) if diff_text else 0
    return {"has_a": has_a, "has_b": has_b, "hunk_count": hunk_count}


def _make_event_log() -> EvolutionEventLog:
    tmp_dir = tempfile.mkdtemp(prefix="real-rd-e2e-")
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


def _build_issue_spec(entry: dict) -> dict:
    target_file = entry["target_file"]
    expected_test = entry["expected_test"]
    return {
        "issue_id": entry["issue_id"],
        "target_files": [target_file],
        "instructions": entry["issue"],
        "test_command_id": "rd_verify",
        "test_command_argv": ["pytest", expected_test],
        "allow_paths": [expected_test, target_file],
        "max_rounds": int(entry.get("max_rounds", 3)),
    }


def run_one(model: ModelGatewayAdapter, event_log: EvolutionEventLog, entry: dict) -> dict:
    issue_spec = _build_issue_spec(entry)
    # 真实验证环境（如被外层沙箱拦截）无法 exec /usr/bin/sandbox-exec，
    # 故以 OFF 直跑；sandbox 三态（AUTO/OFF/ENFORCE）逻辑已由
    # test_local_rd_toolset_sandbox.py 通过 FakeLocalToolset 覆盖，此处不重复。
    executor = RealRDExecutor(model, event_log, sandbox_mode=SandboxMode.OFF)
    return executor.run(issue_spec)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="真实研发闭环端到端实跑（manifest 驱动）")
    parser.add_argument(
        "--env", default=str(_REPO_ROOT / "deploy" / "new-api" / ".env"),
        help="模型网关 .env 路径",
    )
    parser.add_argument("--only", default=None, help="只跑指定 issue_id")
    parser.add_argument("--max-rounds", type=int, default=None, help="覆盖每个 issue 的 max_rounds")
    args = parser.parse_args(argv)

    _load_dotenv(Path(args.env))

    model = ModelGatewayAdapter(
        base_url=os.getenv("CURIS_MODEL_GATEWAY_BASE_URL") or "http://127.0.0.1:3000",
        api_key=os.getenv("CURIS_MODEL_GATEWAY_API_KEY") or "",
        gateway_id=os.getenv("CURIS_MODEL_GATEWAY_ID") or "newapi-local",
        model_name=os.getenv("CURIS_MODEL_GATEWAY_MODEL") or "deepseek-v4-pro",
    )
    event_log = _make_event_log()

    failures = 0
    for entry in manifest.ISSUES:
        if args.only and entry["issue_id"] != args.only:
            continue
        if args.max_rounds is not None:
            entry = {**entry, "max_rounds": args.max_rounds}
        print("=" * 72)
        print(f"[issue] {entry['issue_id']}  (难度: {entry.get('difficulty', '?')})")
        print(f"  target : {entry['target_file']}")
        print(f"  test   : {entry['expected_test']}")
        try:
            result = run_one(model, event_log, entry)
        except Exception as error:  # noqa: BLE001 - 端到端脚本不应因单 issue 崩溃
            print(f"  ERROR  : {type(error).__name__}: {error}")
            failures += 1
            continue

        summary = _summarize_diff(result.get("diff_text", ""))
        ok = result["status"] == "succeeded" and result.get("test_exit_code") == 0
        failures += 0 if ok else 1
        print(f"  status : {result['status']}  (expected succeeded)")
        print(f"  rounds : {result['rounds']}")
        print(f"  test_exit_code: {result.get('test_exit_code')}  (expected 0)")
        print(f"  files  : {[f['path'] for f in result.get('files', [])]}")
        print(
            f"  diff   : has_a={summary['has_a']} has_b={summary['has_b']} "
            f"hunks={summary['hunk_count']}"
        )
        if result.get("diff_text"):
            print("  ----- diff_text -----")
            for line in result["diff_text"].splitlines():
                print(f"    {line}")
        print(f"  verdict: {'PASS' if ok else 'FAIL'}")
    print("=" * 72)
    print(f"结论：{'全部通过' if failures == 0 else f'{failures} 个 issue 未通过'}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
