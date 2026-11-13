# 2026-07-22 macOS Keychain Google OIDC → Project Runtime Review

## 结论

`E2E_FAIL / TASK_EXECUTION_FAILED`。SHA `c86a9328a007b3e76ef570f6d689dcf6fcefda20` 修复后，既有 Google session 已真实完成固定 Project Runtime 加载、目标提交与运行启动，但新建 Task `task-124df2b7` 最终失败（退出码1、执行轮次0、无 trace/文件成果）。按最终用户验收标准，失败运行不算产品交付；只有同一任务实际成功且页面可见 trace/成果后才可回传 `USER_FLOW_PASS`。

## 真实执行证据

1. 安全静态 PASS 后，质量席重新通过 Finder 双击唯一启动器；Owner 重新隐藏输入既有 Google OAuth Client ID/Secret，未复用旧进程或输入，质量席未读取、记录或传递值。
2. 超过 10 秒后，进程仍停在 `expect` 及其 `security add-generic-password ... -w` 子进程；3001 关闭，`/api/auth/google/status` 仍为 401，说明 PTY 提示同步修复未完成真实 Keychain 写入。
3. 启动器未自行触发 timeout fail-closed；第二段 `expect eof` 后的 `wait` 仍可无限等待子进程。质量席为清除驻留内存中的旧输入，终止整组失败进程；未继续浏览器。
4. 清理后只读核验：固定 preauthorization 仍为 `pending`，`material_digest IS NULL`、`consumed_at IS NULL`，active Owner membership 为 0；Keychain 临时项及 `/tmp` override 均 `ABSENT`，无半绑定或历史改写。
5. 运行日志按敏感字段名扫描命中文件为 0；未读取任何 Secret 值。因未形成 `OWNER_BINDING_READY=true` / `LOCAL_GOOGLE_OIDC_SET_AND_MATCH=true`，不得继续 Google OIDC、一次 membership 绑定或 Project Runtime 项目操作。

### SHA 8b852850 最新重试

- 旧进程、Keychain 临时项与有效 override 均确认不存在后，从 Finder 全新双击启动器。
- 启动器立即报错：`mktemp: mkstemp failed on /tmp/curis-local-oidc.XXXXXX.yml: File exists`，Owner 未出现 Client ID/Secret 输入提示。
- 根因是 macOS `mktemp` 将带 `.yml` 后缀的 `XXXXXX` 模板作为字面路径处理；首次留下 `/tmp/curis-local-oidc.XXXXXX.yml`，后续执行直接冲突。该残留为 mode `0600`、size `0`，敏感字段命中 false。
- 失败后进程为 0、Keychain 临时项 `ABSENT`；preauthorization 仍 pending/digest NULL/consumed_at NULL，active Owner 为 0，无秘密输入、半绑定或历史改写。

### SHA 2e912394 最新重试

- Owner 从 Finder 全新双击启动器并隐藏输入既有 Client ID/Secret；Terminal 明确输出 `OWNER_BINDING_READY=true`、`LOCAL_GOOGLE_OIDC_SET_AND_MATCH=true`，随后打开固定 Project Runtime URL。
- 独立状态接口返回 `owner_binding_ready=true, authenticated=false`；3001/8080 均监听。Keychain 临时项与 `/tmp/curis-local-oidc*` 均 `ABSENT`，运行日志敏感字段文件命中 0。
- Google 真实浏览器到达 `accounts.google.com`，页面明确返回 `错误 400: redirect_uri_mismatch`。应用固定回调为 `http://127.0.0.1:8080/api/auth/google/callback`；当前 Google OAuth Client 的授权重定向 URI 未与其精确匹配。
- Google 回调未发生：preauthorization 仍 pending、digest 已设置、consumed_at NULL，active Owner membership 为 0；无半绑定、重复绑定或 Project Runtime 写入。

### SHA 0db39c2f 诊断复核

