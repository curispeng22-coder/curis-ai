"""ADR-0017 D4.platform（issue 060）平台级管理后台真实实现验收测试 + 禁止区守卫。

覆盖 issue 060 acceptance criteria 1-9，并**保留** S3 D4.impl（issue 059）的全部契约
覆盖（propose/approve/apply 全流程、公司部门启用态、受控写、tenant 不变式）——S3 的
占位测试 test_d4_impl_governance.py 因本切片解锁 manage_department_types /
cross_company_policy 真实实现（与其断言的占位行为直接冲突）已退役，覆盖迁移至此文件
（S2/S3 既定的「删除过期占位测试、保留扫描」模式，team-lead 已接受）。

本切片范围：
 1. manage_department_types 真实 CRUD（解锁 LOCKED）：create/remove 须 human-approval
    门控（approved_by 缺省 → PermissionError，gate 未解除）；edit/disable/enable 可逆、
    无事件写；复用 MANIFEST_FIELDS 7 键契约；写 governance.type_created/removed。
 2. cross_company_policy 真实实现（解锁 LOCKED）：set/get/list/disable/enable；set 写
    governance.policy_set；依赖 S1 租户边界（tenant_scope）。
 3. UI 解禁：前端 /platform 管理控制台（仅平台级必要 UI）。
 4. /api/platform/* 新增且鉴权；既有 API 语义不变。
 5. LOCKED_ACTIONS 现仅剩 lift_human_approval_gate / auto_modify_code（仍全程锁定）；
    manage_department_types / cross_company_policy 已解锁（有真实调用，不再 NotImplementedError）。
 6. 受控 evolution_events 写仅 governance.propose / apply / type_created / type_removed /
    policy_set（gate 显式批准）；无其他写路径。
 7. forbidden-scope guard clean（无 lift_human_approval_gate 真实路径、无 auto_modify_code
    真实路径、无 L6/ROI、无 Employee CRUD、无外部平台、无向量/embedding、无未授权
    evolution_events 写）。
 8. D3 facade / D1 不变式不受影响；后端回归（含 D1–D4 既有测试）全绿；无既有测试被修改。
 9. database.py 仅 additive platform_policies 表 + department_types CRUD（首个写入者）；
    department_observability.py / tenant_context.py / employee.py 不被改动。

本测试使用临时 SQLite 库；受控写核查 + 禁止区扫描为硬性门禁。
"""

import os
import re
import unittest
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from app.database import Database
from app.department_catalog import CompanyTopology, DepartmentCatalog
from app.evolution_event_log import EvolutionEventLog
from app.governance import (
    CompanyGovernance,
    DepartmentGovernanceView,
    GovernanceProposal,
    GovernanceScope,
)
from app.main import create_app
from app.runtime_governance import AutoApproveSink
from app.tenant_context import TenantContext
from fastapi.testclient import TestClient


_REPO_ROOT = Path(__file__).resolve().parents[2]
_APP_DIR = _REPO_ROOT / "backend" / "app"

# S4 D4.platform 修改/新增的 app 文件（禁止区扫描范围）。
_CHANGED_APP_FILES = [
    _APP_DIR / "governance.py",
    _APP_DIR / "database.py",
    _APP_DIR / "main.py",
]

_CANONICAL_SELECTED = ["business.general", "function.hr"]

# S4 仍锁定的两个动作（manage_department_types / cross_company_policy 已解锁）。
_LOCKED_ACTIONS = {
    "lift_human_approval_gate",
    "auto_modify_code",
}

# gate 显式批准的受控 evolution_events 写类型（S3 的 propose/apply + S4 的
# type_created/type_removed/policy_set）。此集合为 A 层受控写白名单。
_APPROVED_EVENT_TYPES = {
    "governance.propose",
    "governance.apply",
    "governance.type_created",
    "governance.type_removed",
    "governance.policy_set",
}

