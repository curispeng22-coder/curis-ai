# Agent 拆解转换引擎 V1 — 解析层（agency-agents 范式 1）

把 `agency-agents`（MIT，[msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents)）
的外部 Agent 归一为 Curis 统一中间表示 `CanonicalAgentSpec`，再映射为官方员工候选
（`et_*` / `pt_*` 草稿）+ 工具/技能候选（`skl_*` / `tl_*` candidate）+ 工作流草稿
（`wt_*`）+ 部门映射稿（`dt_*`）。

## 目录结构

```
agent_conversion/
├── __init__.py
├── canonical.py            # CanonicalAgentSpec 及其子 dataclass（统一中间表示）
├── adapter_base.py         # SourceAdapter ABC + SourceEntry / SourceMetadata
├── sanitize.py             # emoji / color 清洗 + Unicode 注入剥离
├── security_scan.py        # credential / prompt-injection / overclaim 三段正则
├── agency_adapter.py       # AgencyMarkdownAdapter（discover/fetch/parse/extract_capabilities）
├── seed.py                 # SeedMapper + PILOT_B_MANIFEST（§7.1 权威映射）+ 候选行构建
├── seed_pilot_b.py         # 独立 CLI：显式 seed / 回滚受控试点 B
├── sources/                # 离线副本（运行期零外网）
│   ├── product/      (3)   # product-feedback-synthesizer / -trend-researcher / -behavioral-nudge-engine
│   ├── marketing/    (3)   # marketing-growth-hacker / -content-creator / -social-media-strategist
│   ├── sales/        (2)   # sales-pipeline-analyst / -discovery-coach
│   ├── support/      (2)   # support-support-responder / -legal-compliance-checker
│   └── finance/      (2)   # finance-financial-analyst / -tax-strategist
└── README.md
```

## 设计约束（红线）

- 所有资产 **candidate / draft 态、可回滚**；不接入凭证、不建 marketplace、不 instantiation（ADR-0017 仍锁 Instance/Runtime）。
- `et_*` / `pt_*` 用 `draft`；`skl_*` / `tl_*` candidate 用 `candidate`。
- 候选工具/技能 id 前缀 `pilot_b_`，保证与既有 115 工具 / 52 技能**零命名冲突**。
- 真实写入经 `database.py` 的 opt-in 函数 `seed_agent_conversion_pilot_b()`，**绝不挂默认 `initialize()`**。

## 数据源获取

`sources/` 下为离线副本（开发期抓取 / 整理，运行期只读）。真实仓库为
`agency-agents`，按 `divisions/<division>/<slug>.md` 组织；非 5-division 目录
（engineering/design/security/project-management 等）不入库。

## 运行

```bash
# 叠加写入 Pilot B 候选/草稿（先幂等 initialize 再叠加）
python -m app.agent_conversion.seed_pilot_b curis_pilot_b.sqlite

# 整批回滚
python -m app.agent_conversion.seed_pilot_b --rollback curis_pilot_b.sqlite
```

## 测试

```bash
python -m pytest backend/tests/test_pilot_b_agent_conversion.py -q
```

校验：12 `et_*` 字段符合 §7.1；与 6 官方 / 115 工具 / 52 技能零冲突；candidate/draft
可回滚；所有 `et` 有合法 `business.*` department_type；emoji/color 经清洗、无控制字符。
