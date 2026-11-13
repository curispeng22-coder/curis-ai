# TALENT-MARKET-002：人才库扩充、开源生态扫描与人才生产线

Status: Review  
日期：2026-08-14  
依据：用户 Phase 2 指令、ADR-0045、Master Map v2.0、Page Map v1.0、人才市场三份专项文档。

## 目标

在不创建第二套 Employee / Skill Runtime、不修改唯一 Blueprint 和主产品一级结构的前提下，
把现有公开资源 Adapter 组装为可重复运行的人才生产线：

```text
公开来源 → 发现 → License/Security Gate → 解析 → 去重 → 分类
→ 能力组合 → Candidate → 验证状态 → Curis-ready / BLOCKED
```

## 允许修改

- `backend/app/agent_conversion/`：生产线、公开来源目录、统一成熟度与去重输出；复用现有 Adapter。
- `backend/app/main.py`、`backend/app/database.py`：只读市场/生产线投影和员工模板能力组合字段，不新增主产品系统。
- `backend/tests/test_talent_market.py`、`backend/tests/test_*agent_conversion*.py`：生产线、门禁、去重和回归测试。
- `frontend/app/ceo-office/talent-market/page.js`、`frontend/lib/talentMarket.js`、`frontend/lib/api.js`：分类、成熟度、来源追溯和职业能力组合展示。
- `frontend/app/platform/page.js`、`frontend/app/platform/TalentProductionPanel.js`：复用现有平台 Admin，提供内部只读 Candidate Queue / 生产线观察面板，不进入普通用户一级导航。
- `docs/01_Product/Curis_Talent_Market_Resource_Audit.md`
- `docs/01_Product/Curis_Talent_Market_Product_Map.md`
- `docs/01_Product/Curis_Talent_Market_Integration_Contract.md`
- `docs/01_Product/Talent_Library_Expansion_Report.md`：本阶段内部工作报告。

## 不允许修改

- 不修改 `docs/01_Product/Curis_Product_Blueprint.html`、Master Map、Page Map、ADR-0045 或一级产品结构。
- 不复制 WorkBuddy / Coze 私有资源，不绕过权限、私有 API 或平台限制。
- 不导入无许可证资源，不把 Resource Candidate 直接变成 EmployeeTemplate。
- 不创建第二套 Skill Runtime、Employee 系统、Marketplace 服务或 Admin 一级导航。
- 不把扫描数量、接口 200、Mock、静态页面或未完成验证显示为 Curis-ready。

## 验收

- 生产线能扫描当前已登记的 Agency、Skill/OpenClaw、CrewAI、MCP 来源，并返回 discovered/candidate/composed/validated/curis_ready/blocked 成熟度。
- 每条资源有 source/repository/path/version-or-digest/license/security/duplicate identity。
- 市场按产品、研发、设计、内容、增长、研究、商业、数据分类；Curis-ready 与 Candidate 明确分开。
- 专家详情显示职业能力组合及其真实来源；Candidate 不可直接招募。
- 当前 5 个 Curis-ready 招募链路保持不回归；55 个 Skill 的安装/绑定保持不回归。
- 形成 Phase 2 内部报告，记录扫描来源、计数、许可证、安全、去重、Candidate、验证与下一步。