# B 层运行时治理边界闸事件（前缀 b.，区别于 A 层 governance.*；由 runtime_governance
# 接线点经 EvolutionEventLog 脱敏写入，不触碰 A 层 LOCKED_ACTIONS）。作为受控写例外，
# 允许出现但不强制出现在全流程测试中（仅 apply_proposal 路径落该事件）。
_B_GOVERNANCE_EVENT_TYPES = {
    "b.governance.gate",
}

# 受控写允许的全部事件类型（A 层白名单 ∪ B 层例外）。
_PERMITTED_EVENT_TYPES = _APPROVED_EVENT_TYPES | _B_GOVERNANCE_EVENT_TYPES

# (正则 pattern, 放行规则)
#   "zero"      -> 零命中
#   "def-only"  -> 命中仅允许出现在 `def ` 占位行（future hook 占位）
#   "decl-str"  -> 命中仅允许出现在 LOCKED_ACTIONS 列表的字符串字面量行
_FORBIDDEN = [
    (r"lift_human_approval_gate\(", "zero"),
    (r"auto_modify_code", "decl-str"),
    (r"manage_employees\(", "zero"),
    (r"connect_platform\(", "zero"),
    (r"roi_schema", "zero"),
    (r'app\.get\(\s*["\']/api/govern', "zero"),
    (r'app\.post\(\s*["\']/api/govern', "zero"),
    (r"\bvector\b", "zero"),
    (r"\bembedding\b", "zero"),
    (r"import openai", "zero"),
    (r"import boto3", "zero"),
    (r"import anthropic", "zero"),
    (r"from requests", "zero"),
    (r"import requests", "zero"),
]

# 符合 MANIFEST_FIELDS 7 键契约的合法 manifest 示例。
_VALID_MANIFEST = {
    "capability_set": ["x"],
    "tool_classes": ["y"],
    "quality_lines": ["z"],
    "output_channels": ["c"],
    "roi_schema": {},
    "guardrail_refs": [],
    "employee_role_spec": {},
}


