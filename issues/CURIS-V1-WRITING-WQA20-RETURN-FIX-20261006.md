# Issue — CURIS V1 Writing WQA-20 模型配置真实回程修复

Status: Accepted
Authority Class: IMPLEMENTATION ISSUE
Disposition: DONE / QA PASS（工程确认登记 ACCEPT，2026-10-06；依据 Owner 决策上报规则，QA 通过后的接受属工程判断直接推进）
Task ID: CURIS-V1-WRITING-WQA20-RETURN-FIX-20261006
Recorded: 2026-10-06
Owner: Main Development
Decision Owner: Curis V1 Delivery Owner
依据：盘点 §4 WQA-20 行；WQA-20 历史 FAIL 证据（Writing QA REPORT / WQA20-repro，任务区可回溯）

## 1. Objective

修复 WQA-20 未翻案 FAIL：Writing 章节内「配置模型」（frontend/components/writing/WritingChapterMain.js 约 L94）当前跳进示例态设置页、无返回原章节链路。要求：

1. 从章节触发模型配置后，完成/返回时回到**原章节、原上下文**（collection/chapter id、草稿内容、滚动位置语义明确）；
2. 落点必须是真实可用的模型配置面（不是示例态/演示态；若复用 ceo-office/settings 真实模型区则带 return 上下文参数与回跳控件）；
3. 优先复用已有跨公司回程基座（businessReturnApi 及其 BOUNDED QA 模式）；
4. 冷启动/刷新/深链接语义明确可验证；跨公司隔离不破坏。

**不在本切片**：模型配置后端逻辑、Writing 经营面（无合同，盘点决策 1 另走）、其他业务线、冷启动模型缓存清空 CAUSE UNKNOWN 的根因（如回程修复过程中定位到该根因，仅记录不扩权修）。

## 2. Allowed Files / Directories（开工前登记 SHA256）

- frontend/components/writing/WritingChapterMain.js
- frontend/components/writing/** 下与配置入口/回程直接相关文件（开工定位 exact 文件登记）
- frontend/app/ceo-office/settings/page.js（**仅在**需要接收 return 参数/回跳控件时的最小 hunk）
- frontend/lib/ 下 businessReturn/writing API 相关（开工定位 exact 文件）
- frontend/tests/ 下 writing 相关测试（exact 文件开工登记）
- artifacts/tasks/CURIS-V1-WRITING-WQA20-RETURN-FIX-20261006/**

**预设为纯前端切片**：任何 backend/app/** 改动需求→STOP 报告。不授权：其他业务组件、8+1 DB、Git。

## 3. Acceptance Evidence

- 真实浏览器 QA（隔离环境）：章节→配置模型（真实配置面）→回跳原章节；草稿文字保留；章节 id 正确；刷新后回程参数的行为符合设计（无残留脏路由）；A 公司写作空间不泄 B 公司。
- 回归：既有 writing 测试（含 SERIAL 本地发布包、chapter discussion）不弱化、全绿；新增回程 focused 测试。
- 构建/lint；`--ui-*` token，无硬编码 hex/`dark:` 变体。
- WQA-20 原 FAIL 场景逐条翻案记录（原证据 vs 新证据对照）；DB 指纹；结束清理。

## 4. Stop Conditions

真实模型配置面无法在不重构设置页的情况下承接回跳；或回程必须后端配合→STOP，给最小替代方案（如章节内联配置弹层）等 Owner 选。

## 5. Workload / 依赖

M ≈ 1–2 人日。frontend 串行 QA（排在 FOUR-FORM 或 Composer 后）。

## 6. Execution Record（2026-10-06，QA PASS 工程接受）

### 6.1 实际改动文件

**零改动。** 12 个目标文件开工 PREHASH（[PREHASH.txt](../artifacts/tasks/CURIS-V1-WRITING-WQA20-RETURN-FIX-20261006/PREHASH.txt)）与收尾 POSTHASH（[POSTHASH.txt](../artifacts/tasks/CURIS-V1-WRITING-WQA20-RETURN-FIX-20261006/POSTHASH.txt)）**IDENTICAL**。无越界、无回滚、无 schema/后端触碰。

### 6.2 执行形态说明

调查证实 Issue §1 指向的缺口已被既有修复闭合：入口为 [WritingChapterMain.js](../frontend/components/writing/WritingChapterMain.js) `writingRepairHref("/ceo-office/capabilities", …)` 落真实配置面；回程由 [ModelManagement.js](../frontend/components/v1/ModelManagement.js) 渲染并经服务端校验（validateBusinessReturn → validateWritingReturn，目标白名单在 [writingApi.js](../frontend/lib/writingApi.js) `writingReturnTarget`）。故本切片以「隔离真实浏览器逐场景复验 + 翻案对照」完成验收，产品代码仅在 QA 发现缺口时改动——QA 全绿，未触发改动。

### 6.3 验收证据（[QA_REPORT.md](../artifacts/tasks/CURIS-V1-WRITING-WQA20-RETURN-FIX-20261006/qa/QA_REPORT.md)）

- 独立真实浏览器 QA（Playwright + 隔离后端 8023/前端 3023/双 mock 网关/隔离 sqlite）：S1–S6 + S4a/b/c 共 **36/36 布尔断言全 PASS**、PAGE_ERRORS 0、15 截图。
- 覆盖：配置模型→真实配置面→回跳原章节原上下文（dirty/未发送/讨论展开保留）；刷新无参数漂移；五种伪造 return_to fail-closed；跨公司 API scope 闸门 404；B 默认公司回程经 instance.company_id 精确授权零泄漏；冷启动深链正文精确匹配；员工详情回程。
- 回归：后端 Writing pytest **63/63**、前端单测 **39/39**、build 成功；lint 4 errors 为既有 `no-html-link-for-pages` 基线（不在 Allowed Files、非本切片引入），登记不修。
- 8 受保护 DB 指纹 pre/post **diff 为空**；零真实云模型调用；零 Git 写；进程与 /tmp 已清理、端口复查全空。

### 6.4 WQA-20 原 FAIL 翻案对照

原 FAIL（[WQA20-repro.json](../artifacts/tasks/CURIS-V1-WRITING-PRODUCT-ENTRY-QA-001/WQA20-repro.json)）五断言全部翻案成立：①示例态 settings → 现为真实配置面（S1_real_config_surface）；②无回程 → 服务端校验回跳精确还原（S1_return_url_ok）；③上下文丢失 → dirty/消息/章节 id 全保留（S1 + S5）；④员工详情无回程 → S6 全绿；⑤selection/anchor 属讨论绑定链、Issue 未列范围，由既有单测覆盖（边界注明）。对照明细见 QA_REPORT §4。

### 6.5 工程判断记录（直接推进，事后告知）

1. S4c 观察项（B 默认公司直接深链 A 章节渲染 A 数据）定性**非缺陷**：符合 V1 身份模型（CEO 租户级、workspace 深链为精确对象地址、隔离闸门在 API scope 层）。若未来要求「当前公司 UI 态阻断深链」属产品语义变更，需另立决策。
2. lint 4 个既有 error 不修（零改动切片无触碰依据），留 lint 专项处置。
3. pytest 隔离跑法修正（仓库根 + PYTHONPATH + CURIS_DB 三变量），属环境问题非缺陷。
4. QA 产物按 [DEVELOPMENT_RETURN.md](../artifacts/tasks/CURIS-V1-WRITING-WQA20-RETURN-FIX-20261006/DEVELOPMENT_RETURN.md) Output Manifest 归档保留，无 PROMOTE/DELETE 项。
