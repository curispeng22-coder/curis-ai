# Phase-9A P2 Capability Package —— 实现设计蓝图

> 配套契约：`docs/contracts/capability-package-commercial-contract.md`
> 实现语言：Python（FastAPI + sqlite3 + pydantic，无 ORM），风格与 P0/P1 的
> `pricing_rules` / `quota_rules` 完全一致。

---

## 1. 数据模型（DDL）

建表位于 `backend/app/database.py` 的 `initialize()`（与 `pricing_rules` / `quota_rules`
同一 `with self.db.connect()` 上下文，幂等 `create table if not exists`）：

```sql
create table if not exists capability_packages (
  package_id            text primary key,
  name                  text not null,
  description           text not null default '',
  capability_ids        text not null default '[]',   -- JSON 数组：能力 key 列表
  connector_ids         text not null default '[]',   -- JSON 数组：连接器 key 列表
  workflow_template_ids text not null default '[]',   -- JSON 数组：工作流模板 id 列表
  employee_template_ids text not null default '[]',   -- JSON 数组：员工模板 id 列表
  pricing_reference     text,                        -- 引用 plan_id（价格来自 pricing_rules）
  quota_reference       text,                        -- 引用 plan_id（配额来自 quota_rules）
  availability          text not null default 'public'
                         check (availability in ('public','tenant_invite_only','enterprise_only')),
  status                text not null default 'draft'
                         check (status in ('draft','active','disabled')),
  created_at            text not null default current_timestamp,
  updated_at            text not null default current_timestamp
);

create index if not exists idx_capability_packages_status on capability_packages(status);
create index if not exists idx_capability_packages_availability on capability_packages(availability);
```

**索引**：`status`、`availability` 加速列表过滤。无需「每 X 仅一条 active」覆盖索引（允许多包并行 active）。

---

## 2. Seed（示例官方包，可改写占位）

`initialize()` 末尾 `insert or ignore` 注入 1 条示例官方包（幂等、可重复执行）：

```python
_SEED_CAPABILITY_PACKAGES = [
    ("cp_content_ops", "内容运营包",
     "面向内容生产与分发的官方能力包（模型/工具/连接器能力 + 内容运营 AI）",
     '["task_execution","tenant_private_capabilities","workflow_sop"]',
     '["xiaohongshu","douyin","shopify"]',
     "[]", "[]",                       # 工作流/员工模板初始为空，由 Admin 经 API 配置
     "plan_pro", "plan_pro", "public", "active"),
]
```

> 数值/引用均为**可改写占位**（非写死不可改）：`pricing_reference`/`quota_reference` 指向
> `plan_pro`，Admin 可经 API 改为任意 plan。**无硬编码业务数值**。

---

## 3. `billing_store.py` 方法

新增 2 个校验常量 + 6 个方法（风格对照 P1 quota_rules）：

```python
_VALID_PACKAGE_STATUSES = frozenset({"draft", "active", "disabled"})
_VALID_PACKAGE_AVAILABILITY = frozenset({"public", "tenant_invite_only", "enterprise_only"})
```

| 方法 | 职责 |
|------|------|
| `_capability_package_dto(row)` | 行 → dict（JSON 数组字段经 `_parse_json` 还原为 list） |
| `_get_capability_package_row(package_id)` | 取原始行或 `None` |
| `_validate_json_id_list(value, field)` | 校验组成引用为字符串数组（或 None→空） |
| `create_capability_package(...)` | 插入；校验 name 非空、枚举合法、引用数组合法；生成 `cp_` id |
| `update_capability_package(package_id, **fields)` | 部分更新；`KeyError`→404，`ValueError`→422；无覆盖语义 |
| `list_capability_packages(status, availability, name)` | 列表过滤（name 用 `like`） |
| `get_capability_package(package_id)` | 单条；缺失 `KeyError`→404 |

连接模式沿用 `with self.db.connect() as connection:`（退出自动 commit）；SQL 全部 `?` 占位。
组成引用列以 `json.dumps(..., ensure_ascii=False)` 写入、以 `_parse_json` 读出。

---

## 4. `main.py` 路由 + pydantic

模型：`CapabilityPackageCreateIn` / `CapabilityPackageUpdateIn`（全部可选字段 `| None = None`）。

路由（全部 `_require_platform_admin`，401 非 403）：

```python
@app.get("/api/platform/capability-packages")                      # 列表 + 过滤
@app.post("/api/platform/capability-packages", status_code=201)     # 创建
@app.get("/api/platform/capability-packages/{package_id}")          # 单条（404）
@app.put("/api/platform/capability-packages/{package_id}")          # 部分更新（404/422）
```

错误映射：`ValueError`→422（非法 availability/status/空名/非数组）、`KeyError`→404（包不存在）。

---

## 5. 测试矩阵（T1–T14）

| 用例 | 覆盖 |
|------|------|
| T1 建表幂等 | `capability_packages` + 2 索引存在 |
| T2 seed 幂等 | 示例包仅 1 条 active，重复 initialize 不重复 |
| T3 创建→201 | JSON 数组正确存取 |
| T4 获取单条→200 | `cp_content_ops` 可读 |
| T5 列表过滤 | status/availability/name 过滤生效 |
| T6 部分更新 | 改 capability_ids/availability/status，未提供字段不变 |
| T7 非法 availability→422 | `worldwide` 被拒 |
| T8 非法 status→422 | `published` 被拒 |
| T9 空名→422 | name="" 被拒 |
| T10 获取不存在→404 | `cp_nope` 返回 404 |
| T11 不硬编码 | 改 `pricing_reference` 后 API 返回新值（非写死） |
| T12 守卫 401 | 无令牌 → 401（非 403） |
| T13 availability 三值 | public/tenant_invite_only/enterprise_only 均接受 |
| T14 红线静态校验 | 源码不含 marketplace/payment/invoice/billing_event/value_pricing/auto_sale 逻辑符号；无 DELETE capability_packages |

---

## 6. 受影响文件清单

| 文件 | 改动 |
|------|------|
| `backend/app/database.py` | 新增 `capability_packages` 建表 + 2 索引 + 示例包 seed |
| `backend/app/billing_store.py` | 2 常量 + 6 方法（含 DTO/校验/CRUD/列表） |
| `backend/app/main.py` | 2 pydantic 模型 + 4 路由 |
| `backend/tests/test_capability_packages.py` | 新增测试 14 例 |
| `docs/contracts/capability-package-commercial-contract.md` | 新增契约 |
| `docs/design/phase9a-p2-cappkg-implementation-design.md` | 新增实现设计 |

**未改动**：`quotas` / `pricing_rules` / `quota_rules` 既有表与代码；Workspace 任何路由/数据；
Credential Vault / Shared Contract / Employee Runtime / Usage Event。

---

## 7. 红线确认

- 不实现 Marketplace / Payment / Invoice / BillingEvent / 超额收费 / 自动销售。
- 不修改 Workspace 执行链；不触碰 `/api/workspace/*` private 路由。
- 不触碰 Credential Vault / Shared Contract / Employee Runtime / Usage Event 写入。
- `capability_packages` 无 DELETE（更新仅 `UPDATE`；停用改 `status='disabled'`）。
- 所有 seed 值与引用均为可改写占位，无硬编码不可改业务数值。
- 全部 SQL `?` 占位，组成引用列仅经 `json.dumps`/`_parse_json` 处理。