- 独立 focused：`backend/tests/test_local_google_oidc.py` → `10 passed`；py_compile 与 diff-check PASS。
- 四个首拒绝分支优先级正确：`provider_error → code_missing → state_missing → state_cookie_mismatch`；应用日志仅固定 `reason` 枚举，对外全部保持 `303 → ?error=login_failed`。
- 阻塞缺口：`deploy/curis/gateway/envoy.yaml.template` 的 access log 格式仍含 `%REQ(:PATH)%`，会记录 callback 完整查询串；Uvicorn 默认 access logger 同样调用 `get_path_with_query_string(self.scope)`。本次测试只检查 `curis.security.local_google_oidc` logger，未覆盖两层 access log。
- 当前容器日志只做计数、不读取内容：Gateway 有 9 条、Workspace 有 8 条 `/api/auth/google/callback?` 记录，证明真实 callback 查询串已经持久化。质量席未输出其中任何 error/code/state/cookie 值。
- 因敏感授权 code/state 可能进入容器日志，本诊断修复为 FAIL；不得以四分支 10 passed 允许 Owner 重试。

### 安全裁决与现存处置

- 状态固定为 `BLOCKED_L2`；计数 9/8 不能抵消泄露风险。
- 现存相关日志不得读取、复制、回显、导出、上传或写入 Issue/Review；本 Review 仅保留组件与计数，不含任何 query 原文。
- 系统交付席须立即停止 callback 链，隔离 gateway/workspace 日志工件，并按受控流程轮转销毁；仅保留计数、时间窗、组件、`redaction_status` 等非原文证据。若确认任何日志已外传，升级凭据泄露事件。
- 后续解除须同时证明：Envoy 不记录 `%REQ(:PATH)%` 或任何 query；Uvicorn/app access log 在进入日志前剥离 query；callback 成功/失败均不记录 code/state/nonce/Cookie/claims；现存敏感日志已清理。

### SHA 7d077838 静态质量复核

- Envoy formatter 已从 `%REQ(:PATH)%` 改为 `%REQ_WITHOUT_QUERY(:PATH)%`，静态扫描未保留旧 formatter。
- callback 入口在任何分支处理前将 `request.scope["query_string"]` 清空；Uvicorn access logger 后续读取的 path-with-query 因此只含无 query path。对外失败仍统一 `303 → ?error=login_failed`，固定四枚举与优先级未变。
- 独立 focused：`test_local_google_oidc.py`、`test_local_owner_launcher.py`、`test_local_project_runtime_target.py`、`test_workspace_identity_membership.py` → `25 passed`；py_compile、diff-check PASS。
- 交付席已在前一安全授权下停止链并随容器销毁 Gateway/Workspace 两个 json 日志工件；只保留 `artifact_count=2`、组件、时间窗、`ORIGINAL_NOT_READ_OR_EXPORTED` 与销毁 disposition。质量席未读取、复制或回显原文。
- 当前 Gateway/Workspace 容器不存在，3001/8080 均关闭；本轮未执行 runtime probe、Owner 登录或外网。
- 最终 PASS 尚缺：使用非敏感 probe 在真实 Gateway 与 Workspace access log 两层证明 callback query 均不保留；以及安全席所指“其余既存 access logs”完成受控处置。两项未完成前保持 `BLOCKED_L2`。

### 总控 B｜非敏感 runtime probe 尝试

- 总控与安全边界席批准一次普通 `start-local` 生命周期，仅启用 `CURIS_ENV=development` / `CURIS_LOCAL_GOOGLE_OIDC_ENABLED=1`，禁止 Owner、Google、Keychain、Secret、模型及外网。
- 启动前确认目标端口和 Gateway 容器均不存在；未注 Client ID/Secret/bootstrap。
- `start-local.sh` 在发送 callback probe 前 fail-closed：`Admin 启动失败: HTTP 000 listener_unavailable`。因此固定 `GET /api/auth/google/callback?...` 未发送，Gateway/Workspace 双层 query 证据未生成。
- 唯一 failure code：`PROBE_START_LOCAL_ADMIN_LISTENER_UNAVAILABLE`。
- 脚本清理后独立确认 3001/3100/8001/8002/8080 全部 CLOSED，Gateway/JWKS 容器与 probe 前端/后端进程均不存在；未读取任何 access log 正文。
- 不改用 compose 或其他旁路重试。整体继续 `BLOCKED_L2`，Owner 登录仍禁止。

