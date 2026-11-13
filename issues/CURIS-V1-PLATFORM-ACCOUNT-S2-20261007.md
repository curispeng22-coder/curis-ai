# CURIS-V1-PLATFORM-ACCOUNT-S2-20261007 — 平台链 S2：发布核验清单（不发出）+ D4 新最小本地导出

- **Status**: Accepted（CEO/Owner 2026-10-08 接受，见 §7）
- **Authority Class**: ACCEPTED / IMPLEMENTATION TRUTH
- **Owner**: Main Development（实施）/ CEO（接受）
- **Date**: 2026-10-07（实施与 QA）/ 2026-10-08（Owner 接受）
- **Backlog**: 平台链 P3 切片 S2；依据 [平台/账号本地链合同](../docs/01_Product/CURIS_PLATFORM_ACCOUNT_LOCAL_CHAIN_CONTRACT.md)（Frozen）§3/§4.2/§6 与 D4；前置 S1（已 QA PASS；其 Owner 接受另行登记）
- **Next Gate**: S3（人工回执 + 人工表现观察）

## 1. Background 与 Design 裁定

S1 已交付平台目录与 ChannelAccount 本地 CRUD。S2 交付合同 §4.2：用户显式选择一篇**当前 workspace 既有 content** + 一个 **business 级账号**，按账号所属平台的生产链检查模板**逐项人工勾核**，生成**时点不可变核验记录**，并提供 **D4 新最小本地导出**（标题/正文/平台/账号/检查结果 JSON）。明确**无发送、无排队、无定时**；不改变 `INTERNAL_CANDIDATE_NO_PUBLICATION` gate，不写 content 状态机（合同 §3）。

### 1.1 存储裁定（工程判断，零新 schema → 按合同 §8 无需正式 Architecture Review）

- 沿用 S1 Architecture Review 已裁定的 runtime_entities 复用范式：新行 `entity_type='PACKAGE_DOMAIN_OBJECT'`、`data_json.objectType='PublishVerification'`、`verification_status='UNVERIFIED'`、`evidence_condition='MISSING'`。**零新表零迁移**。
- 行写 company_id；workspace_id = 创建工作区（溯源用）；业务归属写 `data_json.business_ref`，可见性查询与 S1 账号同构（`company_id + json_extract('$.business_ref')`）→ **核验记录 business 级可见**，同业务任一 CG workspace 可查看/导出。
- 跨级引用落法：content 是 workspace 级对象 → **创建时 content_ref 必须命中当前 workspace 的 CONTENT_ITEM**（复用 `ContentGrowthService.content(..., connection=con)`，越界即 404）；account 是 business 级 → 复用 S1 `_account_row` business 闸门。创建后记录 data 内存**时点快照**（content_ref / content_workspace_id / content_title / content_body / content_format；account_ref / account_name / platform_ref / platform_name），故跨 workspace 查看与导出不需要跨库读 content，且 content 事后改名/改正文**不改变**已存核验记录（时点不可变语义，同 learnings basis 快照）。

### 1.2 检查模板（服务端常量，客户端不可造）

- xhs：封面 / 标题关键词 / 标签话题 / 图文格式（key: cover / title_keywords / tags_topics / graphic_format）
- douyin：封面标题 / 时长字幕（cover_title / duration_subtitles）
- wechat_oa：排版 / 标题·摘要·封面（layout / title_summary_cover）
- tiktok / youtube / bilibili：**通用合规项**（合同仅给类目名，本切片的最小工程解释，Owner Review 可修正）= 版权与素材授权（copyright）/ 内容合规·无违法违规与敏感信息（compliance）/ 表述真实·数据与效果不夸大不伪造（honesty）。
- 严格按合同：三主平台仅专属项；其余三平台仅通用项。模板只读端点按 platform_ref 返回。
- 客户端只提交 `[{key, checked, note?}]`；**label 一律由服务端按模板合成**（客户端伪造 label 不被采纳）；提交键集合必须与模板全等（多/少/未知键 422）；每项 checked 必须是 bool（**允许 false——核验不通过也是核验结果**，产品不阻止记录未通过项）；note 可选，≤2000 字。

