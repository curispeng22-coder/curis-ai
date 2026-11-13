# CURIS-V1-PLATFORM-ACCOUNT-S3-20261008 — 平台链 S3：人工发布回执回填 + 人工表现观察

- **Status**: Accepted
- **Authority Class**: REVIEW / IMPLEMENTATION（执行前为 Issue；验收证据见 §6）
- **Owner**: Main Development（实施）/ CEO（接受）
- **Date**: 2026-10-08
- **Backlog**: 平台链 P3 切片 S3（S1、S2 均已 Accepted 2026-10-08）；依据 [平台/账号本地链合同](../docs/01_Product/CURIS_PLATFORM_ACCOUNT_LOCAL_CHAIN_CONTRACT.md)（Frozen）§1/§3/§4.3/§4.4/§6；范式=Writing/Music Observation 时点记录
- **Next Gate**: 已闭合（Owner 已接受；平台链 v1 S1–S3 全部 Accepted，S4 挂 v1.1 D5）

## 1. Background 与设计裁定

合同 §4.3「人工回执回填」：对某账号某次核验记录，人工回填 `published_at / platform_post_url / note`（全部可选）；三强制真值（§1.2）；URL 展示固定标注「人工回填 · 未验证」。合同 §4.4「人工表现观察」：仿 Music Observation：`title / body / scope_ref（须命中本业务 ChannelAccount，否则 404） / period`；时点不可变、强制 UNVERIFIED、外部数据位恒「未连接」；分析/比较仅基于人工观察，样本不足不下结论（V2 §1.5 纪律仅 UI 提示，不强制）。§1.3：人工回填永不升级为平台事实。

### 1.1 对象 A：PublishReceipt（人工发布回执，objectType=`PublishReceipt`）

- 挂载：回执从属于一条本业务可见的 PublishVerification（路径参数 verification_ref）；核验必须经 `_verify_row` business 闸门，否则 404。
- 入参 exact：`{published_at, platform_post_url, note}`（verification_ref 从路径取，不进 body；伪造 verification/source/connection_status/revision 等任意额外键一律 422）。
- 三字段合同允许全可选，但工程裁定 **trim 后至少一个非空**，否则 422（空回执无证据意义；不违反「可选」——任一字段均可单独提交）。
- 校验：published_at 人工自由文本 ≤200（不强制 ISO 日期，对齐 Writing period 的 bounded 自由文本；空串允许）；platform_post_url 非空时必须以 `http://` 或 `https://` 开头且 ≤2000（防脚本/相对串；不做任何外联校验——零外发）；note ≤2000。
- 存储：runtime_entities 新行（PACKAGE_DOMAIN_OBJECT + UNVERIFIED/MISSING），零新表零迁移；ref `cg-receipt-<uuid4>`；data 含 verification_ref + 核验时点快照镜像（content_ref/content_title/account_ref/account_name/platform_ref/platform_name/business_ref）+ 三字段 + 强制 verification=UNVERIFIED/source=CEO_MANUAL/connection_status=NOT_CONNECTED + revision=1/identity_ref=自身/previous_ref=""。
- runtime_links：`CG_RECEIPT_VERIFICATION` → verification；event `cg.receipt.save`；幂等键 `cg:receipt:`+digest([scope,actor,request_id]) + 数据指纹；同指纹重放同 ref、异指纹 409（同 S2）。
- 无编辑、无删除、无状态推进；同一核验可多次回填（每次一条新时点实体）。
- 行写 workspace_id=当前工作区、company_id；business_ref 进 data 供业务级查询（同 S1/S2 可见性：同业务跨工作区互见）。
- 端点：GET `/verifications/{verification}/receipts`（列表）、POST 同路径（LearningIn 信封 request_id+data）、GET `/receipts/{receipt}`（业务级详情）。
- 展示纪律：列表与详情中 URL 一律紧邻固定文案「人工回填 · 未验证」；产品不做任何「已验证成功」推导，不回写 verification/content 任何字段。

### 1.2 对象 B：AccountObservation（人工表现观察，objectType=`AccountObservation`）