### 总控 B｜三服务恢复路径

- 总控随后明确批准三服务直启，仅作为同一 B probe 的恢复路径：同一 local Compose override、现有镜像、仅 egress/workspace/gateway、无 Admin/前端/Owner/Google/Keychain/Key/模型/外网。
- 启动使用隔离空 DB；egress healthy、workspace started，但 Gateway 在固定 callback GET 前以 exit code 1 退出（started `2026-07-22T16:32:38.942339026Z`，finished `2026-07-22T16:32:39.108231598Z`）。
- 按禁重试立即停止；未发送 `?probe=curis-nonsensitive-probe`，未读取任何容器日志，因此仍未生成双层 query 脱敏证据。
- 唯一 failure code：`PROBE_GATEWAY_EXITED_BEFORE_GET`。
- `stop-local.sh` 后独立确认 3001/3100/8001/8002/8080 全 CLOSED，Gateway/JWKS 容器不存在，隔离 DB 目录与临时 override 均 ABSENT。
- 最终结论仍为 `STATIC_PASS / BLOCKED_L2`；Owner 登录继续禁止。

### SHA cc79be8f｜最终无登录 runtime probe

- 最小修复仅在 Envoy formatter 中注册 `envoy.formatter.req_without_query`；Compose validate、Envoy 1.31 `--mode validate` 均 PASS，query 剥离格式保持 `%REQ_WITHOUT_QUERY(:PATH)%`。
- 独立 local OIDC focused `11 passed`，py_compile、diff-check PASS；无其他服务或身份边界改动。
- 按总控批准的三服务路径，仅启动 egress/workspace/gateway、local OIDC override 与隔离空 DB；未注 Client ID/Secret/bootstrap/Cookie，未启动 Admin/前端，未触 Owner/Google/Keychain/模型/外网。
- 唯一请求：无 Cookie、禁 follow 的 `GET /api/auth/google/callback?probe=curis-nonsensitive-probe`；固定返回 `303 → http://127.0.0.1:3001/login?error=login_failed`，在任何 Google 出网前拒绝。
- 本次新容器日志仅计数、不输出正文：Gateway callback path=1/query=0/sentinel=0；Workspace callback path=1/query=0/sentinel=0；`CALLBACK_QUERY_REDACTED=true`。
- 立即执行 `stop-local.sh`；3001/3100/8001/8002/8080 全 CLOSED，Gateway/JWKS 容器、隔离 DB 目录及临时 override 全 ABSENT。
- probe 未写业务 DB。清理后只读现状为固定 preauthorization `consumed`、active Owner=1；这是 probe 前已存在的真实绑定事实，不由隔离 probe 创建。
- 结论：双层 query 脱敏 runtime Gate PASS；Owner 可点击 Google 登录，继续验证 Google → 8080 callback → 3001 固定项目页及真实项目操作。

### SHA 68fc5413｜既有 Owner bootstrap 轮换复核

- 改动仅涉及 `backend/app/local_google_oidc.py` 与对应 focused 测试；`reset_pending_bootstrap` 对 pending 仍要求 active Owner=0，对 consumed 仅在固定 tenant/company/ceo/project 目标完整且固定 issuer 下 active Owner 精确1条时允许清空临时 material；缺失、漂移或非唯一均 fail-closed。
- `inject` 使用同一固定映射和 Owner 计数约束；轮换不创建第二 preauthorization 或 membership，后续 `_consume_or_authorize` 仍只允许已绑定的同一 Google subject 重新授权，不同 subject 继续拒绝。
- 独立 focused：`backend/tests/test_local_google_oidc.py` → `13 passed`；py_compile、diff-check PASS。
- 只读现库证据：固定 preauthorization=`consumed`、`consumed_at` 已存在、active Owner 精确1条；本次复核未修改业务 DB、未启动服务、未读取 Secret/日志、未触 Google 或外网。
- 结论：`PREAUTHORIZATION_NOT_PENDING` 根因已闭合；允许一次全新 Finder 启动器与后续全新 Google 登录。整体 Issue 仍须以真实浏览器进入固定项目页并完成至少一项真实项目操作后才能最终 PASS。

