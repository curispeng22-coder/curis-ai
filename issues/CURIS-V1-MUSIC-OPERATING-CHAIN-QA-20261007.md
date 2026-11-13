# CURIS-V1-MUSIC-OPERATING-CHAIN-QA-20261007

Status: Review
Authority Class: IMPLEMENTATION SCOPE / QA
Disposition: REVIEW_REQUIRED
Owner: Curis V1 交付负责人
Executor: Main Development（独立 QA 执行体；本任务不改产品代码）

## 1. Objective

对已 BOUNDED ACCEPTED 的 Music 人工本地经营链（[CURIS-V1-MUSIC-OPERATING-CHAIN-001](CURIS-V1-MUSIC-OPERATING-CHAIN-001.md)，Owner 2026-10-06 接受）执行一次与 Writing P1-a/b/c 同标准的**独立完整 QA**：全新隔离 sqlite + 隔离包存储 + forbidden Provider 网关 + 真实 Chromium 走完整经营链 UI（Scope → Snapshot → Reference → confirmed Direction → Song → 歌词/制作保存 → 真实本地试听 → Choice → 独立 Master → 未发布准备包 → UNVERIFIED Observation → 固定 Report → 有限接受 Learning（UNVERIFIED）→ 显式历史采用下一 Direction → 下一 Song），并用 API/DB 探针核验版本 CAS、0≠Unknown、跨公司闸门、changed-basis 停止确认、旧 Report 不被改写、同意图幂等/不同意图第二首、冷重启恢复、零 Task/Usage/外发、受保护 DB 零漂移。

本任务是 QA-ONLY：**不修改任何 backend/frontend/包/产品文档源码**；PREHASH=POSTHASH 对全部 Music owned 源码逐文件 identical 是硬验收。不重新解释或扩大 2026-10-06 Owner 接受边界；真实 Provider/发行/收益/native/full Music 依旧 NOT_RUN。

合同/依据：[OPERATING_CONTRACT.md](../artifacts/tasks/CURIS-V1-MUSIC-OPERATING-CHAIN-001/OPERATING_CONTRACT.md)（Review，Owner approved）、Music Frozen §6/8（经原 Issue 引用）、[原 HANDOFF](../artifacts/tasks/CURIS-V1-MUSIC-OPERATING-CHAIN-001/HANDOFF.md)。

## 2. Allowed Files / Directories

- `artifacts/tasks/CURIS-V1-MUSIC-OPERATING-CHAIN-QA-20261007/**`（Issue、PREHASH/POSTHASH、qa/ 全部工件：seed/server/harness/probe、证据 json、截图、指纹、QA_REPORT、RETURN）
- 本 Issue 文件
- 登记文件（追加顶部条目，不改动既有内容）：`docs/00_Context/CURRENT_STATE.md`、`docs/08_Change_Log/CHANGE_LOG.md`
- 隔离临时区（仅 QA 期间）：`/tmp/music-q1-iso/**`（sqlite + 隔离包存储；结束删除）
- 只读使用既有授权媒体 root：`/private/tmp/curis-music-operating-chain-20261005-01/store`（demo-a/demo-b.wav；只读与 content-addressed staging 是媒体服务既有行为，QA 结束不清该 root）

禁止：任何 backend/app、backend/tests、frontend、bundled_workspace_packages、产品/合同文档、Git、native、真实 Provider、真实发行动作、其它任务 artifacts。

## 3. Acceptance Evidence

