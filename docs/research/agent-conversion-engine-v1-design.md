# Agent 拆解转换引擎 V1 — 资产格式设计（章节 4 / 章节 6 / MVP 切片）

> **文档性质：设计稿 / pre-gate / 不实现**
> 作者：架构师 高见远（software-architect）
> 阶段：纯规划 / 资产格式设计，不写实现代码、不 seed 真实资产、不碰 L2 红线冻结项
> 衔接对象：产品经理 许清楚 前半草稿 `agent-conversion-engine-v1-plan.md`（章节 1/2/3/5 + 候选 harvest 清单）
> 红线声明：⚠️ 把外部 agent 真实转换为 Employee / Skill / Department / Workflow 属 **L2 暂停四项 #4 红线冻结**；本报告所有 schema / 映射 / 清单均为 pre-gate 设计稿，解冻前不执行任何对 `employee_templates` / `skill_templates` / `tool_templates` / `workflow_templates` / `department_templates` / `persona_templates` 的真实写操作。

---

## 0. 关于真实资产体系基线的勘误（重要，开篇先读）

本报告在动手前先读取了 `backend/app/database.py` 的真实 `CREATE TABLE` 语句，发现**实际落地表结构与 PM 草稿第 0 节的假设存在 3 处关键偏差**，必须先纠正设计基线，否则映射会落空：

| # | PM 草稿假设 | 真实 `database.py` 事实 | 对设计的影响 |
|---|------|------|------|
| ① | `et_*` 含扩展字段 `image_ref_json`（头像/主题色） | `employee_templates` **无 `image_ref_json` 列**；该字段存在于 `persona_templates.image_ref_json`（additive，行 1080） | 头像/主题色必须经由 `et_*.persona_ref → persona_templates.image_ref_json` 落地，**不能直接写 `et_*`** |
| ② | `et_*` 含 `applicable_departments`（适用多部门） | `employee_templates` **无此列**；仅有单值 `department_type`（→ `department_types.type_key`）；反向"哪些部门含本员工"由 `department_templates.default_employee_templates_json` 承载 | agency 的 `services` 绑定提示只能分解为「单 `department_type` 标签 + 候选工具绑定」，无正向多部门列 |
| ③ | `wt_*` 属 Phase-5+ 预留，当前仅沉淀设计稿 | `workflow_templates` + `workflow_contents`（wl_* 折叠）**已经落地**（行 712、942） | agency 的 Workflow Process / runbooks **现在即可映射到真实 `wt_*` 表结构**，schema 已就绪；仅缺内容补全与人工评审 |

**真实落地表与关键列（已逐一核实）：**

- `employee_templates`：`id, slug, name, role, responsibility, description, department_type, default_instructions, default_capability_types_json, default_model_policy_json, default_workflow_step_types_json, guardrails_json, source, tenant_id, enabled, created_at` + additive：`persona_ref, default_skill, default_tool, persona_overrides_json, version, status, updated_at`
- `persona_templates`：`persona_id, slug, name, archetype(CHECK 6值), traits_json, communication_style_json, reporting_style_json, decision_style, collaboration_style_json, version, status, source, tenant_id, enabled, created_at, updated_at` + additive：`image_ref_json`
- `skill_templates`：`skill_template_id, slug, name, description, skill_type, default_capability_types_json(默认["model"]), instruction_excerpt, source, tenant_id, status, created_from_template_id, created_at, updated_at` + additive：`version, category`
- `tool_templates`：`tool_template_id, slug, name, description, tool_type, default_capability_types_json(默认["tool"]), instruction_excerpt, source, tenant_id, status, version, created_at, updated_at`
- `workflow_templates`：`id, name, description, source, tenant_id, department_type(默认 software_rnd), process_type(默认 sequential), steps_json, status, created_at, updated_at`
- `workflow_contents`（wl_* 折叠）：`workflow_content_id, name, workflow_template_ref, pack, owner_roles_json, step_templates_json, source_attribution, version, status, source, tenant_id, enabled, created_at, updated_at`
- `department_templates`：`id, slug, name, department_type, description, default_employee_templates_json, default_workflow_template_id, default_capability_types_json, source, tenant_id, enabled, created_at` + additive：`version, status`
- `department_types`（类型注册表，已解禁，7 列 DDL 锁定）：`type_key, category, display_name, description, manifest_json(7键), manifest_schema_version, is_system`

> 注：PM 草稿第 0 节称「et_* 现有 12 字段」，真实 base 为上述 16 列（含 additive 后即约 23 列）。命名空间约定：`official.employee.*` / `tenant:<tid>:employee.*` / `marketplace:employee.*`；三态 `source` CHECK `('official','tenant_private','marketplace')`。

---

## 章节 4：Agent → Curis Employee 目标资产格式设计

### 4.1 CanonicalAgentSpec 字段级中间 schema（统一中间表示）