- 字段 exact `{title, body, scope_ref, period}`（对齐 Writing `_save_observation` 字段集）；额外键（含伪造 verification/source/connection_status/revision）一律 422。
- 校验（对齐 Writing 限额）：title 非空 ≤2000；body 非空 ≤20000；period bounded ≤200（非空要求对齐 Writing：观察周期必须可识别）；scope_ref 非空 ≤256 且必须命中本业务 ChannelAccount——经 `_account_row(con, company, business, scope_ref)`，不存在/非账号/跨业务 → 404。
- 与 Writing 版本链的差异（合同 §1.2 优先）：平台链**每次保存都是新实体**（revision=1、identity_ref=自身、无编辑链、无 expected_ref），不沿用 Writing 的 revision 链；幂等键 `cg:observation:`+digest([scope,actor,request_id]) + 指纹（同 S2）。
- 存储：runtime_entities 新行，零新表；ref `cg-obs-<uuid4>`；data 含 title/body/period/scope_ref + 账号快照（account_name/platform_ref/platform_name/business_ref）+ 强制 UNVERIFIED/CEO_MANUAL/NOT_CONNECTED + revision=1/identity=self/previous=""；runtime_links `CG_OBS_ACCOUNT`→account；event `cg.observation.save`。
- 端点：GET `/observations`（业务级列表）、POST `/observations`（LearningIn 信封）、GET `/observations/{observation}`。
- UI 纪律：恒显「人工观察 · 未验证」「未连接」；固定提示「分析仅基于人工观察；样本不足不下结论」（V2 §1.5，仅提示不强制）；不做自动分析/比较/聚合结论（无数字采集字段——title/body/period 全是人工文本）。

### 1.3 不做项（红线）

- 零外发：不请求 platform_post_url，不校验 URL 可达性，不抓取任何平台数据；不新增任何连接器/cookie/webhook/analytics 代码；legacy connectors/、content_publish_package.py、content_workflow_runtime.py 继续冻结。
- 不改 content 状态机、不改 INTERNAL_CANDIDATE_NO_PUBLICATION gate、不改 S1/S2 既有实体与端点语义；回执不回写核验记录（核验详情通过新端点实时带出回执列表）。
- 无自动「已发布」状态、无 VERIFIED 升级、无回执编辑/删除、无观察编辑/删除。
- ContentGrowth.module.css 零改动（复用既有类）；main.py / content_growth_entry_service.py 目标零改动。
- 仅 `--ui-*` token（本切片不新增任何样式）；每页最多一个 btn-primary（沿用既有 primary 类使用）。

## 2. Allowed Files

后端：
- `backend/app/content_growth_service.py`（新增 RECEIPT/OBSERVATION 常量、校验 helper 与方法族；在类尾追加，不改既有方法）
- `backend/app/api/content_growth_router.py`（新增 6 端点，复用 LearningIn/invoke）
- `backend/tests/test_cg_receipt_observation.py`（NEW）
- `backend/app/content_growth_entry_service.py`、`backend/app/main.py`：目标零改动（PREHASH 验证）

前端：
- `frontend/lib/contentGrowthState.mjs`（cg_view 白名单 +`observe`）
- `frontend/lib/contentGrowthApi.js`（receipts/observation 6 封装）
- `frontend/components/content-growth/ContentGrowthWorkspace.js`（context「表现观察」+ view 分支）
- `frontend/components/content-growth/ContentGrowthVerify.js`（详情模式内嵌回执列表+回填表单）
- `frontend/components/content-growth/ContentGrowthObserve.js`（NEW：list/create/detail）
- `frontend/tests/contentGrowthObserve.test.mjs`（NEW）
- `frontend/components/content-growth/ContentGrowth.module.css`：零改动（PREHASH 验证）

QA 产物（任务区，实施后创建）：`artifacts/tasks/CURIS-V1-PLATFORM-ACCOUNT-S3-20261008/qa/`（PREHASH.txt、qa_seed_s3.py、qa_server_s3.py、qa_probe_s3.py、run_qa_s3.sh、QA_REPORT.md、DEVELOPMENT_RETURN.md、运行日志）。

## 3. 验收标准

