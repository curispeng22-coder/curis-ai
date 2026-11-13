# TALENT-MARKET-001：人才市场第一条招募与技能装配链

Status: Review  
日期：2026-08-14  
授权：用户 2026-08-14 明确授权人才市场专项开始产品设计和开发；本 Issue 将授权收敛为可审计的最小实现边界。

## 目标

在不修改 Curis 主产品架构、不新增 Admin/Workspace 系统的前提下，交付人才市场首版浏览体验，并打通：

```text
发现专家 → 查看详情 → 招募 → 员工化 → 组织中心可见
发现 Skill → 纳入公司资源 → 分配给员工 → 员工 Skill 可读
```

## 允许修改

- `docs/01_Product/Curis_Talent_Market_Resource_Audit.md`
- `docs/01_Product/Curis_Talent_Market_Product_Map.md`
- `docs/01_Product/Curis_Talent_Market_Integration_Contract.md`
- 本 Issue
- `backend/app/skill_runtime.py`
- `backend/app/main.py`（仅新增 Skill install 端点）
- `backend/tests/test_talent_market.py`
- `frontend/app/ceo-office/talent-market/page.js`
- `frontend/lib/talentMarket.js`
- `frontend/components/terra/TerraNavData.js`
- `frontend/app/ceo-office/talent-market/` 下为首版右侧检查器/招募装配所需的最小组件

## 本轮授权扩展

用户 2026-08-14 明确要求把专项从市场基础 UI 推进到真实资源链路。沿用本 Issue，不新建平行 Issue，增加以下最小文件范围：

- `backend/app/employee_templates.py`：保持 Department 可选的招募契约并复用现有 EmployeeInstance。
- `backend/app/agent_conversion/`：复用并扩展现有 CanonicalAgentSpec / AgencyMarkdownAdapter，实现公开候选与 OpenClaw/ClawHub 只读适配器；适配器不直接写库。
- `backend/tests/test_talent_market.py`、`backend/tests/test_*agent_conversion*.py`：为新适配器和真实绑定链增加最小回归。
- `frontend/app/ceo-office/organization/employees/[id]/page.js`、`frontend/lib/api.js`：展示真实 Skill/Tool Binding，并提供已有工作上下文的诚实入口状态。
- `frontend/lib/talentMarket.js`、`frontend/app/ceo-office/talent-market/page.js`：展示外部 Candidate 与 Curis-ready 的真实状态差异。

本扩展不授权修改 Master Map、唯一 Blueprint、Runtime 状态机、数据库 schema、Platform/Admin API 或制造外部执行/授权证据。没有真实凭据、原生授权或工作上下文时，必须保留 BLOCKED / Candidate 状态，不以 API 成功或静态 UI 代替完成。

## 复用

- 现有 `TerraShell`、`TerraPrimitives`、`TerraState`、`workspaceFetch`。
- 现有 EmployeeTemplate、Company/Department/Employee、SkillTemplate、SkillRuntime、Employee Skill Binding API。
- 现有 Capability/Connector registry 只读事实。

## 禁止修改

- 不修改 Master Map、主产品 Blueprint、Runtime 状态机、数据库 schema、Platform/Admin API、旧项目/任务链。
- 不引入 WorkBuddy/Coze 私有接口、闭源配置、抓取或逆向逻辑。
- 不新增“专家”组织表或第二套员工系统。
- 不制作虚构使用量、质量评分、连接健康或真实外部执行证据。

## 验证

- 后端最小测试：官方 Skill install 幂等、租户隔离、来源引用、员工 Skill 绑定安全边界。
- 前端最小测试/静态检查：市场 Tab、搜索、详情检查器、招募装配、Skill 安装与员工分配状态。
- 若当前环境允许，使用现有 Browser/Desktop 路径验证刷新/重启后的员工与 Skill binding；否则记录具体阻塞，不升级为 Desktop 完成。