所有 `SourceAdapter` 把异构源**归一化**为下述中间 schema，再共享章节 3 的同一转换流水线。这是转换引擎的"单一归一契约"——源解析与 Curis 映射彻底解耦。

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://curis.ai/schemas/CanonicalAgentSpec/v1",
  "title": "CanonicalAgentSpec",
  "description": "外部 Agent 转 Curis 资产的统一中间表示。所有 SourceAdapter.parse() 的输出，喂入章节 3 的映射流水线。设计稿，不实现。",
  "type": "object",
  "required": ["spec_version", "source", "license", "division", "identity", "security_scan"],
  "properties": {
    "spec_version": { "type": "string", "const": "1.0.0" },
    "source": {
      "type": "object",
      "description": "来源治理元数据",
      "required": ["adapter", "repo_url", "entry_path"],
      "properties": {
        "adapter": {
          "type": "string",
          "enum": [
            "MarkdownFrontmatterAdapter", "SkillRepoAdapter", "CrewYAMLAdapter",
            "AgentConfigAdapter", "PlatformExportAdapter", "MCPManifestAdapter"
          ]
        },
        "repo_url": { "type": "string", "format": "uri" },
        "entry_path": { "type": "string", "description": "源内条目路径/文件" },
        "fetched_at": { "type": "string", "format": "date-time" }
      }
    },
    "license": {
      "type": "object",
      "description": "许可合规闸门输入",
      "required": ["spdx", "commercial_use", "copyleft", "attribution_required"],
      "properties": {
        "spdx": { "type": "string", "examples": ["MIT", "Apache-2.0", "GPL-3.0", "AGPL-3.0"] },
        "commercial_use": { "type": "boolean" },
        "copyleft": { "type": "boolean", "description": "强 copyleft（GPL/AGPL）须过滤拒绝" },
        "attribution_required": { "type": "boolean", "description": "true 时须保留原作者/许可于 source_attribution" },
        "raw_license_text": { "type": "string" }
      }
    },
    "division": {
      "type": "object",
      "description": "源分区 → Curis 部门映射",
      "required": ["source_key", "label"],
      "properties": {
        "source_key": { "type": "string", "examples": ["marketing", "sales", "finance"] },
        "label": { "type": "string" },
        "target_dt_type": { "type": "string", "description": "→ department_types.type_key，如 business.general" },
        "target_dt_id": { "type": "string", "description": "→ 目标 department_templates.id（division 级 harvest 时填）" }
      }
    },
    "identity": {
      "type": "object",
      "description": "角色身份（frontmatter 层）",
      "required": ["name", "role"],
      "properties": {
        "name": { "type": "string", "minLength": 1, "maxLength": 120 },
        "role": { "type": "string", "minLength": 1, "maxLength": 80 },
        "slug": { "type": "string", "pattern": "^[a-z0-9][a-z0-9_-]{1,78}$" },
        "description": { "type": "string", "maxLength": 500 },
        "emoji": { "type": "string", "maxLength": 4, "description": "清洗后单 grapheme emoji（见 4.4 Q5）" },
        "color": { "type": "string", "pattern": "^#[0-9a-fA-F]{6}$", "description": "清洗后 hex" },
        "vibe": { "type": "string", "maxLength": 200 }
      }
    },
    "mission": {
      "type": "object",
      "description": "目标/职责/约束（→ et_*.responsibility + default_instructions + guardrails_json）",
      "properties": {
        "summary": { "type": "string", "maxLength": 1000 },
        "responsibilities": { "type": "array", "items": { "type": "string", "maxLength": 400 }, "maxItems": 30 },
        "critical_rules": { "type": "array", "items": { "type": "string", "maxLength": 400 }, "maxItems": 50 }
      }
    },
    "persona": {
      "type": "object",
      "description": "人格层（→ pt_* 或 et_*.persona_overrides_json）",
      "properties": {
        "archetype": {
          "type": "string",
          "enum": [
            "supportive_coach", "direct_executor", "analytical_advisor",
            "creative_explorer", "balanced_facilitator", "risk_aware_guardian"
          ]
        },
        "traits": { "type": "array", "items": { "type": "string", "maxLength": 60 }, "maxItems": 20 },
        "communication_style": { "type": "object", "additionalProperties": { "type": "string" }, "maxProperties": 10 },
        "reporting_style": { "type": "object", "additionalProperties": { "type": "string" }, "maxProperties": 10 },
        "decision_style": {
          "type": "string",
          "enum": ["consultative", "autonomous", "delegative", "data_driven"]
        },
        "collaboration_style": { "type": "object", "additionalProperties": { "type": "string" }, "maxProperties": 10 }
      }
    },
    "deliverables": {
      "type": "object",
      "description": "交付物 + 隐含技术栈（→ default_instructions + skl_*/tl_* 抽取）",
      "properties": {
        "text_blocks": { "type": "array", "items": { "type": "string", "maxLength": 600 }, "maxItems": 30 }
      }
    },
    "workflow": {
      "type": "object",
      "description": "工作流步骤（→ wt_*.steps_json / workflow_contents）",
      "properties": {
        "process_type": { "type": "string", "enum": ["sequential", "parallel"], "default": "sequential" },
        "steps": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["step_order", "name"],
            "properties": {
              "step_order": { "type": "integer", "minimum": 1 },
              "name": { "type": "string", "maxLength": 120 },
              "instruction_excerpt": { "type": "string", "maxLength": 800 },
              "expected_output": { "type": "string", "maxLength": 400 },
              "owner_role": { "type": "string", "maxLength": 80, "description": "单 agent 源缺省=该 agent role" }
            }
          },
          "maxItems": 40
        }
      }
    },
    "capability_candidates": {
      "type": "object",
      "description": "NLP 抽取后的隐含工具/技能候选（candidate 草案，不自动 seed）",
      "properties": {
        "tool_candidates": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["name_hint"],
            "properties": {
              "name_hint": { "type": "string", "maxLength": 80 },
              "evidence": { "type": "string", "maxLength": 300 },
              "matched_tool_id": { "type": "string", "description": "命中 Curis tl_* 则填，否则空 → 生成候选" },
              "suggested_tool_type": { "type": "string" }
            }
          }
        },
        "skill_candidates": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["name_hint"],
            "properties": {
              "name_hint": { "type": "string", "maxLength": 80 },
              "evidence": { "type": "string", "maxLength": 300 },
              "matched_skill_id": { "type": "string" },
              "suggested_skill_type": { "type": "string" }
            }
          }
        }
      }
    },
    "memory_notes": {
      "type": "array", "items": { "type": "string", "maxLength": 400 }, "maxItems": 20,
      "description": "Learning & Memory 章节；Curis Phase-4 不支持员工记忆，仅记录不映射（后置）"
    },
    "success_metrics": {
      "type": "array", "items": { "type": "string", "maxLength": 300 }, "maxItems": 20,
      "description": "成功指标 → wt_* 验收条件或 quality gate（无独立 et 字段）"
    },
    "security_scan": {
      "type": "object",
      "description": "安全红线扫描结果（关卡⑦输入）",
      "required": ["credential_patterns", "prompt_injection_flags", "overclaim_flags"],
      "properties": {
        "credential_patterns": {
          "type": "array", "items": { "type": "string" }, "maxItems": 20,
          "description": "命中的 api_key/secret/token/password 模式，须剥离，绝不持久化"
        },
        "prompt_injection_flags": {
          "type": "array", "items": { "type": "string" }, "maxItems": 20,
          "description": "试图覆盖系统指令/外泄/越权的注入指令"
        },
        "overclaim_flags": {
          "type": "array", "items": { "type": "string" }, "maxItems": 20,
          "description": "越权表述（如'执行任意代码'）须降级为受控 skl_* 或剔除"
        }
      }
    },
    "conversion_disposition": {
      "type": "object",
      "description": "转换处置建议（评审稿元数据，非 DB 列）",
      "properties": {
        "employee_action": { "type": "string", "enum": ["create", "enhance_existing", "skip"], "default": "create" },
        "existing_official_id": { "type": "string", "description": "enhance_existing 时填，如 official.employee.tech_lead" },
        "star_rating": { "type": "integer", "minimum": 1, "maximum": 5 },
        "notes": { "type": "string", "maxLength": 500 }
      }
    }
  }
}
```

> **设计原则**：`CanonicalAgentSpec` 刻意区分「内容字段」（identity/mission/persona/workflow/deliverables）与「治理字段」（source/license/security_scan/conversion_disposition）。后者在映射阶段被消费但不进入 Curis 业务表（除 `source` 三态与 `license`→`source_attribution` 文本）。

---

### 4.2 SourceAdapter 接口契约（抽象基类，仅签名 + docstring）

> 仅定义契约，不实现逻辑。所有适配器实现同一接口，输出 `CanonicalAgentSpec`。

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Iterable

from .canonical import CanonicalAgentSpec  # 见 4.1 JSON Schema 的 Python 绑定（仅类型，不实现）


@dataclass
class SourceEntry:
    """源内一个可转换条目的轻量引用。"""
    entry_id: str
    entry_path: str
    title: str
    raw_ref: Any  # 源内部引用（URL / 文件路径 / 解析对象），适配器自用，不跨层传递


@dataclass
class SourceMetadata:
    """治理元数据，供关卡①许可闸门与关卡⑦评审消费。"""
    adapter: str
    repo_url: str
    license_spdx: str
    commercial_use: bool
    copyleft: bool
    attribution_required: bool
    fetched_at: str


class SourceAdapter(ABC):
    """外部 Agent 来源的归一化适配器契约。

    所有异构来源（agency-agents / skill 仓库 / CrewAI / AutoGPT / Coze-Dify / MCP Registry）
    均实现本接口，把源原始内容转换为统一的 CanonicalAgentSpec，从而与 Curis 映射逻辑解耦。
    本类仅为接口契约（设计稿），不含任何实现逻辑，不读写数据库。
    """

    @abstractmethod
    def discover(self, source_root: Any) -> Iterable[SourceEntry]:
        """枚举源内可转换为 Curis 资产的条目（agent / skill / tool）。

        Args:
            source_root: 源根引用（本地目录 / 仓库 URL / 导出 JSON 根）。
        Returns:
            可迭代的 SourceEntry 列表；非源目录（如 integrations/、strategy/ 分发输出）
            须在此阶段过滤，不进入后续流水线。
        """
        raise NotImplementedError

    @abstractmethod
    def fetch(self, entry: SourceEntry) -> Any:
        """拉取单个条目的原始内容（.md / .json / .yaml）。

        Args:
            entry: discover() 产出的条目引用。
        Returns:
            原始内容载体（文本或结构化对象）；不含任何归一化或安全清洗。
        """
        raise NotImplementedError

    @abstractmethod
    def parse(self, raw: Any, entry: SourceEntry) -> CanonicalAgentSpec:
        """把原始内容归一化为 CanonicalAgentSpec。

        须完成：frontmatter/字段抽取、章节切分、emoji/color 清洗（见 4.4 Q5）、
        license 字段填充、security_scan 初扫（credential/prompt-injection/overclaim 模式）。
        结构化不足的来源（如 agency-agents）应在 parse 后调用 extract_capabilities。
        """
        raise NotImplementedError

    @abstractmethod
    def extract_capabilities(self, spec: CanonicalAgentSpec) -> CanonicalAgentSpec:
        """对结构化不足的来源，抽取隐含工具/技能候选（candidate）。

        输入已有的 spec（多为自然语言内容），输出补全 capability_candidates
        （tool_candidates / skill_candidates），并按 Curis 115 工具库 / 52 技能库做命中匹配
        （命中填 matched_tool_id / matched_skill_id，未命中留空 → 生成候选）。
        严禁凭空生成工具 id；无法命中者一律标记为 candidate。
        """
        raise NotImplementedError

    @abstractmethod
    def get_metadata(self) -> SourceMetadata:
        """返回治理元数据：适配器名、源 URL、许可（SPDX / 商用 / copyleft / 署名）、抓取时间。

        关卡①许可闸门据此过滤不可商用 / 强 copyleft 源。
        """
        raise NotImplementedError
```

