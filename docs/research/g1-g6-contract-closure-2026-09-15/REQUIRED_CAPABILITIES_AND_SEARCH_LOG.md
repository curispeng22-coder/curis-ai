# G1–G6 Required Capability 与检索账本

Authority Class: RESEARCH
Status: Draft
Disposition: DEFINE FIRST — BEFORE EXTERNAL SEARCH
Date: 2026-09-15 Asia/Shanghai

上轮来源：full-app-completeness-2026-09-14的三份主文件、C01–C48与G1–G6。不修改V2或Authority，只交本轮closure及待修改清单。

|Gap|Required Capability|已有Curis证据|精准核查候选/停止条件|
|---|---|---|---|
|G1|Search/Reader/Interactive分离；DOM、截图、账号隔离、真人接管、localhost、Console/Network、上传下载、可观察员工API|C12–16/C21；历史tool catalog存在Playwright定义，不等集成；Shell preview非自动操作|Playwright、官方Playwright MCP、browser-use，最多三者深入；能决定底层与产品归属即停止|
|G2|连接实例、完整发现、来源化能力元数据、用途测试、合法路由/fallback、唯一Usage|C02–08；现有ModelGatewayAdapter/Profile/多能力绑定；历史LiteLLM仅备用，不采纳旧Admin-only/无Keychain事实|LiteLLM、models.dev元数据；OpenRouter只区分服务非完整OSS系统；不搜SDK大全|
|G3|关闭UI继续、可控退出/睡眠边界、持久工作、checkpoint、排程/触发、崩溃恢复|C25–27；现有Scheduler/WorkspaceRuntime与模拟路径不同；桌面close会kill sidecar|原生launchd+当前Runtime先；必要比较APScheduler、DBOS、Temporal（G4共用）|
|G4|幂等、效果未知、安全重试、审批快照、checkpoint、人介入、审计、恢复|C29/C38–40；既有Execution/Decision/Result与持久化；历史研究明确避免第二Runtime|复用G3候选，不另找Agent框架；判断底层引擎与Curis动作语义的边界|
|G5|Terminal/Git/Preview/解析OCR/Data/Media各自可调用、有限权限、真实结果|C17–24/C42；LocalRDToolset仅登记工具；backend只FastAPI/httpx/PyYAML等少量依赖|优先标准Shell/Git/现有HTTP与SQLite；Docling/Tesseract/FFmpeg最多三项深入，不找新AI Workspace|
|G6|一致备份包、完整性、恢复预检、稳定引用、凭证重连清单、恢复前核验Work|C43–48；desktop/runtime/recovery.py；备份接受仍pending|SQLite backup+Python标准库+macOS Keychain，明显足够则不增加restic/分布式系统候选|

检索纪律：仅下载公开源文件作为证据，不安装/运行项目，不clone整仓，不集成。每候选先README/API/License/Release/维护；仅入选者查目标源码。G3/G4证据共用，查询与原因随检索记录。历史结论有陈旧Admin-only/凭证占位段，只当历史，不覆盖最新Accepted Keychain/Runtime。

## 搜索结束登记

Status仍为Draft需求前置记录；最终判定以同目录Review主报告为准。

G1停止B/C；G2停止C；G3/G4停止B/C；G5停止A/C；G6停止A/C。没有第二轮扩仓。
直接地址核查：microsoft/playwright及playwright-mcp对应会话与桥接；browser-use对应Agent层耦合；BerriAI/litellm对应协议与fallback；anomalyco/models.dev对应来源化元数据；agronholm/apscheduler、dbos-inc/dbos-transact-py、temporalio/sdk-python对应三类调度/持久执行；Docling/Tesseract/FFmpeg对应三类工具底层。

相关Issue只采用LiteLLM #24512的“历史包安全报告”边界，不采用社区帖的扩大推断。搜索结果中的browser-use #3153、models.dev #3028未深查当前状态，因此不以它们作为选型事实或缺陷结论。
