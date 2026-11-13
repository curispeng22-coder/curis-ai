# Issue — CURIS V1 Beta Stage A 分发基线

Status: Review
Authority Class: IMPLEMENTATION ISSUE
Disposition: APPROVED / READY_TO_EXECUTE（Owner 2026-10-06 盘点 §6 决策 5 授权）
Task ID: CURIS-V1-BETA-DISTRIBUTION-STAGE-A-20261006
Recorded: 2026-10-06
Owner: Main Development
Decision Owner: Curis V1 Delivery Owner
依据：artifacts/tasks/CURIS-V1-APP-COMPLETION-INVENTORY-20261006/V1_APP_COMPLETION_INVENTORY.md §5、§6、§7-P0；docs/reviews/CURIS_V1_DISTRIBUTION_STRATEGY.md（Stage A gate）

## 1. Objective

让当前 S5 已验证的 .app/DMG 具备「可交给外部试用者」的 Stage A 分发条件（不签名、不公证、零 Apple 费用）：

1. **Beta 发布文档包**（单一 Development 文档）：版本化 DMG+SHA256 公示与校验步骤；Sequoia 起 Gatekeeper 新流程安装指引（双击被拦→系统设置→隐私与安全性→Open Anyway；Control-click 捷径已取消须写明）；首次启动/数据默认位置；已知限制（未签名、Keychain 重授权、冷启动约 15s、updater 不支持）；备份/恢复用法；手动升级步骤（先备份→替换 .app）。
2. **curis-recovery fresh E2E 复验**：用已打包进 .app 的 recovery sidecar（desktop/runtime/recovery.py，已有 3 单测）在 fresh 默认位置 `~/Library/Application Support/com.curis.desktop` 跑 备份→损坏恢复/恢复到新位置→重启 App 数据可读 全链；S5 仅验二进制存在，未运行，本项补齐。
3. **版本化发布操作**：desktop/build-manual-dmg.sh 的硬编码 0.1.0/DMG 名参数化（版本变量+产物名含版本）；产出 release checklist（tag、SHA256 文件、release notes 模板、8/31 旧 DMG 勿发警示、SHA 以 S5_BUILD_EVIDENCE `0f31ff03…9aa026` 为 10/6 基线对照）。

## 2. Allowed Files / Directories

- desktop/build-manual-dmg.sh（编辑：版本参数化）
- docs/04_Development/CURIS_BETA_STAGE_A_DISTRIBUTION.md（**新建**，唯一发布文档）
- docs/00_Context/DOCUMENT_INVENTORY.md（仅追加索引行）
- docs/08_Change_Log/CHANGE_LOG.md（仅追加 2026-10 条目）
- artifacts/tasks/CURIS-V1-BETA-DISTRIBUTION-STAGE-A-20261006/**（任务区：prehash、E2E 证据、QA 报告、return）

**明确不授权**：desktop/runtime/recovery.py 源码改动（E2E 若发现缺陷→STOP 报缺陷另立）；签名/公证/updater 代码（Stage B）；任何 frontend/backend 业务代码；8+1 受保护 DB；Git 写操作；真发 GitHub Release（发布动作另需 Owner 明示）。

## 3. Acceptance Evidence（下一 Gate）

- 文档由非作者第三方视角可独立完成：下载→SHA 校验→安装过 Gatekeeper→首启→备份→升级恢复；含 Sequoia/Tahoe 实测截图或录屏路径引用。
- E2E 证据：fresh 临时默认位置演练（测试用 CURIS_DB/临时 HOME 或明确隔离手段，不污染真实 `~/Library/Application Support`），backup zip 产物清单（curis.sqlite 在内、Keychain 排除须明示）、restore 后启动+行数/内容抽检、sha 校验失败 fail-closed 记录。
- 参数化脚本演练：以显式版本变量产出命名正确的 DMG（可复用 10/6 .app，不要求重新全量构建时说明），checklist 完整。
- QA 结束清理进程/临时目录；任务回报含 changed paths、证据清单、skipped 项与原因。

## 4. Stop Conditions

recovery E2E 暴露数据损坏/无法恢复 → 立即停止并报告，不得改 recovery.py 绕过；文档与实际 Gatekeeper 行为不一致时以实测为准并标注系统版本。

## 5. Workload / 依赖

S+S+S ≈ 2–3 人日。无外部依赖；不阻塞其他 frontend 切片（无 frontend 文件重叠）。

## 6. Execution + QA complete · 2026-10-06 — ACCEPTED（Stage A 工程基线）

**Allowed Files 勘误**：实际脚本为 `desktop/scripts/build-manual-dmg.sh`（Issue §2 写的 `desktop/build-manual-dmg.sh` 为路径笔误；QA 裁定其为全仓唯一含 `hdiutil create` 的 DMG 脚本、package.json `build:dmg` 唯一调用处，改动仅 2 行版本参数化，授权效力不受影响）。

交付与证据（artifacts/tasks/CURIS-V1-BETA-DISTRIBUTION-STAGE-A-20261006/）：
- docs/04_Development/CURIS_BETA_STAGE_A_DISTRIBUTION.md 新建（10 节；QA 后补 4 处打磨：恢复片段自包含、--help 措辞改「用法整理」、437 MiB/458 MB 双口径、AirDrop 无 quarantine 分叉提示）。
- desktop/scripts/build-manual-dmg.sh：`VERSION` 环境变量参数化（默认 0.1.0，不传时产物名逐字不变；演练 Curis_0.1.0 / Curis_0.2.0-rc1 双版本名正确）。
- recovery fresh E2E：开发 20/20、**独立 QA 18/18**（包内 PyInstaller 入口；backup→zip 恰 2 条目无 Keychain→恢复全新根→行/user_version/integrity 一致；坏 zip/sha 掉包/多塞条目/运行锁 4 类 fail-closed 全拒且目标不动）；既有 3 单测过；recovery.py 源码零改动；真实默认库指纹前后一致零污染。
- 独立 QA Verdict **PASS**（14 大项、18+13+3 断言、6 项发布时 SKIP）；两 DMG SHA 复算一致、挂载确认仅 Curis.app 无快捷方式、ad-hoc/spctl 拒绝只读实证。

**Disposition：ACCEPTED — Stage A 工程基线（工程确认 2026-10-06）**。发布动作（tag、release notes、Sequoia 15/Tahoe 26 实机 Open Anyway 录屏、重建则重算公示 SHA、.sha256 附件、排除 8/31 旧包）仍需 Owner 发布时按文档 §9.2 checklist 执行，本接受不构成已发布。已知非阻断项：损坏到无法打开的归档 CLI 输出 BadZipFile traceback（安全性质成立，文案统一另立小修，登记 backlog）。Stage B（签名/公证/updater、US$99/年）不在本 Issue。