---

### 4.3 目标资产字段级映射 schema（CanonicalAgentSpec → Curis 真实表）

下列映射表以 **4.1 的 CanonicalAgentSpec 字段** 为左键，**Curis 真实列**为右键。所有 `source` 在解冻前统一以 `official`（命名空间 `official.*`），解冻后经 Admin 写通道 seed；设计阶段全部产出 **candidate 草案**。

#### 4.3.1 → `employee_templates`（et_*）

| CanonicalAgentSpec 字段 | 目标列 | 类型/约束 | 转换与说明 |
|---|------|------|------|
| `identity.slug` + `division.target_dt_type` | `id` | text PK | 命名空间 `official.employee.{slug}`；冲突需 slug 唯一化 |
| `identity.name` | `name` | text NOT NULL | 直接复制 |
| `identity.role` | `role` | text NOT NULL | 直接复制（如 `marketing_growth_hacker`） |
| `identity.description` | `description` | text | 直接复制 |
| `mission.summary` | `responsibility` | text | **CEO 面向公开**；一句话职责 |
| `mission.summary` + `mission.responsibilities` + `mission.critical_rules` + `deliverables.text_blocks` + `workflow.steps[].instruction_excerpt` | `default_instructions` | text | **隐藏不暴露 CEO**；完整 prompt 模板拼接 |
| `mission.critical_rules[]` | `guardrails_json` | text(JSON) | 数组；结构化约束（与 default_instructions 互补） |
| `division.target_dt_type` | `department_type` | text | → `department_types.type_key`（单值 forward） |
| `capability_candidates`（命中 tl_*→加 `tool`；命中 connector 类→加 `connector`；skl_*→`model`） | `default_capability_types_json` | text(JSON) | 如 `["model","tool"]`；仅类型偏好 |
| `persona`（复用既有 persona 时） | `persona_ref` | text | → `persona_templates.persona_id`（如 `pt_{slug}`） |
| `persona`（本员工专属微调） | `persona_overrides_json` | text(JSON) | 仅存 delta；与 persona_ref 深合并（见 4.4 Q1） |
| `identity.emoji` / `identity.color` | —（经 `persona_ref`） | — | **不直接落 et_***；写入 `persona_templates.image_ref_json`（见 4.4 Q1/Q5） |
| `capability_candidates`（默认首选技能） | `default_skill` | text | → `skill_templates.skill_template_id`（可选快捷绑定） |
| `capability_candidates`（默认首选工具） | `default_tool` | text | → `tool_templates.tool_template_id`（可选快捷绑定） |
| `workflow.process_type` 偏好 | `default_workflow_step_types_json` | text(JSON) | 仅步骤类型标签，如 `["research","draft","review"]` |
| `conversion_disposition.employee_action == enhance_existing` | （不新建） | — | 标记为增强既有 official（如 tech_lead），非独立 et_* |
| `license`（attribution_required） | `source_attribution`＊ | text | ＊落 `workflow_contents.source_attribution` 或存档于 catalog；et_* 无此列，署名经 catalog/audit 保留 |
| — | `source` | CHECK 3态 | 解冻前草案记 `official`（待审候选） |
| — | `tenant_id` | text | `official` → `'platform'` |
| — | `version` / `status` / `updated_at` / `slug` / `created_at` / `enabled` | — | 默认值（`1.0.0` / `draft` / ts / slug / ts / 1） |