### 1.3 不可变与幂等（三强制，服务端强制）

- 记录固定带 `verification="UNVERIFIED"`、`source="CEO_MANUAL"`、`revision=1`、`identity_ref=自身`、`previous_ref=""`、`connection_status="NOT_CONNECTED"`；载荷 exact 仅 `{content_ref, account_ref, checks}`，客户端塞 verification/source/connection_status 一律 422（字段被拒），无法覆盖。
- 幂等沿用 learning_command：idempotency_key = `cg:verification:` + digest([scope, actor, request_id])；同 request_id 同指纹重放返回原结果，异指纹 409 ContentGrowthConflict。
- runtime_links 记 `CG_VERIFY_ACCOUNT` / `CG_VERIFY_CONTENT` 两条溯源链接。
- 无编辑、无删除、无状态推进；S3 的人工回执将是引用 verification_ref 的独立新对象（本切片不实现）。

### 1.4 导出（D4，新最小导出，不复用 legacy content_publish_package.py）

- 只读端点 `GET /verifications/{ref}/export` → JSON attachment（沿用 writing download 先例）：
  `{package_type:"curis.cg.local-verification-export/1", verification_ref, exported_at, title, body, format, platform:{ref,name}, account:{ref,name}, checks:[{key,label,checked,note}], connection_status:"NOT_CONNECTED", verification:"UNVERIFIED", source:"CEO_MANUAL", notice:"本地核验导出，不构成发布；平台连接不存在。"}`
- 头：`Content-Disposition: attachment; filename="cg-local-verification-<ref8>.json"`、`X-Content-SHA256`（导出字节 sha256）、`Cache-Control: no-store`。
- 导出是只读投影：不建实体、不写事件、不外发。`content_publish_package.py` / connectors/ / content_workflow_runtime.py 零触碰。

## 2. Allowed Files

后端：
- `backend/app/content_growth_service.py`（新增：VERIFY 模板常量（含通用合规三项）、`CG_VERIFY_KIND="PublishVerification"`、verification_template / verification_collection / verification / verification_create / verification_export + `_verify_row`/`_verify_template` helper）
- `backend/app/api/content_growth_router.py`（新增：GET `/verification-template/{platform_ref}`、GET/POST `/verifications`、GET `/verifications/{verification}`、GET `/verifications/{verification}/export`；`Response` 导入；同 invoke 错误映射；main.py 零改动目标）
- `backend/tests/test_cg_publish_verification.py`（NEW）

前端：
- `frontend/lib/contentGrowthApi.js`（template/verifications/verification/create/export(blob) 封装）
- `frontend/lib/contentGrowthState.mjs`（cg_view 白名单 +verify）
- `frontend/components/content-growth/ContentGrowthWorkspace.js`（context 入口 + view 分支）
- `frontend/components/content-growth/ContentGrowthVerify.js`（NEW：列表/新建/详情/导出；仅 --ui-* token 与既有类，CSS 零改动目标）
- `frontend/tests/contentGrowthVerify.test.mjs`（NEW）

文档/证据：本 Issue §6、`artifacts/tasks/CURIS-V1-PLATFORM-ACCOUNT-S2-20261007/qa/`、CURRENT_STATE head、CHANGE_LOG tail。

**Forbidden**：任何发送/排队/定时/重试控件或文案、connectors/、content_publish_package.py、content_workflow_runtime.py、workspace_package_objects、schema/建表、content 状态机与 INTERNAL_CANDIDATE gate 改动、legacy 页面、S3（回执/观察）、S4、product docs 修改、hex 色值、任何外发网络调用。

## 3. Acceptance Evidence