### SHA 68fc5413｜全新浏览器 E2E

- Owner 全新执行 Finder 启动器并完成隐藏输入；质量席未读取终端、Keychain、Client ID 或 Secret。独立状态为 `owner_binding_ready=true`、3001/8080 OPEN；现库只读仍为 fixed preauthorization=`consumed`、material 已设置、active Owner=1。
- 浏览器从 `http://127.0.0.1:3001/login` 点击唯一“使用 Google 登录”，真实完成 Google → 8080 callback，并导航至固定项目 URL `http://127.0.0.1:3001/projects/local-project-b6f325cc-f347-4a74-a6d6-67528a3889b8`；未复用旧 code/state，未读取或回显 callback query。
- 项目页真实显示“项目读取失败 / Failed to fetch”，未形成项目数据、目标保存、运行启动或结果查看证据。
- 定向非敏感复核：页面 API helper 对所有请求固定发送 `Content-Type: application/json`，因此项目 GET 也触发 CORS 预检；对同一 `/api/pipeline/project/{fixed_project_id}` 的 `OPTIONS`（Origin=`http://127.0.0.1:3001`，method=GET，header=content-type）固定返回 401。
- Envoy 仅对带 `curis_local_session` Cookie 的 `/api/` route 禁用 JWT；浏览器标准 preflight 不携带该 Cookie，落入通用 JWT route 并在真实 GET 前被拒绝。后续 JSON POST 同样受此边界影响，故不能用仅消除 GET header 的局部调整宣称完整操作链已修复。
- 唯一 failure code：`PROJECT_API_PREFLIGHT_UNAUTHORIZED`。本轮不重放 Google 登录、不修改实现；失败页面已保留给交付复现。

### CORS preflight 安全裁决

- 安全结论：`PASS`，仅批准修复预检边界，不要求重放 Google 登录。
- 允许范围仅为 HTTP `OPTIONS`、精确当前 loopback Origin、既有最小 Allow-Methods/Allow-Headers；可由既有 CORSMiddleware处理或 Gateway 固定 204 空响应。Origin、Method 或 Header 不匹配继续拒绝。
- 预检不得要求 JWT、读取 Cookie、写 DB、创建 Run、改变状态或出外网；不得设置业务 Cookie或返回实体数据。
- `GET/POST/PUT/DELETE` 及其他业务请求继续经过既有 Envoy JWT、membership 与 TenantContext；禁止通配 Origin、任意 Origin、非 loopback、通用 OPTIONS 放行或业务鉴权旁路。query 脱敏边界保持不变。
- 后续质量验收须同时证明：合法预检固定成功且空体；不匹配预检拒绝；真实未授权业务请求仍拒绝；OPTIONS 无副作用。

### SHA ead13449｜CORS preflight 运行复核