#### 4.3.2 → `persona_templates`（pt_*，独立可复用资产）

| CanonicalAgentSpec 字段 | 目标列 | 类型/约束 | 转换与说明 |
|---|------|------|------|
| `identity.slug` | `persona_id` | text PK | `pt_{slug}` |
| `identity.slug` | `slug` | text | 同 slug |
| `identity.name` + `persona.archetype` | `name` | text | persona 展示名 |
| `persona.archetype` | `archetype` | CHECK 6值 | 须映射到 6 枚举之一（映射表见 4.4 内附） |
| `persona.traits[]` | `traits_json` | text(JSON) | 数组 |
| `persona.communication_style` | `communication_style_json` | text(JSON) | 对象 |
| `persona.reporting_style` | `reporting_style_json` | text(JSON) | 对象 |
| `persona.decision_style` | `decision_style` | text | 4 枚举之一 |
| `persona.collaboration_style` | `collaboration_style_json` | text(JSON) | 对象 |
| `identity.emoji` / `identity.color` | `image_ref_json` | text(JSON) | **清洗后**：`{"avatar_emoji":"📊","identity_description":"...","theme_color":"#1E88E5"}`（见 Q5） |
| — | `version`/`status`/`source`/`tenant_id`/`enabled`/`created_at`/`updated_at` | — | 默认（`1.0.0`/`draft`/`official`/`platform`/1/ts/ts） |

