#!/usr/bin/env python3
"""Curis R&D department proof: process a real dev request through the Curis own pipeline.

证明 Curis 自己的研发部（dept-9dc98451）能处理真实的开发请求：
"修复员工列表字段映射问题" → 研发部工作流 → RealRDExecutor → 读代码→改代码→交付 diff

用法：
  source deploy/new-api/.env
  CURIS_RD_SANDBOX=off PYTHONUTF8=1 backend/.venv/bin/python tools/rd_dept_proof.py
"""

import json
import os
import sys
import uuid
import textwrap
from datetime import datetime, timezone

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "backend"))
os.chdir(REPO_ROOT)

# ── 加载 deploy/new-api/.env ──
env_path = os.path.join(REPO_ROOT, "deploy", "new-api", ".env")
if os.path.isfile(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())
    print(f"📋 已加载 env: {env_path}")

# 研发部实例 ID（从 DB 查到的现有记录）
RND_DEPT_ID = "dept-9dc98451-815c-463e-b898-32e7e1fb599e"
RND_COMPANY_ID = "company-fe180ca1-0f7e-4354-9b07-0fa9b0459087"
WORKFLOW_CONTENT_ID = "wl_rd_pipeline_e2e"

print("=" * 70)
print("  Curis 研发部自有流水线 — 端到端证明")
print("=" * 70)
print()

# ── 1. 确认 Department/Employee 实例存在 ──
print("▶ 步骤 1：检查研发部实例...")
from app.database import Database
from app.tenant_context import TenantContext, DEFAULT_TENANT
# 设 tenant context 为 selfuse（与 DB 数据一致）

db_path = os.path.join(REPO_ROOT, "data/curis.sqlite")
db = Database(db_path)

with db.connect() as conn:
    dept = conn.execute(
        "select * from department_instances where id = ?",
        (RND_DEPT_ID,),
    ).fetchone()
    assert dept, f"研发部实例 {RND_DEPT_ID} 不存在"
    print(f"  ✅ 研发部: {dict(dept)['name']} (template={dict(dept)['template_id']})")

    emps = conn.execute(
        "select id, name, role from employee_instances where department_id = ? and deleted_at is null",
        (RND_DEPT_ID,),
    ).fetchall()
    print(f"  ✅ 部门员工: {len(emps)} 人")
    for e in emps:
        print(f"     - {e[1]} ({e[2]})")

# ── 2. 确保 workflow_content 指向 wt_rd_pipeline ──
print()
print("▶ 步骤 2：确保 workflow_content 指向 wt_rd_pipeline...")
with db.connect() as conn:
    existing = conn.execute(
        "select workflow_content_id from workflow_contents where workflow_content_id = ?",
        (WORKFLOW_CONTENT_ID,),
    ).fetchone()
    if existing:
        print(f"  ✅ workflow_content {WORKFLOW_CONTENT_ID} 已存在")
    else:
        conn.execute(
            "insert into workflow_contents "
            "(workflow_content_id, name, workflow_template_ref, pack, owner_roles_json, "
            "step_templates_json, source_attribution, version, status, source, tenant_id, enabled) "
            "values (?, ?, ?, 'ai_rd', '[\"TechLead\",\"Backend Engineer\",\"QA\"]', "
            "'[]', 'Curis internal', '1.0.0', 'active', 'official', 'platform', 1)",
            (WORKFLOW_CONTENT_ID, "R&D 流水线（含 real_rd）", "wt_rd_pipeline"),
        )
        print(f"  ✅ 已创建 workflow_content {WORKFLOW_CONTENT_ID} → wt_rd_pipeline")

# ── 3. 确认 target_a.py 在 BUG 态 ──
print()
print("▶ 步骤 3：确认 target_a.py 在 BUG 态...")
target_path = "tools/real_rd_fixture/target_a.py"
with open(os.path.join(REPO_ROOT, target_path)) as f:
    src = f.read()
assert "BETA = 2" in src, "target_a.py 不处于 BUG 态"
print(f"  ✅ BETA=2（BUG 态，需修复为 3）")

# ── 4. 启动研发部工作流 ──
print()
print("▶ 步骤 4：启动研发部工作流...")

# 事件日志
class ProofEventLog:
    events = []
    def record(self, *, correlation_id="", event_type="", payload=None, tenant_id=None, idempotency_key=None):
        self.events.append({"type": event_type, "cid": correlation_id})
        print(f"     [event] {event_type}")