1. **新后端测试全绿**：六平台模板键恒定（xhs 4/douyin 2/wechat_oa 3/其余各 3 通用）；非法平台 422；创建/读取（快照全字段 + checks 服务端 label 合成 + UNVERIFIED/CEO_MANUAL/NOT_CONNECTED/revision=1/identity/previous=""）；checks 缺键/多键/未知键/checked 非 bool 422；note 超长 422；客户端伪造 verification/source/connection_status 被拒（422 或被服务端值覆盖）；content 越界/不属于当前 workspace 404；account 不属于本 business 404；幂等同指纹重放同 ref、异指纹 409；content 事后改名不影响已存快照；导出 JSON 形状（标题/正文/平台/账号/检查结果）与 X-Content-SHA256 正确；跨公司 404；同 business 第二 workspace 可见+可导出；employee 角色不可创建。
2. **全量回归**：失败集与当前基线（43 failed / 1893 passed / 8 skipped，S1 POST 基线）IDENTICAL。
3. **前端**：eslint 0 error；新测试全过；全量 9 既有失败不变零新增；生产 build 成功；ContentGrowth.module.css 零改动（哈希）。
4. **独立 QA**（隔离 sqlite + 真实浏览器 + forbidden 网关）：发布核验视图选内容+选账号→模板逐项勾核（含故意不勾项）→保存→列表通过数→详情→**导出文件真实下载且内容/sha256 正确**→无「发送/排队/定时」任何字样与控件；伪造/越权 4xx；零 5xx；零外发；无新表；PREHASH=POSTHASH（仅 Allowed Files）；冷重启记录存活且仍可导出；进程/端口//tmp 清理。
5. **登记五处**：QA_REPORT / DEVELOPMENT_RETURN / Issue §6 / CURRENT_STATE head / CHANGE_LOG tail。

## 4. Stop Conditions

- 需要建表/迁移或触碰 workspace_package_objects / content 状态机才能实现 → STOP 回报。
- 发现 content() 当前 workspace 校验无法复用、或导出需要服务端文件落盘 → STOP 定位。
- 现行三业务链/S1 出现回归 → STOP 优先恢复。
- 出现任何外发请求路径或「发送」语义 → 立即移除并回报。

## 5. Conventions

- 中文汇报；无 Git 写；后端测试 `CURIS_DB=CURIS_DB_PATH=CURIS_WORKSPACE_DB` 同隔离路径 + `PYTHONPATH=backend` + cwd=仓库根；前端 QA 后端 8000、浏览用 localhost:3000。
- 合同红线 §1 全量适用；QA 必含合同 §6 列项（三强制、伪造 422、越权 404、零 5xx、零外发、PREHASH=POSTHASH、诚实空态）。

## 6. Execution Record

**实施完成（Status: Review，待 Owner 接受）**。依据 §1 设计裁定全部落地，零新表零迁移、
零外发、main.py / entry_service / ContentGrowth.module.css 零改动（哈希验证）。

- 后端 [content_growth_service.py](../../backend/app/content_growth_service.py)：模块常量
  VERIFY_PLATFORM_CHECKS（xhs 封面/标题关键词/标签话题/图文格式；douyin 封面标题/时长字幕；
  wechat_oa 排版/标题·摘要·封面）、VERIFY_COMMON_CHECKS（copyright/compliance/honesty 供
  tiktok/youtube/bilibili，合同仅给类目名的最小工程解释，Owner Review 可修正）、
  VERIFY_CREATE_FIELDS 精确三字段、VERIFY_NOTICE；`CG_VERIFY_KIND="PublishVerification"`
  核验方法族——`_verify_template`（未知平台 422）、`_verify_check_results`（允许子集
  `{key,checked}` ⊆ 键 ⊆ `{key,checked,note,label}`；**客户端 label 容忍但丢弃**，标签一律
  服务端合成；键集合须与模板全等；checked 必须 bool，**false 显式允许**；note ≤2000）、
  `_verify_row`（business 闸门 404）、`verification_template/collection/verification/
  verification_create`（content 经既有 `self.content(..., connection=con)` 强制属当前
  workspace；data 内时点快照 content 五字段 + account 四字段；强制 UNVERIFIED/CEO_MANUAL/
  NOT_CONNECTED、revision=1/identity_ref=self/previous_ref=""；幂等键 `cg:verification:`+
  digest([scope,actor,request_id])，数据指纹 digest(payload data)，同指纹重放同 ref、异指纹
  409；ref `cg-verify-<uuid4>`；runtime_links CG_VERIFY_ACCOUNT/CG_VERIFY_CONTENT；事件
  `cg.verification.save`）、`verification_export`（只读投影：返回字节/sha256/文件名，不建实体
  不写事件不落盘不外发；JSON sort_keys indent=2，package_type
  `curis.cg.local-verification-export/1`，filename `cg-local-verification-<ref8>.json`）。