> **persona archetype 映射启发**（agency vibe/style → 6 枚举）：`direct_executor`（工程师/执行型）、`analytical_advisor`（分析/研究型）、`supportive_coach`（客服/支持型）、`creative_explorer`（营销/设计型）、`risk_aware_guardian`（安全/合规型）、`balanced_facilitator`（PM/协调型）。

#### 4.3.3 → `skill_templates`（skl_*）与 `tool_templates`（tl_*）

区分原则（回答 Q4）：**`tl_*` = 具名外部产品/API/技术栈的原子能力或集成；`skl_*` = 方法论/手艺/流程型 know-how（常 model-only，可再绑定工具）**。

| 来源（capability_candidates） | 目标表 | 目标列 | 类型/约束 | 转换与说明 |
|---|------|------|------|------|
| `skill_candidates[].name_hint` | `skill_templates` | `skill_template_id` | text PK | `skl_{slug}`（规范化） |
| 同上 | | `slug` / `name` / `description` | text | name_hint + evidence 合成 |
| `skill_candidates[].suggested_skill_type` | | `skill_type` | text | 如 `analysis`/`creation`/`research` |
| `skill_candidates[].evidence` | | `instruction_excerpt` | text | 方法摘要 |
| — | | `default_capability_types_json` | text(JSON) | 默认 `["model"]`（skl 多为方法论） |
| `division` 业务职能 | | `category`（additive） | text | 如 `marketing`/`sales`/`finance` |
| `tool_candidates[].matched_tool_id`（命中） | `tool_templates`（复用） | `tool_template_id` | text PK | 直接复用既有 `tl_*`，不新建 |
| `tool_candidates[].name_hint`（未命中） | `tool_templates`（候选） | `tool_template_id` | text PK | `tl_{slug}` candidate，**status=candidate 不 seed active** |
| 同上 | | `tool_type` | text | 映射到 Curis `tool_type` 枚举（code_execution/file_io/api_integration/database/vector_search/data_processing/document/deployment/observability/secret 等） |
| 同上 | | `description` / `instruction_excerpt` | text | name_hint + evidence |
| — | 两者 | `source`/`tenant_id`/`status`/`version`/`created_at`/`updated_at` | — | `official`/`platform`/`draft`(候选) 或 `active`(命中复用)/`1.0.0`/ts |

> 富字段（适用部门/适用员工/需要权限/认证方式/安全等级/版本/来源）以 `official-tool-catalog-v1.md` 为单一真相源，本设计为编目元数据，不写入 DB 核心列（DB `tool_templates` 仅存核心列）。

#### 4.3.4 → `workflow_templates`（wt_*，schema 已就绪）

| CanonicalAgentSpec 字段 | 目标列 | 类型/约束 | 转换与说明 |
|---|------|------|------|
| `identity.name` + `workflow.process_type` | `name` / `description` | text | 工作流名 + 说明 |
| `workflow.process_type` | `process_type` | text | `sequential`（默认）/ `parallel` |
| `division.target_dt_type` | `department_type` | text | 默认 `software_rnd`，按 division 设（如 `business.general`） |
| `workflow.steps[]` | `steps_json` | text(JSON) | 数组，步骤形状：`{"step_order":1,"name":"...","owner_role":"<agent role>","instruction_excerpt":"...","expected_output":"..."}`（单 agent 源 owner_role 缺省=该 agent role） |
| `success_metrics[]` | （wt 步骤 `expected_output` / quality gate） | — | 无独立列，并入步骤验收或评审稿 |
| `runbooks.json` roster（多 agent） | `workflow_contents.owner_roles_json` + `step_templates_json` | text(JSON) | 组队名册 → 多 owner 工作流（见 4.4 Q3） |