- 静态范围符合安全闭集：仅精确 Origin `http://127.0.0.1:3001`；`/api/pipeline/*` 仅 OPTIONS + GET/POST + content-type，`/api/workspace/projects/*` 仅 OPTIONS + PATCH + content-type；规则位于 Cookie session route 前，真实业务 route 与 query 脱敏未改。
- 独立 focused `13 passed`、py_compile、diff-check、Compose config、Envoy 1.31 validate 均 PASS。
- 质量席仅重新生成 Gateway 配置并 `--no-deps --force-recreate gateway`；Gateway 容器 ID 已更新，Workspace 容器 ID 与前端 PID 均保持不变，Gateway `/health`=200，现有 Workspace session 未主动重置。
- 运行时合法预检仍失败：固定项目 GET preflight 返回 `401`、body 37 bytes，而非批准的 200/204 空响应。容器内配置 hash 与宿主生成配置一致，证明新规则已真实载入。
- 精确根因：Envoy route 已禁用 JWT并把 OPTIONS 代理到 Workspace；Workspace `_tenant_scope_middleware` 对 `/api/` 先执行身份授权，标准 preflight 无 Cookie/identity，因此在既有 CORSMiddleware 产生 CORS 响应前返回 `trusted_identity_missing`。当前代理式规则不能满足“预检不要求身份、固定 CORS 字段、空体”。
- 未授权真实 GET 仍为 401，未发生业务鉴权旁路；但合法预检硬条件不成立，未继续浏览器读写执行。
- 结论：`FAIL / PREFLIGHT_REJECTED_BY_WORKSPACE_IDENTITY`。系统交付须在已批准边界内改为 Gateway 固定 204 空响应及固定最小 CORS headers，或等价确保 CORSMiddleware 先于身份中间件处理；不得扩大 Origin/path/method/header。
- 安全后续裁决：既定 PASS 闭集保持但当前质量仍 FAIL。下一次仅允许 Gateway 在身份中间件前对精确 loopback Origin、OPTIONS、既定 path/method/header 返回固定 204 空体与固定 CORS headers；不得代理 Workspace、触发 TenantContext/DB/业务响应或放宽真实请求。修复后质量只复验合法 preflight 与未授权真实 GET 对照，不重放 Google 登录。

### SHA c86a9328｜最终浏览器 E2E

- 独立静态：focused `13 passed`、py_compile、diff-check、Compose config、Envoy 1.31 validate PASS。Gateway 精确匹配规则改为固定 204 空体及固定最小 CORS headers，不再代理 Workspace；真实业务 route 与 query 脱敏未改。
- 仅 `--no-deps --force-recreate gateway`：Gateway 容器已更新，Workspace 容器 ID 与前端 PID 保持不变，health=200，既有 Google session 未退出或重放。
- 对照结果：合法固定项目 GET preflight=`204`、body=0，Origin/Methods/Headers/Credentials 均为固定批准值；无 Cookie 的真实项目 GET 仍=`401`，未形成业务鉴权旁路。
- 浏览器复用既有 Google session 重新加载固定项目页成功，显示 `Project Runtime Local` 与真实项目/公司 ID，不再出现 `Failed to fetch`。
- 提交目标“通过 Project Runtime 提交目标并运行”成功，页面生成1节点计划并进入“待启动”；点击“启动运行”后显示“运行已启动”，随后刷新为最终“失败”状态。
- 真实运行对象：Task=`task-124df2b7`，Graph=`graph-03afad89ddf5`；结果为测试退出码1、执行轮次0、涉及文件未记录、暂无 trace。页面如实展示失败，没有伪造成功或进度。
- 结论：入口、项目读取、目标保存和启动动作已真实可操作，但任务执行失败，因此整体仍为 `E2E_FAIL`；唯一阻塞是同一 Task 尚未成功并产出可见 trace/成果。
- 安全最终确认：CORS 边界 PASS；合法 OPTIONS=204/body0/固定 headers，未授权真实 GET=401，Workspace/前端/session 保持且无 Google 重放。Task exit1 与 CORS 安全边界无关，不回滚或扩大安全范围。

### SHA 15f13188｜同一 Task 成功恢复候选