class D4PlatformTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.db = Database(str(Path(self.tmp.name) / "curis.sqlite"))
        self.db.initialize()
        self.governance = CompanyGovernance(self.db)

    def tearDown(self):
        self.tmp.cleanup()

    # ── helpers ──
    def _grep_files(self, files, pattern):
        compiled = re.compile(pattern)
        hits = []
        for path in files:
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            for i, line in enumerate(text.splitlines(), start=1):
                if compiled.search(line):
                    hits.append(f"{path.relative_to(_REPO_ROOT)}:{i}: {line.strip()}")
        return hits

    def _event_log_events(self):
        return EvolutionEventLog(self.db).get_all()

    def _full_cycle(self, ceo_id, type_key, enabled, selected):
        """propose → approve → apply 全流程，返回 proposal_id。"""
        proposal = self.governance.propose_department_toggle(
            ceo_id, type_key, enabled, selected
        )
        self.governance.approve_proposal(proposal.proposal_id, "approver-x")
        self.governance.apply_proposal(proposal.proposal_id, decision_sink=AutoApproveSink())
        return proposal.proposal_id

    # ════════════════════════════════════════════════════════════════════
    # 保留的 S3 D4.impl 契约覆盖（propose/approve/apply / 公司态 / 不变式）
    # ════════════════════════════════════════════════════════════════════
    def test_facade_declares_required_methods_and_dataclasses(self):
        for method in (
            "get_governance_scope",
            "list_company_departments",
            "propose_department_toggle",
            "approve_proposal",
            "apply_proposal",
            "list_governance_audit",
            "manage_department_types",   # S4 已解锁：真实方法（不再占位）
            "cross_company_policy",      # S4 已解锁：真实方法（不再占位）
        ):
            self.assertTrue(hasattr(CompanyGovernance, method), f"缺少方法 {method}")
            self.assertTrue(callable(getattr(CompanyGovernance, method)))
        # S4 解锁：manage_department_types / cross_company_policy 不再抛 NotImplementedError
        self.assertIsNotNone(
            self.governance.manage_department_types(
                "edit", "business.general", category="business"
            )
        )
        self.assertIsNotNone(
            self.governance.cross_company_policy("list", "")
        )
        for cls in (GovernanceScope, DepartmentGovernanceView, GovernanceProposal):
            self.assertTrue(hasattr(cls, "__dataclass_fields__"))

    def test_get_governance_scope_returns_scope_with_locks_and_catalog(self):
        scope = self.governance.get_governance_scope("ceo-1", _CANONICAL_SELECTED)
        self.assertIsInstance(scope, GovernanceScope)
        self.assertIsInstance(scope.topology, CompanyTopology)
        # S4：locked_actions 仅剩仍锁定的 2 个（manage_department_types /
        # cross_company_policy 已解锁，不在其中）。
        self.assertEqual(set(scope.locked_actions), _LOCKED_ACTIONS)
        self.assertEqual(
            scope.selectable_type_keys, DepartmentCatalog(self.db).list_types()
        )

    def test_list_company_departments_length_and_approval(self):
        views = self.governance.list_company_departments("ceo-1", _CANONICAL_SELECTED)
        self.assertIsInstance(views, list)
        self.assertEqual(len(views), len(_CANONICAL_SELECTED))
        for view in views:
            self.assertIsInstance(view, DepartmentGovernanceView)
            self.assertTrue(view.requires_human_approval)

    def test_propose_department_toggle_returns_proposed_and_unknown_raises(self):
        proposal = self.governance.propose_department_toggle(
            "ceo-1", "function.hr", False, _CANONICAL_SELECTED
        )
        self.assertIsInstance(proposal, GovernanceProposal)
        self.assertEqual(proposal.status, "proposed")
        self.assertTrue(proposal.requires_human_approval)
        parsed = datetime.fromisoformat(proposal.proposed_at)
        self.assertIsNotNone(parsed)
        with self.assertRaises(KeyError):
            self.governance.propose_department_toggle(
                "ceo-1", "unknown.dept", False, _CANONICAL_SELECTED
            )

    def test_propose_persists_proposal_tenant_and_ceo_scoped(self):
        proposal = self.governance.propose_department_toggle(
            "ceo-alpha", "function.hr", True, _CANONICAL_SELECTED
        )
        row = self.db.get_governance_proposal(proposal.proposal_id)
        self.assertIsNotNone(row)
        self.assertEqual(row["tenant_id"], TenantContext.current_tenant_id())
        self.assertEqual(row["ceo_id"], "ceo-alpha")
        self.assertEqual(row["type_key"], "function.hr")
        self.assertEqual(row["status"], "proposed")
        self.assertEqual(row["proposed_enabled"], 1)
        other = self.governance.propose_department_toggle(
            "ceo-beta", "business.general", False, _CANONICAL_SELECTED
        )
        self.assertNotEqual(proposal.proposal_id, other.proposal_id)
        self.assertEqual(
            self.db.get_governance_proposal(other.proposal_id)["ceo_id"], "ceo-beta"
        )

    def test_approve_proposal_sets_approved(self):
        proposal = self.governance.propose_department_toggle(
            "ceo-1", "function.hr", False, _CANONICAL_SELECTED
        )
        self.governance.approve_proposal(proposal.proposal_id, "approver-7")
        row = self.db.get_governance_proposal(proposal.proposal_id)
        self.assertEqual(row["status"], "approved")
        self.assertEqual(row["approved_by"], "approver-7")
        self.assertIsNotNone(row["approved_at"])
        with self.assertRaises(ValueError):
            self.governance.approve_proposal(proposal.proposal_id, "approver-8")
        with self.assertRaises(KeyError):
            self.governance.approve_proposal("nope", "approver-9")

    def test_apply_refuses_when_not_approved(self):
        proposal = self.governance.propose_department_toggle(
            "ceo-1", "function.hr", False, _CANONICAL_SELECTED
        )
        with self.assertRaises(PermissionError):
            self.governance.apply_proposal(proposal.proposal_id, decision_sink=AutoApproveSink())
        state = self.db.get_company_department_state(
            TenantContext.current_tenant_id(), "ceo-1", "function.hr"
        )
        self.assertIsNone(state)
        types = [e["event_type"] for e in self._event_log_events()]
        self.assertNotIn("governance.apply", types)

    def test_apply_unknown_proposal_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.governance.apply_proposal("does-not-exist")

    def test_apply_persists_state_and_toggles_department_off(self):
        dept = DepartmentCatalog(self.db).create_department(
            type_key="function.hr", display_name="人事部-测试"
        )
        self.assertEqual(dept.status, "active")
        proposal_id = self._full_cycle("ceo-1", "function.hr", False, _CANONICAL_SELECTED)
        state = self.db.get_company_department_state(
            TenantContext.current_tenant_id(), "ceo-1", "function.hr"
        )
        self.assertIsNotNone(state)
        self.assertEqual(state["enabled"], 0)
        self.assertEqual(state["approved_by"], "approver-x")
        refreshed = DepartmentCatalog(self.db).get_department(dept.department_id)
        self.assertIsNotNone(refreshed)
        self.assertEqual(refreshed.status, "disabled")
        self.assertEqual(self.db.get_governance_proposal(proposal_id)["status"], "applied")
        types = [e["event_type"] for e in self._event_log_events()]
        self.assertIn("governance.apply", types)

    def test_apply_toggles_department_on_round_trip(self):
        DepartmentCatalog(self.db).create_department(
            type_key="function.hr", display_name="人事部-测试"
        )
        self._full_cycle("ceo-1", "function.hr", False, _CANONICAL_SELECTED)
        self.assertEqual(
            DepartmentCatalog(self.db)
            .get_department(
                DepartmentCatalog(self.db).list_departments()[0].department_id
            )
            .status,
            "disabled",
        )
        self._full_cycle("ceo-1", "function.hr", True, _CANONICAL_SELECTED)
        self.assertEqual(
            DepartmentCatalog(self.db).list_departments()[0].status, "active"
        )

    def test_reapply_after_applied_refused(self):
        self._full_cycle("ceo-1", "function.hr", False, _CANONICAL_SELECTED)
        proposal = self.governance.propose_department_toggle(
            "ceo-1", "function.hr", False, _CANONICAL_SELECTED
        )
        self.governance.approve_proposal(proposal.proposal_id, "approver-x")
        self.governance.apply_proposal(proposal.proposal_id, decision_sink=AutoApproveSink())
        with self.assertRaises(PermissionError):
            self.governance.apply_proposal(proposal.proposal_id, decision_sink=AutoApproveSink())

    def test_list_company_departments_reflects_real_state(self):
        DepartmentCatalog(self.db).create_department(
            type_key="function.hr", display_name="人事部-测试"
        )
        before = self.governance.list_company_departments("ceo-1", ["function.hr"])
        self.assertEqual(len(before), 1)
        self.assertTrue(before[0].enabled)
        self._full_cycle("ceo-1", "function.hr", False, _CANONICAL_SELECTED)
        after = self.governance.list_company_departments("ceo-1", ["function.hr"])
        self.assertEqual(len(after), 1)
        self.assertFalse(after[0].enabled)

    def test_tenant_context_invariant_preserved(self):
        self.assertEqual(TenantContext.current_tenant_id(), "selfuse")
        self.assertTrue(TenantContext.is_multi_tenant())

    def test_constructor_injects_database_only(self):
        import inspect

        sig = inspect.signature(CompanyGovernance.__init__)
        self.assertEqual(list(sig.parameters)[1:], ["database"])

    def test_database_additive_tables_present(self):
        with self.db.connect() as connection:
            names = {
                r["name"]
                for r in connection.execute(
                    "select name from sqlite_master where type='table'"
                )
            }
            # department_types 仍保持 D2 reservation 契约的 7 列（不可改 DDL）。
            cols = {
                c["name"]
                for c in connection.execute("pragma table_info(department_types)")
            }
            self.assertEqual(
                cols,
                {
                    "type_key",
                    "category",
                    "display_name",
                    "description",
                    "manifest_json",
                    "manifest_schema_version",
                    "is_system",
                },
            )
        self.assertIn("governance_proposals", names)
        self.assertIn("company_department_state", names)
        # S4 新增 additive 表：platform_policies（跨公司策略）+ department_type_status
        # （部门类型启用态；因 department_types 列固定为 7，启用态单独落库于此表）。
        self.assertIn("platform_policies", names)
        self.assertIn("department_type_status", names)

    # ════════════════════════════════════════════════════════════════════
    # S4 D4.platform 新增覆盖
    # ════════════════════════════════════════════════════════════════════
    def test_locked_actions_only_two_still_locked(self):
        # S4 解锁 manage_department_types / cross_company_policy；仅剩 2 个锁定。
        self.assertEqual(set(CompanyGovernance.LOCKED_ACTIONS), _LOCKED_ACTIONS)
        # 锁定的两个动作无真实实现方法（无调用路径）。
        self.assertFalse(hasattr(CompanyGovernance, "lift_human_approval_gate"))
        self.assertFalse(hasattr(CompanyGovernance, "auto_modify_code"))

    def test_manage_department_types_create_requires_human_approval_gate(self):
        # 无 approved_by → 拒绝（gate 未解除），不写库、不写事件。
        with self.assertRaises(PermissionError):
            self.governance.manage_department_types(
                "create", "custom.new", manifest=_VALID_MANIFEST
            )
        self.assertIsNone(self.db.get_department_type("custom.new"))
        types = [e["event_type"] for e in self._event_log_events()]
        self.assertNotIn("governance.type_created", types)

    def test_manage_department_types_create_success_writes_type_created(self):
        # 提供 approved_by → 真实创建 + 受控写 governance.type_created。
        row = self.governance.manage_department_types(
            "create",
            "custom.new",
            category="custom",
            display_name="新类型",
            description="测试",
            manifest=_VALID_MANIFEST,
            approved_by="admin-1",
        )
        self.assertEqual(row["type_key"], "custom.new")
        self.assertEqual(row["enabled"], 1)
        self.assertIsNotNone(self.db.get_department_type("custom.new"))
        # 受控写 governance.type_created。
        created = [
            e
            for e in self._event_log_events()
            if e["event_type"] == "governance.type_created"
        ]
        self.assertEqual(len(created), 1)
        self.assertEqual(created[0]["payload"]["type_key"], "custom.new")
        self.assertEqual(created[0]["payload"]["approved_by"], "admin-1")

    def test_manage_department_types_create_duplicate_rejected(self):
        self.governance.manage_department_types(
            "create", "custom.dup", manifest=_VALID_MANIFEST, approved_by="admin-1"
        )
        with self.assertRaises(ValueError):
            self.governance.manage_department_types(
                "create", "custom.dup", manifest=_VALID_MANIFEST, approved_by="admin-1"
            )

    def test_manage_department_types_manifest_contract_enforced(self):
        # 缺失 7 键契约 → ValueError（仅结构校验，不消费字段）。
        bad = {"capability_set": []}  # 缺 6 键
        with self.assertRaises(ValueError):
            self.governance.manage_department_types(
                "create", "custom.bad", manifest=bad, approved_by="admin-1"
            )
        # 非 dict → ValueError。
        with self.assertRaises(ValueError):
            self.governance.manage_department_types(
                "create", "custom.bad2", manifest="not-a-dict", approved_by="admin-1"
            )

    def test_manage_department_types_edit_disable_enable(self):
        self.governance.manage_department_types(
            "create", "custom.e", manifest=_VALID_MANIFEST, approved_by="admin-1"
        )
        # edit（无门控、无事件写）。
        self.governance.manage_department_types(
            "edit", "custom.e", display_name="改名后", category="business"
        )
        row = self.db.get_department_type("custom.e")
        self.assertEqual(row["display_name"], "改名后")
        self.assertEqual(row["category"], "business")
        # disable → enabled=0。
        self.governance.manage_department_types("disable", "custom.e")
        self.assertEqual(self.db.get_department_type("custom.e")["enabled"], 0)
        # enable → enabled=1。
        self.governance.manage_department_types("enable", "custom.e")
        self.assertEqual(self.db.get_department_type("custom.e")["enabled"], 1)
        # edit/disable/enable 不写 evolution_events。
        types = {e["event_type"] for e in self._event_log_events()}
        self.assertNotIn("governance.type_removed", types)

    def test_manage_department_types_remove_requires_human_approval_gate(self):
        self.governance.manage_department_types(
            "create", "custom.rm", manifest=_VALID_MANIFEST, approved_by="admin-1"
        )
        # 无 approved_by → 拒绝。
        with self.assertRaises(PermissionError):
            self.governance.manage_department_types("remove", "custom.rm")
        self.assertIsNotNone(self.db.get_department_type("custom.rm"))
        # 提供 approved_by → 真实移除 + 写 governance.type_removed。
        self.governance.manage_department_types(
            "remove", "custom.rm", approved_by="admin-2"
        )
        self.assertIsNone(self.db.get_department_type("custom.rm"))
        removed = [
            e
            for e in self._event_log_events()
            if e["event_type"] == "governance.type_removed"
        ]
        self.assertEqual(len(removed), 1)
        self.assertEqual(removed[0]["payload"]["type_key"], "custom.rm")
        self.assertEqual(removed[0]["payload"]["approved_by"], "admin-2")

    def test_manage_department_types_unknown_type_raises_keyerror(self):
        with self.assertRaises(KeyError):
            self.governance.manage_department_types("remove", "does.not.exist")
        with self.assertRaises(KeyError):
            self.governance.manage_department_types("edit", "does.not.exist")
        with self.assertRaises(KeyError):
            self.governance.manage_department_types("disable", "does.not.exist")

    def test_manage_department_types_empty_type_key_rejected(self):
        with self.assertRaises(ValueError):
            self.governance.manage_department_types(
                "create", "", manifest=_VALID_MANIFEST, approved_by="admin-1"
            )

    def test_cross_company_policy_set_get_list_round_trip(self):
        # set → upsert platform_policies + 写 governance.policy_set。
        row = self.governance.cross_company_policy(
            "set", "tenant_quota", {"max_depts": 10}, tenant_scope="all"
        )
        self.assertEqual(row["policy_key"], "tenant_quota")
        self.assertEqual(row["tenant_scope"], "all")
        self.assertEqual(row["enabled"], 1)
        import json as _json

        self.assertEqual(_json.loads(row["policy_value"]), {"max_depts": 10})
        # get 回读。
        fetched = self.governance.cross_company_policy("get", "tenant_quota")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched["policy_key"], "tenant_quota")
        # list 含该策略。
        listed = self.governance.cross_company_policy("list", "")
        keys = [p["policy_key"] for p in listed]
        self.assertIn("tenant_quota", keys)
        # 受控写 governance.policy_set。
        set_events = [
            e
            for e in self._event_log_events()
            if e["event_type"] == "governance.policy_set"
        ]
        self.assertEqual(len(set_events), 1)
        self.assertEqual(set_events[0]["payload"]["policy_key"], "tenant_quota")
        self.assertEqual(set_events[0]["payload"]["tenant_scope"], "all")

    def test_cross_company_policy_tenant_scoped_and_update(self):
        self.governance.cross_company_policy(
            "set", "access_rule", {"allow": True}, tenant_scope="tenant-a"
        )
        # upsert 同 key 覆盖 value / tenant_scope。
        self.governance.cross_company_policy(
            "set", "access_rule", {"allow": False}, tenant_scope="all"
        )
        fetched = self.governance.cross_company_policy("get", "access_rule")
        import json as _json

        self.assertEqual(_json.loads(fetched["policy_value"]), {"allow": False})
        self.assertEqual(fetched["tenant_scope"], "all")
        # list 按 tenant_scope 过滤：'all' 返回全局 + 该租户；'tenant-x' 仅返回全局。
        all_rows = self.governance.cross_company_policy("list", "", tenant_scope="all")
        self.assertIn("access_rule", [p["policy_key"] for p in all_rows])
        scoped = self.governance.cross_company_policy(
            "list", "", tenant_scope="tenant-x"
        )
        self.assertIn("access_rule", [p["policy_key"] for p in scoped])

    def test_cross_company_policy_disable_enable(self):
        self.governance.cross_company_policy(
            "set", "toggle_me", {"x": 1}, tenant_scope="all"
        )
        self.governance.cross_company_policy("disable", "toggle_me")
        self.assertEqual(
            self.governance.cross_company_policy("get", "toggle_me")["enabled"], 0
        )
        self.governance.cross_company_policy("enable", "toggle_me")
        self.assertEqual(
            self.governance.cross_company_policy("get", "toggle_me")["enabled"], 1
        )

    def test_cross_company_policy_unknown_or_empty_rejected(self):
        with self.assertRaises(KeyError):
            self.governance.cross_company_policy("enable", "nope")
        with self.assertRaises(ValueError):
            self.governance.cross_company_policy("set", "")
        with self.assertRaises(ValueError):
            self.governance.manage_department_types("bogus-action", "x")

    # ── AC4/6: /api/platform/* 存在 + 鉴权 + 真实落地 ──
    def _platform_client(self):
        os.environ.setdefault("CURIS_PLATFORM_ADMIN_TOKEN", "platform-admin-dev")
        return TestClient(
            create_app(str(Path(self.tmp.name) / "platform_api.sqlite"))
        )

    def test_platform_endpoints_exist_and_require_auth(self):
        client = self._platform_client()
        # 无令牌 → 401。
        self.assertEqual(client.get("/api/platform/department-types").status_code, 401)
        self.assertEqual(
            client.post(
                "/api/platform/department-types",
                json={"type_key": "x.custom", "manifest": _VALID_MANIFEST},
            ).status_code,
            401,
        )
        self.assertEqual(client.get("/api/platform/policies").status_code, 401)
        self.assertEqual(client.get("/api/platform/tenants").status_code, 401)
        # 错误令牌 → 401。
        bad = {"Authorization": "Bearer wrong-token"}
        self.assertEqual(
            client.get("/api/platform/department-types", headers=bad).status_code, 401
        )

    def test_platform_department_type_create_requires_approval_via_api(self):
        client = self._platform_client()
        auth = {"Authorization": "Bearer platform-admin-dev"}
        # 缺 approved_by → 403（human-approval 门控）。
        resp = client.post(
            "/api/platform/department-types",
            headers=auth,
            json={"type_key": "api.custom", "manifest": _VALID_MANIFEST},
        )
        self.assertEqual(resp.status_code, 403)
        # 提供 approved_by → 201 且真实落地（GET 可见）。
        resp = client.post(
            "/api/platform/department-types",
            headers=auth,
            json={
                "type_key": "api.custom",
                "manifest": _VALID_MANIFEST,
                "approved_by": "admin-api",
            },
        )
        self.assertEqual(resp.status_code, 201)
        listed = client.get("/api/platform/department-types", headers=auth).json()
        self.assertIn("api.custom", [t["type_key"] for t in listed])

    def test_platform_department_type_remove_requires_approval_via_api(self):
        client = self._platform_client()
        auth = {"Authorization": "Bearer platform-admin-dev"}
        client.post(
            "/api/platform/department-types",
            headers=auth,
            json={
                "type_key": "api.rm",
                "manifest": _VALID_MANIFEST,
                "approved_by": "admin-api",
            },
        )
        # 缺 approved_by → 403。
        self.assertEqual(
            client.delete(
                "/api/platform/department-types/api.rm", headers=auth
            ).status_code,
            403,
        )
        # 提供 approved_by → 200 且已移除。
        resp = client.delete(
            "/api/platform/department-types/api.rm",
            headers=auth,
            params={"approved_by": "admin-api"},
        )
        self.assertEqual(resp.status_code, 200)
        listed = client.get("/api/platform/department-types", headers=auth).json()
        self.assertNotIn("api.rm", [t["type_key"] for t in listed])

    def test_platform_policy_set_and_tenants_via_api(self):
        client = self._platform_client()
        auth = {"Authorization": "Bearer platform-admin-dev"}
        # 设置策略 → 201。
        resp = client.post(
            "/api/platform/policies",
            headers=auth,
            json={"policy_key": "api_quota", "value": {"n": 5}, "tenant_scope": "all"},
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()["policy_key"], "api_quota")
        # 列出策略含该 key。
        listed = client.get("/api/platform/policies", headers=auth).json()
        self.assertIn("api_quota", [p["policy_key"] for p in listed])
        # 租户总览 → 200 且含 default 租户。
        tenants = client.get("/api/platform/tenants", headers=auth).json()
        self.assertIn("selfuse", [t["tenant_id"] for t in tenants["tenants"]])

    def test_existing_api_unchanged(self):
        client = self._platform_client()
        # 既有 /api/tasks 不受影响（无鉴权要求，保持原语义）。
        self.assertEqual(client.get("/api/tasks").status_code, 200)
        self.assertEqual(client.get("/health").status_code, 200)

    # ── AC6: 受控 evolution_events 写仅 5 个批准类型（源码级 + 运行时）──
    def test_controlled_evolution_events_source_only_approved(self):
        """源码级受控写核查：governance.py 中 record 的 event_type 仅允许集合。

        允许集合 = A 层白名单 ∪ B 层运行时治理边界闸例外（b.governance.gate）。
        """
        text = (_APP_DIR / "governance.py").read_text(encoding="utf-8")
        event_types = re.findall(r'event_type\s*=\s*["\']([^"\']+)["\']', text)
        self.assertTrue(event_types, "governance.py 应至少写一次治理事件")
        for et in event_types:
            self.assertIn(
                et,
                _PERMITTED_EVENT_TYPES,
                f"受控写越权：非批准治理事件 {et!r}",
            )

    def test_controlled_evolution_events_runtime_only_approved(self):
        # 全流程（S3）+ 类型 CRUD（S4）+ 策略（S4）后，evolution_events 仅含允许类型。
        self._full_cycle("ceo-1", "function.hr", False, _CANONICAL_SELECTED)
        self.governance.manage_department_types(
            "create", "custom.rt", manifest=_VALID_MANIFEST, approved_by="admin-1"
        )
        self.governance.manage_department_types(
            "remove", "custom.rt", approved_by="admin-1"
        )
        self.governance.cross_company_policy(
            "set", "rt_policy", {"v": 1}, tenant_scope="all"
        )
        event_types = {e["event_type"] for e in self._event_log_events()}
        self.assertTrue(
            event_types.issubset(_PERMITTED_EVENT_TYPES),
            f"受控写越权：evolution_events 含非批准事件 {event_types - _PERMITTED_EVENT_TYPES}",
        )
        # A 层 5 个批准类型均至少出现一次（证明 S4 三新事件确实经 gate 写入）。
        # B 层 b.governance.gate 为允许例外，但不强制出现（仅 apply_proposal 路径落该事件）。
        for et in _APPROVED_EVENT_TYPES:
            self.assertIn(et, event_types, f"缺少预期治理事件 {et}")

    # ── AC7: forbidden-scope guard clean ──
    def test_forbidden_scope_keywords(self):
        for pattern, kind in _FORBIDDEN:
            hits = self._grep_files(_CHANGED_APP_FILES, pattern)
            if kind == "zero":
                self.assertEqual(
                    hits, [], f"禁止区命中（零容忍）{pattern!r}: {hits}"
                )
            elif kind == "def-only":
                for hit in hits:
                    code = hit.split(": ", 1)[-1]
                    self.assertTrue(
                        code.strip().startswith("def "),
                        f"禁止区命中非 def 调用 {pattern!r}: {hit}",
                    )
            elif kind == "decl-str":
                for hit in hits:
                    code = hit.split(": ", 1)[-1]
                    self.assertTrue(
                        re.match(r'^\s*"[^"]*",?\s*$', code.strip()),
                        f"禁止区命中非声明字符串 {pattern!r}: {hit}",
                    )

    def test_forbidden_scope_no_department_id_filter(self):
        hits = self._grep_files(_CHANGED_APP_FILES, r"WHERE\s+department_id")
        self.assertEqual(hits, [], f"禁止区命中 WHERE department_id: {hits}")


if __name__ == "__main__":
    unittest.main()