> `wt_*.steps_json` 步骤形状为**本设计新增约定**（DB 仅定义 `steps_json text`），供映射层与未来运行时一致消费。

#### 4.3.5 → `department_templates`（dt_*，division 级 harvest）

| CanonicalAgentSpec 字段 | 目标列 | 类型/约束 | 转换与说明 |
|---|------|------|------|
| `division.label` | `name` | text | 部门模板名 |
| `division.target_dt_type` | `department_type` | text | → `department_types.type_key` |
| `division` 描述 | `description` | text | 部门说明 |
| 已转换的 `et_*.id` 列表 | `default_employee_templates_json` | text(JSON) | **反向**归集：该 division 下所有 agent 转换后的 et_* id |
| — | `default_workflow_template_id` | text | 可选，关联 4.3.4 的 wt_* |
| 下属员工能力类型聚合 | `default_capability_types_json` | text(JSON) | 由下属 et_* 派生（不冗余存储，详见 department-template-research Q3） |

---

### 4.4 五个前置问题的架构答复（基于真实 DDL 证据）

**Q1：`persona_overrides` / `image_ref_json` / `applicable_departments` 是否为 Phase-4 S1 additive？与现有字段如何合并？`persona_overrides` 是否独立于 `pt_*`？**

- `persona_overrides_json`：**是 additive 列，已落地**（database.py 行 1077，注释标明 "Phase-1 Gate E 员工注入扩展字段"）。它是**每员工专属的 persona delta 层**，与 `pt_*` **相互独立但可组合**：解析 persona = 深合并（`persona_templates[et_*.persona_ref]` + `et_*.persona_overrides_json`）。`pt_*` 是可复用基元，`persona_overrides_json` 是该员工对基元的覆盖（不改写基元），避免为微调而 fork 整个 persona。
- `image_ref_json`：**不在 `et_*` 上**（PM 草稿假设有误）。它位于 `persona_templates.image_ref_json`（additive，行 1080）。即头像/主题色**必须经 `et_*.persona_ref → persona_templates.image_ref_json` 落地**。若某员工不引用 persona，则无 et 级头像（符合"形象属人格层"的设计意图）。
- `applicable_departments`：**不存在该列**。员工仅有单值 `department_type`（→ `department_types.type_key`）；"适用于哪些部门"是**反向关系**，由 `department_templates.default_employee_templates_json` 承载。因此 agency 的 `services` 绑定提示只能分解为：① 单 `department_type` 标签；② 候选工具绑定（`tl_*` candidate）。无正向多部门列。
- **合并方式**：现有 base 列（16 列：含 `id/name/role/responsibility/description/department_type/default_instructions/default_capability_types_json/default_model_policy_json/default_workflow_step_types_json/guardrails_json/source/tenant_id/enabled/created_at`）+ additive（`slug/persona_ref/default_skill/default_tool/persona_overrides_json/version/status/updated_at`）。`image_ref_json` 不在此合并范围内（在 `pt_*`）。

**Q2：`pt_*`（Persona Template）独立成表，还是 `et_*` 内嵌 JSON？**

- **独立成表**（已落地 `persona_templates`，16 列）。Persona 是**可复用的一级资产**，被多个 `et_*` 经 `persona_ref` 共享引用（如多个营销 agent 共用 `pt_brand_guardian`）。agency 的 Identity/Style/Communication 正适合抽为可复用 persona。
- `et_*.persona_overrides_json` **仅承载 per-employee delta，不承载完整 persona 定义**。完整 persona 永不在 `et_*` 内嵌——保持"模板定义复用、员工仅存差异"的边界。

**Q3：`wt_*`（Workflow）schema 何时就绪？agency 的 Workflow Process / runbooks 当前只能沉淀设计稿？**

- **schema 已就绪**（与 PM 草稿"Phase-5+ 预留"的判断不同，实际 `workflow_templates` + `workflow_contents` 已于 Phase-6 运行时阶段落地）。agency 的 Workflow Process **现在即可映射到真实结构**：
  - 单 agent `Workflow Process` 步骤 → `wt_*.steps_json`，`owner_role` 缺省填该 agent 的 `role`（单 agent 无协作 owner）。
  - `strategy/runbooks.json` 组队名册 → `workflow_contents`（wl_* 折叠），`owner_roles_json` 承载多 agent 角色，`step_templates_json` 承载步骤。
- 当前仅缺**内容补全 + 人工评审**（如补全 `expected_output`、校验 owner_role 合法），无需等 schema。故本设计可直接产出 wt_* 映射稿，但仍是 candidate/设计稿（受 L2 红线冻结，不 seed）。

**Q4：`skl_*` catalog 现状（version/category）与 `tool_templates` 关系，harvest 时如何区分 `skl_*` 与 `tl_*`？**