- 独立静态复核 PASS：`backend/tests/test_project_runtime_page.py` → 7 passed；前端 view-model → 3 passed；scoped ESLint、py_compile、diff-check PASS。
- 变更保持同一失败 Task/Graph 恢复语义，并限定固定 local/development 项目、tool capability 与仓内 focused pytest；未引入模型或 RealRD 路径。
- 当前运行 `gateway-workspace-1` 仍为修复前镜像 `sha256:9add903c...`（created `2026-07-23T00:50:52+08`），Compose 无宿主源码挂载，因此 15f13188 后端代码尚未加载，不能对同一 Task 执行有效 retry。
- 直接 rebuild/recreate Workspace 会清空内存中的 Google Client/Secret、session 与 bootstrap 状态；质量席不得读取、迁移或持久化 Secret，也不得违反“不退出/重登”约束。
- 当前结论：`STATIC_PASS / RUNTIME_NOT_LOADED`。唯一阻塞是缺少能够加载新 Workspace 代码且保留既有 OIDC session 的受控部署路径；总控须裁决保 session 部署，或明确批准一次全新 Owner bootstrap + Google 登录。裁决前未点击 retry。
- 安全意见：状态保持 `BLOCKED_L2`；禁止读取、迁移、持久化或隐式恢复 Client/Secret/session。若无法在不重建 Workspace 下加载代码，只能由总控明确批准一次全新 Owner bootstrap + 全新 Google 登录；旧 session/code/state 必须全部失效且不得复用。批准前不 retry、不注入、不登录、不出网。
- 总控最终选择 B：批准重建 Workspace 后执行一次全新 Owner bootstrap + 全新 Google 登录；旧 session、旧 code/state 与旧镜像全部作废且不得复用。重建必须保留原数据库中的 Task `task-124df2b7` / Graph `graph-03afad89ddf5`，不得创建第二实体；质量最终只复验该同一任务是否成功并显示 trace/成果。

### SHA 22bdfcf4｜范围冲突

- 交付回传声称创建新 Task `task-169503a4` / Graph `graph-1d3c4201e22d` 并扩展终态后“修改目标并创建下一次运行”；代码 diff 亦明确新增 next-run 产品能力。
- 该行为违反总控 B 的硬约束：质量只复验原 Task `task-124df2b7` / Graph `graph-03afad89ddf5`，不接受第二实体，也不扩大到下一次运行产品功能。
- 质量已立即终止尚未输入的 Owner bootstrap，`BOOTSTRAP_REMAINING=0`；未注入、未登录、未 retry。当前不采信交付 Chrome E2E 为最终证据，也不以新 Task 的成功替代原 Task 验收。
- 结论：`SCOPE_CONFLICT / SECOND_ENTITY_CREATED`。须由总控裁决 22bdfcf4 的超范围变更与第二实体处置；裁决前整体保持 `E2E_FAIL`，Owner 不再操作。
- 产品席正式事实核对：`22bdfcf4` 不能按旧 Issue 验收；旧 Issue 已改为 `PRODUCT_MISMATCH / PARTIAL`，唯一后续范围是 `issues/20260723_project_owner_workbench_product_flow.md`。新 Issue 明确要求聊天式目标与结构化任务双入口、统一结构化确认单，以及计划/进度/员工分工/成果/成本/风险/批准/返工/再运行；22bdfcf4 只覆盖终态目标编辑、下一次运行和结果解释，不能作为新 Issue 完成交付。
- 因此交付席“最新产品口径已覆盖旧限制、按22bdfcf4验收”的纠正不成立。22bdfcf4 可由产品/总控决定是否作为新 Issue 的部分实现复用，但质量当前不启动 Owner、不登录、不做浏览器验收。

## 既有离线证据

- 交付 focused：22 passed；bash syntax、py_compile、diff-check PASS。
- 上轮质量 focused：身份与 provisioning 影响集 17 passed。
- RealRD 保持暂停；本次未启模型、未读取 Key、未访问 Google 或其他外网。

## 唯一恢复动作

系统交付席以 Task `task-124df2b7` 的退出码1为唯一诊断输入；仅在同一任务实际成功并于页面显示 trace/成果后回质量最终复验。失败页已关闭，不再交 Owner 浏览或验收。

Next Seat: 产品规划席

Handoff: sent to 产品规划席
