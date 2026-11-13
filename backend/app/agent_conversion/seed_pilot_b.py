"""Pilot B 独立 seed 运行器（CLI）。

显式调用 ``Database.seed_agent_conversion_pilot_b()`` 写入受控试点 B 候选/草稿资产。
**不挂默认 initialize() 链**——本脚本是唯一的显式触发入口，且先 ``initialize()``
（幂等，确保 schema + 既有 6 官方 et_* / 115 工具 / 52 技能）再叠加 Pilot B。

用法：
    python -m app.agent_conversion.seed_pilot_b [db_path]

运行后打印各表 Pilot B 行数；需要回滚时调用：
    python -m app.agent_conversion.seed_pilot_b --rollback [db_path]

聚焦激活（仅元数据 status，可逆，不影响其余候选）：
    python -m app.agent_conversion.seed_pilot_b --activate-highvalue [db_path]
    python -m app.agent_conversion.seed_pilot_b --deactivate-highvalue [db_path]

注意：激活/回滚仅改已落库的 4 个 ★5 候选 status；须先 ``--rollback`` 的反向
（即先 seed 落 draft）再激活才有效。激活本身不新建任何资产。
"""

from __future__ import annotations

import sys
from pathlib import Path

# 确保 backend/ 与 backend/app/ 在 sys.path（直接运行脚本时）。
_ROOT = Path(__file__).resolve().parent.parent.parent
for _p in (str(_ROOT), str(_ROOT / "app")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from app.database import Database  # noqa: E402


def _counts(db: Database) -> dict:
    with db.connect() as conn:
        def _c(sql: str) -> int:
            return conn.execute(sql).fetchone()[0]

        return {
            "department_types(business.*)": _c(
                "select count(*) from department_types where type_key like 'business.%'"
            ),
            "persona_templates(pt_*)": _c(
                "select count(*) from persona_templates where persona_id like 'pt_%' "
                "and persona_id not in ("
                "'pt_supportive_coach','pt_direct_executor','pt_analytical_advisor',"
                "'pt_creative_explorer','pt_balanced_facilitator','pt_risk_aware_guardian')"
            ),
            "employee_templates(official.employee.*)": _c(
                "select count(*) from employee_templates where id like 'official.employee.%'"
            ),
            "skill_templates(skl_pilot_b_*)": _c(
                "select count(*) from skill_templates where skill_template_id like 'skl_pilot_b_%'"
            ),
            "tool_templates(tl_pilot_b_*)": _c(
                "select count(*) from tool_templates where tool_template_id like 'tl_pilot_b_%'"
            ),
            "workflow_templates(wt_pilot_b_*)": _c(
                "select count(*) from workflow_templates where id like 'wt_pilot_b_%'"
            ),
            "department_templates(dt_pilot_b_*)": _c(
                "select count(*) from department_templates where id like 'dt_pilot_b_%'"
            ),
        }


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("--")]
    db_path = args[0] if args else "curis_pilot_b.sqlite"
    rollback = "--rollback" in argv
    activate = "--activate-highvalue" in argv
    deactivate = "--deactivate-highvalue" in argv

    db = Database(path=db_path)
    if rollback:
        db.rollback_agent_conversion_pilot_b()
        print(f"[rollback] Pilot B 资产已回滚：{db_path}")
        for k, v in _counts(db).items():
            print(f"  {k}: {v}")
        return 0

    if activate:
        db.activate_pilot_b_highvalue()
        print(f"[activate-highvalue] 4 个 ★5 候选已激活（status='active'）：{db_path}")
        for k, v in _counts(db).items():
            print(f"  {k}: {v}")
        return 0

    if deactivate:
        db.deactivate_pilot_b_highvalue()
        print(f"[deactivate-highvalue] 4 个 ★5 候选已回滚（status='draft'）：{db_path}")
        for k, v in _counts(db).items():
            print(f"  {k}: {v}")
        return 0

    db.seed_agent_conversion_pilot_b()
    print(f"[seed] Pilot B 候选/草稿已叠加写入：{db_path}")
    for k, v in _counts(db).items():
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