1. 后端新测全过；后端全量回归失败集与 S2 后基线（43 failed / 1904 passed / 8 skipped）IDENTICAL；前端新测全过、全量 9 既有失败不变；eslint 切片 0 error；`next build` 成功。
2. 探针必含：回执三强制与快照、字段校验（全空 422、URL 非 http(s) 422、超长 422、额外/伪造键 422）、核验越权/不存在 404、同 request_id 重放/异指纹 409、列表/详情业务可见+跨公司 404+同业务第二工作区可见、观察 scope_ref 非本业务账号 404、观察字段校验、两类对象零新表（无 receipt/observation 表）且落 runtime_entities、legacy 表零 S3 行、冷重启存活。
3. 零外发证据：forbidden-outbound.log 不生成；零 5xx；PREHASH=POSTHASH（8 文件口径，仅 Allowed 文件变更；main.py/entry_service/module.css 哈希不变）。
4. 浏览器 QA：核验详情回填回执（仅填 URL → 列表显 URL+「人工回填 · 未验证」；再补一条仅 note）；表现观察新视图（账号下拉均带「未连接」、选账号→填标题/正文/周期→保存→列表/详情显「人工观察 · 未验证」「未连接」与样本不足提示；scope 为他业务账号不可见）；页面无发送/排队/定时/已连接/实时数据字样；干净会话 console 零 error。
5. 登记：QA_REPORT.md、DEVELOPMENT_RETURN.md、本 Issue §6、CURRENT_STATE head、CHANGE_LOG tail（Status: Review 待接受；接受另轮登记）。

## 4. 风险与边界

- 合同「全部可选」与「至少一个非空」：工程裁定见 §1.1，Owner 可否决。
- 回执不回写核验：核验详情读时聚合 receipts，避免给不可变实体加可变附属字段。
- 观察无数字字段：合同 §4.4 只给 title/body/scope_ref/period；指标数字进 body 自由文本，服务端不解析，杜绝「平台数据」误读。

## 5. 输入来源

Frozen 合同 §1/§3/§4.3/§4.4/§5/§6/§7；S1 Issue/架构评审（runtime_entities 复用模式）；S2 Issue §1 与实现（幂等/快照/导出/标签服务端所有）；writing_operating_service._save_observation（字段限额范式）。

## 6. Execution Record

2026-10-08 实施完成并通过独立 QA（Status: Review，待 CEO/Owner 接受）。

### 6.1 变更源码（仅 §2 Allowed Files）

后端：
- `../../backend/app/content_growth_service.py` — RECEIPT/OBSERVATION 四常量 +
  notice 两常量 + `CG_RECEIPT_KIND`/`CG_OBS_KIND`；`_domain_row`/`_receipt_row`/
  `_observation_row` 行闸门；`_receipt_payload`/`_observation_payload` exact 校验；
  receipt/observation 各 collection/get/create（ref `cg-receipt-`/`cg-obs-`、
  幂等键+指纹、event、runtime_link、快照与三强制、revision=1/identity=self/
  previous=""）。
- `../../backend/app/api/content_growth_router.py` — 6 端点（receipts 列表/创建/
  详情、observations 列表/创建/详情）。
- `../../backend/tests/test_cg_receipt_observation.py`（NEW，12 测试）。
- `content_growth_entry_service.py`、`main.py`：零改动（PRE/POST 哈希实证，
  与 S2 相同）。

前端：
- `../../frontend/lib/contentGrowthState.mjs`（+observe）、
  `../../frontend/lib/contentGrowthApi.js`（6 封装）、
  `../../frontend/components/content-growth/ContentGrowthWorkspace.js`
  （「表现观察」入口+分支）、
  `../../frontend/components/content-growth/ContentGrowthVerify.js`
  （详情 Promise.all 聚合 receipts + 三字段回填表单 + 固定标注）、
  `../../frontend/components/content-growth/ContentGrowthObserve.js`
  （NEW：list/create/detail）、
  `../../frontend/tests/contentGrowthObserve.test.mjs`（NEW，3 测试）。
- `ContentGrowth.module.css`：零改动（哈希与 S1/S2 相同）。

### 6.2 证据