- 后端 [content_growth_router.py](../../backend/app/api/content_growth_router.py)：
  `Response` 导入 + 5 端点 GET `/verification-template/{platform_ref}`、GET/POST
  `/verifications`（POST 复用 LearningIn request_id+data 信封）、GET
  `/verifications/{verification}`、GET `/verifications/{verification}/export`
  （Content-Disposition attachment + X-Content-SHA256 + Cache-Control no-store，沿用
  writing download 先例）；同 invoke 错误映射。
  [main.py](../../backend/app/main.py) **零改动**（哈希验证）。
- 前端 [contentGrowthState.mjs](../../frontend/lib/contentGrowthState.mjs) 白名单 +verify；
  [contentGrowthApi.js](../../frontend/lib/contentGrowthApi.js) 5 封装（export 走 blob）；
  [ContentGrowthVerify.js](../../frontend/components/content-growth/ContentGrowthVerify.js)
  （NEW：list/create/detail 三模式，无编辑/删除/状态推进；选账号后拉模板，checkbox+备注，
  未勾项可保存并在详情显「未通过」；恒显「人工核对·未验证」「未连接」；副标题「不发送、不排队、
  不定时」；blob→createObjectURL→`<a download>`，卸载 revokeObjectURL；仅复用既有
  ContentGrowth.module.css 类——该 CSS 零改动）；
  [ContentGrowthWorkspace.js](../../frontend/components/content-growth/ContentGrowthWorkspace.js)
  context「发布核验」入口 + view 分支。
- 测试：[test_cg_publish_verification.py](../../backend/tests/test_cg_publish_verification.py)
  11/11（六平台模板键恒定/未知 422、快照全字段+三强制+行 UNVERIFIED/MISSING、伪造 truth 422、
  客户端 label 容忍但丢弃、缺/多/非 bool 422、content/account 缺失 404、幂等重放+异指纹 409、
  content 事后改名快照不变、导出形状+sha256、跨公司 404、同业务第二工作区可见可导出）；
  [contentGrowthVerify.test.mjs](../../frontend/tests/contentGrowthVerify.test.mjs) 3/3。

**回归与独立 QA**：

- 后端全量 43 failed / 1904 passed / 8 skipped（+11 新通过），失败集与 S1 基线
  （`artifacts/tasks/CURIS-V1-PLATFORM-ACCOUNT-S1-20261007/qa/FAILSET_S1_IDS.txt`，
  `sed 's/^FAILED //'` 裁前缀后）IDENTICAL（diff 为空）。
- 前端全量 229/220/9（9 既有失败不变，+3 新通过）；eslint 切片 0 error（1 warning 为 S1
  既有 unused-disable 随 import 位移至 Workspace.js L54）；`next build` 成功。
- 独立 QA（隔离 sqlite/store、8000/3000、forbidden 网关零外发、真实浏览器）：
  API 探针 **60/60**（六平台模板 19、三强制与快照 10、校验/越权/幂等 11、列表/详情/D4 导出/
  跨工作区/跨公司/存储 20；含 legacy content_publish_packages 零 S2 行、无 verif 新表、
  PublishVerification 行落 runtime_entities）；浏览器 **8/8**（列表 3 记录均「未连接」→
  新建选 QA 第一篇图文+QA 小红书号出 4 项→故意「图文格式」不勾并填备注→列表显
  「核对通过 3/4」→详情 3 已核对+1 未通过+「人工核对·未验证」「未连接」→「导出本地文件」
  出现「保存 JSON 文件」链接→YouTube 账号切换为 3 项通用合规；页面无任何发送/排队/定时
  可操作控件）；初次 console 报 dev chunk ERR_ABORTED/ERR_CONNECTION_REFUSED，经独立取证
  （旧 chunk 名在 127.0.0.1 与 localhost 下均 404、服务端 186×200 零 5xx、当前 HTML 全相对
  路径无 SW）+ 新标签 Disable cache 复验 **0 error 0 warning**，判定为浏览器 profile 旧 dev
  缓存/旧标签与扩展注入（/@vite/client），非 S2 缺陷；冷重启 4 条记录存活（含浏览器所建
  3/4 记录与备注），导出 200 且同响应 X-Content-SHA256 与 body 一致；全会话 196 请求
  186×200/4×404/1×409/5×422，零 5xx；forbidden-outbound.log 全程不存在。