- 真实两表共享形态：`{slug, name, description, default_capability_types_json, instruction_excerpt, source, tenant_id, status, version, created_at, updated_at}`，均 CHECK 三态、均有 `(tenant_id, slug)` 唯一约束。
- **关键差异**：`skill_templates` 默认 `default_capability_types_json=["model"]`、有 `skill_type` + additive `category`；`tool_templates` 默认 `["tool"]`、有 `tool_type`。即 **skl 是方法论（常 model-only，可再绑工具），tl 是具名原子能力/集成**。
- **harvest 区分启发式**：
  - 隐含能力是**具名外部产品/API/技术栈**（React、GitHub、HubSpot、WCAG）→ `tl_*`（或匹配既有 `tl_*`）；
  - 隐含能力是**方法/手艺/流程型 know-how**（trend-scan、content-draft、nudge-design）→ `skl_*`；
  - 不确定时优先匹配 Curis 115 工具库，命中即 `tl_*`，未命中且偏方法论则 `skl_*` candidate。

**Q5：`image_ref_json` 安全——emoji/color 来自外部，注入清洗策略？**

- 清洗在 `SourceAdapter.parse()` 的归一阶段执行，`image_ref_json` 仅存清洗后值。规则：
  - **emoji**：白名单 Unicode 区段（Emoticons `U+1F300`–`1FAFF`、Misc Symbols `U+2600`–`26FF`、Dingbats `U+2700`–`27BF`、Arrows `U+2190`–`21FF`、Geometric `U+25A0`–`25FF`）；按 grapheme cluster 计 **≤1**；剥离变体选择符(VS16)、零宽连接符(ZWJ)、RTL 覆盖符、控制字符、不可见字符；归一后 >2 code point 即拒收置空。
  - **color**：严格 `^#[0-9a-fA-F]{6}$`；拒绝具名色、rgb()/hsl()/url()/gradient、任何 CSS 表达式。
  - **通用防注入**：对所有字符串字段（name/description/instructions/persona 文本）统一剥离控制字符、零宽、BOM、RTL 覆盖（`U+202A`–`U+202E`），防 Unicode 滥用/隐藏字符。

---

## 章节 6：风险与治理

### 6.1 L2 Gate #4 红线边界清单（冻结 vs 允许）

> 红线原文：把外部 agent 真实转换为 Employee / Skill / Department / Workflow 属 L2 暂停四项 #4 冻结。

| 动作 | 是否在冻结内 | 说明 |
|------|------|------|
| 真实 seed `employee_templates` / `skill_templates` / `tool_templates` / `workflow_templates` / `department_templates` / `persona_templates`（外部 agent 来源） | ❌ **冻结** | 解冻前不执行任何写操作 |
| 经 `/api/platform/*` 或 `/api/tenant/*` 写通道落外部资产 | ❌ **冻结** | 须待 L2 红线解冻 + Admin 审批 |
| 接入凭证 / 建 marketplace / instantiation（员工实例创建/执行） | ❌ **冻结** | 全局禁止 |
| 模板触发任务路由 / prompt 注入 / 员工记忆 | ❌ **冻结** | ADR-0017 Instance/Runtime 仍锁定 |
| 编目元数据、做映射设计、产出 candidate 草案、schema 设计、安全审查设计 | ✅ **允许（本设计范畴）** | 仅 pre-gate 设计稿 |
| 读取并分析 `database.py` 真实表结构以对齐 schema | ✅ **允许** | 只读，不修改 |

### 6.2 candidate vs active 两态管理

- 所有未在 Curis 现有库（115 工具 / 52 技能 / 6 official 员工）**命中**的抽取结果，一律产出 **candidate 草案**：`tool_templates.status='candidate'`、`skill_templates` 仅登记不 seed active、`employee_templates` 标 `conversion_disposition.employee_action` 但 `status='draft'`。
- 命中既有 `tl_*` / `skl_*` / official 员工的，判定为**复用/增强**而非新建（如 agency `product-manager` ↔ `official.employee.product_manager` → enhance_existing）。
- 候选清单（章节 5 的 15 个 harvest）全部为 candidate，解冻后经 Admin 写通道 + 评审方可转 active。

### 6.3 安全审查三类风险（关卡⑦）

| 风险类 | 识别方式（security_scan 字段） | 处置 |
|------|------|------|
| 凭证持久化剥离 | `security_scan.credential_patterns` 命中 `api_key`/`secret`/`token`/`password` 模式 | 从 `default_instructions` 等字段剥离；模板**永不持久化凭证**；仅记录"该 agent 需 X 凭证"于 catalog 元数据 |
| prompt 注入 | `security_scan.prompt_injection_flags` 命中覆盖系统指令/外泄/越权指令 | 评审打回或清洗；禁止模板承载可触发注入的内容 |
| 越权表述降级 | `security_scan.overclaim_flags` 命中"执行任意代码"等 | 降级为受控 `skl_*`（受 capability 边界约束）或直接剔除；不可映射为不受限 `tl_*` |

### 6.4 外部 emoji / color Unicode 注入清洗