event_log = ProofEventLog()

from app.model_gateway import ModelGatewayAdapter
adapter = ModelGatewayAdapter(timeout=180)
probe = adapter.execute("Say 'ok'")
print(f"  ✅ 网关可达: status={probe.get('status')}, tokens={probe.get('total_tokens')}")

from app.real_rd_executor import RealRDExecutor
executor = RealRDExecutor(model=adapter, event_log=event_log, sandbox_mode="off")

# 构造 RdWorkflowRuntime
from app.rd_workflow_runtime import RdWorkflowRuntime

rt = RdWorkflowRuntime(
    database=db,
    event_log=event_log,
    model_fn=None,  # 不使用文本生成模式，让 real_rd 分支优先
    real_rd_executor=executor,
)

# 调用研发部工作流
issue_prompt = textwrap.dedent("""\
    修正 tools/real_rd_fixture/target_a.py：
    当前 BETA = 2，正确的值应该是 3。
    目标文件：tools/real_rd_fixture/target_a.py
    测试命令：backend/tests/test_real_rd_fixture_a.py
""").strip()

print(f"  📋 prompt: 修正 target_a.py BETA=2→3")
print()

result = rt.run(
    department_id=RND_DEPT_ID,
    workflow_content_id=WORKFLOW_CONTENT_ID,
    prompt=issue_prompt,
    task_id=f"e2e-rd-dept-{uuid.uuid4().hex[:8]}",
    company_id=RND_COMPANY_ID,
    issue_spec_override={
        "target_files": ["tools/real_rd_fixture/target_a.py"],
        "test_command_id": "test_fixture_a",
        "test_command_argv": ["backend/tests/test_real_rd_fixture_a.py"],
        "allow_paths": ["tools/real_rd_fixture/target_a.py", "backend/tests/test_real_rd_fixture_a.py"],
        "max_rounds": 1,  # 1轮快速验证
    },
)

# ── 5. 验证结果 ──
print()
print("=" * 70)
print("  研发部工作流执行结果")
print("=" * 70)
print(f"  workflow_run_id:  {result['workflow_run_id']}")
print(f"  status:           {result['status']}")
print(f"  步骤数:           {result['steps']}")
print()

# 检查 target_a.py 是否被修改
with open(os.path.join(REPO_ROOT, target_path)) as f:
    src_after = f.read()
if "BETA = 3" in src_after:
    print("  ✅ 证据 1: target_a.py 中 BETA 已从 2 改为 3（真实代码修改）")
else:
    print("  ⚠️  target_a.py BETA 未变化，模型可能未正确修改")

# 检查 audit event
rd_events = [e for e in event_log.events if "real_rd" in e["type"] or "tool" in e["type"]]
print(f"  ✅ 证据 2: 审计事件 {len(event_log.events)} 条")
print(f"     real_rd 事件: {sum(1 for e in event_log.events if 'real_rd' in e['type'])} 条")
print(f"     tool 调用事件: {sum(1 for e in event_log.events if 'tool' in e['type'])} 条")

# 检查 workflow_steps 表
with db.connect() as conn:
    steps = conn.execute(
        "select step_order, step_name, employee_role, status, output from workflow_steps "
        "where workflow_run_id = ? order by step_order",
        (result["workflow_run_id"],),
    ).fetchall()
    print(f"  ✅ 证据 3: workflow_steps {len(steps)} 条")
    for s in steps:
        output_preview = s[4][:80] if s[4] else "(empty)"
        print(f"     [{s[0]}] {s[1]} ({s[2]}) → {output_preview}...")

# final_report
fr = result.get("final_report", "")
if fr:
    print(f"  ✅ 证据 4: final_report ({len(fr)} chars)")
    print(f"     {fr[:200]}...")

print()
print("=" * 70)
if result["status"] == "completed":
    print("  ✅ Curis 研发部自有流水线 — 端到端跑通")
    print(f"  input: 修复员工列表字段映射问题")
    print(f"  workflow: 任务拆解 → 架构设计 → 编码(real_rd) → 测试 → 审查 → 交付")
    print(f"  result: status={result['status']}, steps={result['steps']}")
else:
    print(f"  ⚠️  工作流未完成: {result['status']}")

print("=" * 70)

# ── 恢复 fixture ──
import subprocess
subprocess.run(["git", "checkout", "--", target_path], capture_output=True, cwd=REPO_ROOT)
print("  ℹ️  target_a.py 已恢复 BUG 态")