1. PREHASH/POSTHASH：原 Music 21 owned 路径 + 5 测试相关文件哈希前后逐文件 identical（含 backend/app/runtime/music.py、music_service.py、music_entry_service.py、music_media_service.py、api/music_router.py、frontend/components/music/*、frontend/lib/music*、bundled music 0.2/0.1 包与 manifest）。
2. pytest 隔离回归：test_music_operating_chain.py、test_music_canonical_entry.py、test_music_selected_execution.py 全绿（单文件口径），记录既有跨文件顺序基线。
3. 前端：musicOperatingChain.test.mjs、musicEntryReadiness.test.mjs 全绿；切片 eslint 0；`npm run build` 成功。
4. 真实 Chromium（headless，production dev API）走完整链，场景断言全 true：七经营面空态/真值标签（人工、未联网核验、UNVERIFIED、未发布、发布按钮 disabled）、歌曲目录、新建歌曲、歌词/制作版本、接入本地试听 A（真实音频字节 + 解码时长一致 + 播放时钟前进）、选择候选、双勾选确认 Master、建立本地准备包、保存原观察（已知 0 与留空 Unknown 两种）、创建并确认报告、接受经验效果待验证、changed-basis 后确认停止且旧报告只读、历史采用产生下一方向（原文含反例与待验证）、下一首固定原方向/经验、fail-closed 入口、零 console/page/http 错误（404/409/422 等探针预期响应单列不计错误）。
5. API 探针：跨公司 404；非法周期/伪造 verification/foreign master/空 source 等 422/404/409；同 request_id+同输入重复创建同一首、新意图第二首；读端点零写入（实体计数）。
6. DB 探针：tasks=0、ai_usage_records=0（无 fixture 用量场景）、workspace_package_objects=0（经营对象走 runtime_entities）；事件计数与链一致；七类经营实体/链接存在；无 DDL/新表；forbidden-outbound.log 不存在。
7. 冷重启：kill 后端同库重启，七类对象/歌曲/Master/包/观察/报告/经验/下一方向/下一首全部恢复，计数一致。
8. 8 处受保护 DB（7 sqlite + com.curis.desktop）QA 前后 SHA diff 为空；QA 进程正常退出、端口 8025/3024 清空、/tmp/music-q1-iso 删除。
9. QA_REPORT.md 如实记录证据、截图（以 shots/ 实际文件数为准）、失败/边界与 NOT_RUN 清单。

## 4. Stop Conditions

- 任何 PREHASH≠POSTHASH 的源码漂移（非本任务授权）→ STOP 登记，不继续。
- 隔离环境无法安装 0.2 候选包或授权媒体样本缺失/哈希不符 → STOP 报告（不得改 music_media_service 常量、不得造样本）。
- 真实链出现与 Owner 已接受语义冲突（如 UNKNOWN 被补 0、报告被改写、未发布呈现为已发布）→ STOP 并登记 PRODUCT/SEMANTIC 冲突，不自行修代码。
- 需要真实 Provider、凭证、网络、native、发布授权 → 超出范围，STOP。

## 5. Workload / 依赖

M（完整链浏览器自动化 + 双探针 + 冷重启）。依赖：已交付 Music 0.2 实现（BOUNDED ACCEPTED）、授权媒体 root 与 demo 样本仍在、Playwright 本地 Chromium（复用 CG QA node_modules）。

## 6. Execution Record（2026-10-07，QA-ONLY）

Status: QA PASS（待 Owner 接受）。Changed Files 全部限于 §2 Allowed Files：`artifacts/tasks/CURIS-V1-MUSIC-OPERATING-CHAIN-QA-20261007/**`（PREHASH/POSTHASH、qa_seed.py、qa_server.py、qa_harness.cjs、qa_probe.py、qa_fingerprint.sh、harness_evidence.json、probe_summary.json、requests.jsonl、server-ownership.json、db-fingerprint-before/after.txt、shots/*.png 5、QA_REPORT.md、DEVELOPMENT_RETURN.md）与本登记（Issue、CURRENT_STATE、CHANGE_LOG 追加）；无任何 backend/frontend/包/产品文档改动——**PREHASH=POSTHASH 21/21 逐文件 identical**。

验收对照（Issue §3）：

1. PREHASH=POSTHASH：21 owned 文件 identical（`diff` 为空）。PASS
2. pytest：去 selfuse 三文件合跑 24/24；selfuse 下 3 失败为夹具/身份注入既有冲突，QA_REPORT §6 登记。PASS
3. 前端 node --test 15/15、eslint 0 error、`npm run build` 47 页成功（QA 运行形态为 standalone 生产构建，原因见 OBS-1）。PASS
4. 真实 Chromium：S0–S14 + A1–A9 共 42 断言全 true；console/page/http 错误 0（预期 404/409/422 单列）。PASS
5. API 闸门：跨公司 song 404、A 路径挂 B workspace 422（canonical Company lineage）、伪造 verification 422、非法周期 422、stale confirm 409、同意图幂等/新意图第二首、fail-closed 深链。PASS
6. DB 探针 28/28：tasks/ai_usage_records/workspace_package_objects=0；七类 1/1/1/2/3/2/1（Report rev1→2 同 identity）；歌曲 3 + 16 版本实体；41 链接零悬空；无 Music 私有表；forbidden-outbound.log 不存在。PASS
7. 冷重启 C1–C10：计数恢复、pending 空、音频 Range 206、旧报告 rows=2 且 report_current=false。PASS
8. 受保护指纹：7 sqlite + com.curis.desktop 共 15 文件 before/after diff 空；8025/3024 已停；/tmp/music-q1-* 已删；授权媒体 root 按授权保留。PASS
9. QA_REPORT.md：证据、5 截图、环境注意点、OBS-1、NOT_RUN 全部如实记录。PASS

OBS-1（请 Owner 处置，未改码）：`frontend/components/music/MusicWorkspace.js` 的 mounted ref 在 `next dev` React Strict Mode 下致经营表单 submit 成功后早退；仅开发模式，standalone 交付形态不受影响（QA 生产构建全绿）。
NOT_RUN：真实 Provider/发行/收益/native/full Music/多人多租户。
证据：[QA_REPORT.md](../artifacts/tasks/CURIS-V1-MUSIC-OPERATING-CHAIN-QA-20261007/qa/QA_REPORT.md)、[DEVELOPMENT_RETURN.md](../artifacts/tasks/CURIS-V1-MUSIC-OPERATING-CHAIN-QA-20261007/DEVELOPMENT_RETURN.md)。