- PREHASH=POSTHASH 8 文件 IDENTICAL：仅 5 个 Allowed 文件变更；entry_service/main.py/
  ContentGrowth.module.css 哈希不变（CSS 哈希与 S1 相同）。
- 清理：QA server 与 next dev 已 kill，端口 8000/3000 释放；本任务 /tmp 隔离文件已删。

**证据**：`artifacts/tasks/CURIS-V1-PLATFORM-ACCOUNT-S2-20261007/qa/` 下 QA_REPORT.md、
DEVELOPMENT_RETURN.md、PREHASH.txt / POSTHASH.txt、qa_probe_s2.py（60 检查）、
qa_seed_s2.py / qa_server_s2.py / run_qa_s2.sh、requests.jsonl、seed-summary.json、
server.log / server-restart.log、server-ownership.json。

**边界与不做项**（合同切片，非遗漏）：S3 人工回执（引用 verification_ref 的独立新对象，
UNVERIFIED/CEO_MANUAL/时点不可变）+ 人工表现观察（Music Observation 范式）、S4 平台角色+
Learning scope（v1.1，D5）；legacy connectors/、content_publish_package.py、
content_workflow_runtime.py 保持冻结未触碰（探针实证 legacy 表零 S2 行）；零外发零连接器；
content 状态机与 INTERNAL_CANDIDATE gate 未改。

**下一 Gate**：Owner Review；其后 backlog——S3（人工回执 + 人工表现观察）。

## 7. Owner Acceptance Record（2026-10-08）

- **Verdict**: ACCEPTED — 实施与独立 QA 均通过，§3 五项验收标准逐项有证据闭合，合同红线全部遵守。
- **Disposition**: SLICE ACCEPTED / CLOSED；产物以现状 PROMOTE 为正式 Implementation Truth（文件已在 canonical 路径，无需移动）；qa/ 证据保留为 EVIDENCE。
- **Owner**: CEO（2026-10-08 指令「帮我 Review 接受 S2」）；接受前由工程侧按 §3 完成证据复核（60/60 API 探针、浏览器 8/8、回归失败集 IDENTICAL、PREHASH=POSTHASH、零 5xx/零外发、冷重启存活）。
- **接受时一并确认的设计解释**：tiktok / youtube / bilibili 通用合规三项（版权与素材授权 copyright / 内容合规 compliance / 表述真实 honesty）为合同仅给类目名下的最小工程解释（§1.2 已声明 Owner Review 可修正），本次接受视为认可；后续若产品给出更细平台模板，按新 Frozen/Decision 走，不回改本切片。
- **遗留观察（非阻塞，非缺陷）**：浏览器 QA 中 dev chunk 的 console 报错已取证定性为旧 dev 缓存/旧标签与浏览器扩展注入（/@vite/client），Disable cache 干净会话 0 error；不登记缺陷、不立修复 Issue。
- **未完成项（合同切片，不在本接受范围）**：S3 人工回执（引用 verification_ref 的独立新对象，UNVERIFIED/CEO_MANUAL/时点不可变）+ 人工表现观察（Music Observation 范式）；S4 挂 v1.1（D5）。
- **Next Action**: 立 S3 Issue（范围研究 → Issue → 实施 → 独立 QA → 接受）。
- **Target Authority**: S3 Issue + 本合同 §6；CURRENT_STATE / CHANGE_LOG 同步本接受。
- **Next Gate**: S3 Owner 接受后，平台链 S1–S3 本地内容经营闭环全部闭合（S1 的 Owner 接受状态独立，不被本接受替代）。