- QA 报告：`artifacts/tasks/CURIS-V1-PLATFORM-ACCOUNT-S3-20261008/qa/QA_REPORT.md`
- 开发回执：`artifacts/tasks/CURIS-V1-PLATFORM-ACCOUNT-S3-20261008/qa/DEVELOPMENT_RETURN.md`
- Harness：同目录 qa_seed_s3.py / qa_server_s3.py / qa_probe_s3.py /
  run_qa_s3.sh；PREHASH.txt / POSTHASH.txt（8 文件 IDENTICAL）；
  FAILSET_S3_IDS.txt / BACKEND_REGRESSION_TAIL.txt；requests.jsonl；
  screenshots/（5 张）。

### 6.3 验收结果（对应 §3）

1. **回归**：后端 12/12 新测；全量 43 failed / 1916 passed / 8 skipped，失败集
   裁剪后与 S1/S2 的 43 集 diff 为空（IDENTICAL，+12 新通过）。前端新测 3/3；
   全量 232/223/9（9 既有失败不变，+3 通过）；eslint 切片 0 error（1 条 S1
   既有 unused-disable warning 位移至 Workspace.js L55）；`next build` 成功。
2. **探针 94/94 PASS**：覆盖 §3.2 全部项（回执三强制+快照、全空/空白 422、
   javascript/ftp/无 scheme/伪 http URL 422、超长 422、4 类伪造键 422、核验
   不存在/跨公司 404、重放同 ref/异指纹 409、第二次回填为新实体、第二工作区
   可见且 provenance 保留、verification 不被回写；观察三字段空/超长 422、
   伪造 metrics 422、scope 不存在/content 冒充 404、幂等 409、跨公司 404、
   第二工作区可见、youtube 账号快照；无新表、legacy 表零行、两类对象落
   runtime_entities、两类 event 与 link、全表三强制零异常行、S2 面未回归）。
3. **零外发/哈希**：forbidden-outbound.log 全程不存在；全会话 526 请求
   （493×200/8×404/2×409/23×422）零 5xx；PREHASH=POSTHASH 字节级一致，
   entry_service/main.py/module.css 三哈希与 S2 完全一致。
4. **浏览器 QA PASS**：核验详情仅 URL 回执→「人工回填 · 未验证 未连接」+
  「系统不访问」纯文本；仅 note 第二/三条回执；观察视图账号下拉两项均带
  「（未连接）」→选账号+标题/周期/正文保存→列表/详情显「人工观察 · 未验证」
  「未连接」与样本不足 notice；两视图无发送/排队/定时/已连接/实时数据字样；
  干净会话 console 零 error、网络零 5xx。原生 select 在某轮 headless click
  失败系自动化工具限制（按 option value 选取成功），非产品缺陷。
5. **冷重启**：同库重启后回执 6/观察 3 均可读，强制真值与 revision 不变。
6. **登记**：QA_REPORT、DEVELOPMENT_RETURN、本 §6、CURRENT_STATE head、
   CHANGE_LOG tail 均已落盘（Status: Review）。

### 6.4 Verdict / Next Gate

Verdict: 工程实施完成、独立 QA PASS（REVIEW_REQUIRED）。
待 Owner 裁决项：§1.1「全部可选」工程解释（trim 后至少一项非空，否则 422）
可否决。Next Gate：CEO/Owner 接受；接受后平台链 v1 S1–S3 闭合，S4 挂 v1.1。

## 7. Owner Acceptance Record

- **Date**: 2026-10-08
- **Verdict**: ACCEPTED
- **Disposition**: SLICE ACCEPTED / CLOSED（同步登记 CURRENT_STATE head 与 CHANGE_LOG tail 为 Accepted）
- **Owner**: CEO（「好的，执行吧」2026-10-08，对 S3 独立 QA 结果与工程裁定作出接受）
- **工程裁定裁决**：§1.1「全部可选」解释为「trim 后至少一项非空，否则 422」——Owner 接受，不否决。
- **Next Action**: 平台链 v1 S1–S3 闭合；剩余 backlog 为 S4（平台角色记录 + Learning scope），挂 v1.1（D5）。
- **Target Authority**: 本 Issue + artifacts/tasks/CURIS-V1-PLATFORM-ACCOUNT-S3-20261008/qa/ 证据集（QA_REPORT / DEVELOPMENT_RETURN / 探针 94 项 / 截图 5 张 / PREHASH=POSTHASH / requests.jsonl）。
- **Next Gate**: 无（切片闭合；S4 启动需另立 Issue）。
