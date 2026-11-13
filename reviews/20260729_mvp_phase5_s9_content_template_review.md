# MVP Phase 5 / S9 — 内容创作模板 Review

结论：`PASS`

日期：2026-07-29

Issue：`issues/20260729_mvp_phase5_s9_content_template.md`

## 交付事实

- 复用 Wave-1 `ccp_ai_content_company` 的真实内容部门、员工和 Project，不增加全局模板种子或第二套 Workspace/Admin。
- 用户可从已绑定 Model Capability 的真实 Task 输入可追溯热点来源与摘要，生成选题、三平台文案/脚本、原生 SVG 图片和复盘计划。
- ContentWorkflowRun、ContentPublishPackage、Task、Execution 与模型 Token/成本真实持久化并关联。
- 模型结果非法时 ContentWorkflowRun 与 Task 明确失败，不回退 mock。
- 项目创建按所选部门自动使用其真实 Company，修复多公司下固定写入默认公司的归属错误。
- 外部发布未执行；未调用平台、未读取 Cookie、未伪造发布或表现数据。

## 验证证据

- 聚焦后端：`16 passed`。
- Frontend lint：`PASS`。
- Frontend build：`PASS`，26 个页面生成。
- 隔离干净提交候选全量后端回归：`1131 passed, 3 skipped, 0 failed`。
- 真实浏览器：Project `project-c6e418a5-0222-4d1f-971c-06ed8abb771b` → Task `04ac21c1-69f0-4a72-a0a2-3c9e333b72d2` → 内容工作流 → Task 详情完成。
- 浏览器持久化事实：模型 `browser-content`、Token `120`、成本 `$0.0080 USD`；小红书、抖音、头条文案和三张 SVG 均可见，复盘计划可见，外部发布明确未执行。
- Desktop `1440×1000`：`scrollWidth = clientWidth = 1425`，三张图片均完整加载。
- Mobile `390×844`：`scrollWidth = clientWidth = 375`，三张图片均为 `309×412` 且完整加载。

## 变更说明

- 扩展既有内容运行时，以人工选择模型生成并保存严格结构化 ContentPublishPackage。
- 新增 Project 内内容工作流抽屉和 Task 详情结构化成果展示。
- 项目中心读取全部 Company 的 Project；创建 Project 时从所选部门解析 Company 归属。

Handoff: sent to 产品规划席