- 见 4.4 Q5。清洗在 `SourceAdapter.parse()` 归一阶段强制实施；`image_ref_json` 仅存白名单内值。

### 6.5 许可合规

- **MIT**（agency-agents）：可商用、可改造、可再分发；`attribution_required=true` → 在 catalog `source_attribution` / audit 保留原作者与 MIT 文本。
- **copyleft 过滤**：`license.copyleft=true`（GPL/AGPL 等）→ 直接拒绝 harvest（关卡①前置过滤）。
- **Apache-2.0**：允许，须保留 `NOTICE`；`attribution_required=true`。
- 所有 harvest 条目在 `CanonicalAgentSpec.license` 登记 SPDX，未确认许可的一律 candidate 且不 seed。

### 6.6 三态治理 + ADR-0017 禁止区

- 三态 `official` / `tenant_private` / `marketplace` 与现有 capability / template 体系完全一致；候选草案记 `official`（待审）。
- **ADR-0017 禁止区**：Template 元数据（et_*/skl_*/tl_*/wt_*/dt_*/pt_*）属**可解禁层**；Employee Instance 创建/激活、AIEmployee 执行（Runtime）**仍锁定**。本设计仅触及元数据层 schema 与映射，**不触碰 Instance/Runtime**。
- 不变式：模板不持久化凭证、不触发任务路由/prompt 注入、不扩展 `CAPABILITY_TYPE`、不复用 `official_models`/`tenant_private_capabilities` 表。

---

## 附：MVP 切片建议（假设 L2 红线未来解冻）

> 目标：给出 V1 最小可落地范围（首个切片），含源 / division / 资产类型与依赖顺序。全部假设红线已解冻、走 Admin 写通道。

### 切片选型原则

1. **保真度优先**：结构化源（② skill 仓库）损耗低，但首批 MVP 选 **① agency-agents 的商业职能 division**——因其正好补 Curis 最大缺口（营销/销售/支持/财务无官方员工），设计验证价值最高。
2. **资产类型梯度**：V1 先落「人格 + 员工 + 技能/工具候选」，工作流仅沉淀草稿，部门仅做 division→department 映射。
3. **candidate 优先**：MVP 输出以 candidate/草稿为主，active seed 仅限高置信命中。

### V1 首个切片范围

| 维度 | 选择 | 理由 |
|------|------|------|
| 源 | 仅 ① `agency-agents`（MIT，范式 1） | 体量大、互补性强；结构化源（② skill 仓库）作 V2 高保真批次 |
| division | `marketing` / `sales` / `support` / `finance` / `product`（商业职能缺口） | Curis 净新增，与现有 6 研发员工无冲突；`engineering`/`design` 部分已覆盖，后置 |
| 资产类型 | `et_*` + `pt_*` + `skl_*` candidate + `tl_*` candidate + `wt_*` 步骤草稿 + `dt_*` division 映射稿 | 人格与员工是核心；skl/tl 先候选；wt 仅草稿（schema 已就绪）；dt 仅映射设计 |

### 依赖与顺序（6 步流水线）

| 步骤 | 内容 | 产出 | 依赖 |
|------|------|------|------|
| T1 | `SourceAdapter` + `CanonicalAgentSpec` schema + emoji/color 清洗器（解析层基础设施） | 适配器框架 + 归一契约 | — |
| T2 | 候选 harvest 清单 → `CanonicalAgentSpec` 生成（解析 5 个 division 的 agent 文件） | 结构化 spec 集合 | T1 |
| T3 | `pt_*` persona 抽取 + `et_*.persona_ref` 关联 + `persona_overrides_json` | 人格层 + 引用 | T2 |
| T4 | `et_*` 字段填充稿（role/responsibility/default_instructions/guardrails/department_type/capability_types） | 员工模板草案 | T2, T3 |
| T5 | `skl_*`/`tl_*` candidate 抽取 + 安全审查（credential/prompt-injection/overclaim）+ 许可合规 | 技能/工具候选 + 安全标记 | T2 |
| T6 | `wt_*` 步骤草稿 + `dt_*` division 映射 + 汇总评审稿（candidate，待 gate） | 工作流/部门草案 + 总评审 | T4, T5 |

> 全部为 candidate/草稿；**真实 seed 仅在 L2 红线解冻后由 Admin 经 `/api/platform/*` 写通道执行**，并过章节 3 关卡⑦安全评审。

---

## 附录：约束遵守声明

- ✅ 本报告**仅含 schema / 接口签名 / docstring / 设计说明**，无任何实现逻辑代码。
- ✅ **未 seed、未修改** `backend/app/database.py` 或任何真实资产表（仅读取 DDL 以对齐 schema）。
- ✅ 未触碰 L2 暂停四项 #4 红线；所有映射/清单均为 **pre-gate 设计稿**。
- ✅ 未接入凭证、未建 marketplace、未 instantiation。
- ✅ 所有产出标注 **设计稿 / pre-gate / 不实现**。

*（架构师设计稿完。后续由主理人汇编入《Agent 拆解转换引擎 V1 规划报告》并做自判。）*
