# Curis V1 Beta Stage A 分发与安装指引（未签名 / 不公证）

Status: Review
Authority Class: IMPLEMENTATION
Task ID: CURIS-V1-BETA-DISTRIBUTION-STAGE-A-20261006
Date: 2026-10-06
依据：issues/CURIS-V1-BETA-DISTRIBUTION-STAGE-A-20261006.md；docs/reviews/CURIS_V1_DISTRIBUTION_STRATEGY.md（Stage A，Frozen）
适用读者：Beta 外部试用者、发布执行人、独立 QA

> 本文是 Stage A（GitHub Beta 分发：**不签名、不公证、零 Apple 费用**）唯一发布文档。
> 文中命令均已在 macOS 26.5（arm64）实跑或取自源码/构建证据；发布时才确定的值以
> **「待发布时填」**显式标注，不得以推测填充。签名/公证/自动更新属于 Stage B，本文不涉及。

---

## 0. 一句话流程

下载 DMG → 本地核对 SHA-256 → 拖拽安装到 `/Applications` → 双击被 Gatekeeper 拦截后到
**系统设置 → 隐私与安全性 → Open Anyway** 放行 → 首启（冷启动约 15 秒）。
升级前先用 `curis-recovery` 备份；本包**无自动更新**。

---

## 1. 当前发布基线（10/6 构建，已实证）

| 项 | 值 | 证据 |
| --- | --- | --- |
| 版本 | 0.1.0 | desktop/tauri.conf.json `version` |
| Bundle ID | `com.curis.desktop` | desktop/tauri.conf.json `identifier` |
| 架构 / 最低系统 | Apple Silicon（aarch64/arm64）/ macOS 12.0 起 | tauri.conf.json `bundle.macOS.minimumSystemVersion` |
| DMG 文件名 | `Curis_0.1.0_manual_aarch64.dmg` | desktop/scripts/build-manual-dmg.sh（已参数化，见 §9） |
| DMG 大小 | 216,737,419 B（约 207 MB） | 本地实测 |
| DMG SHA-256 | `0f31ff03763b6d8f108c0c5215ea04d7a2cd8c699face0f544bf6c75ef9aa026` | 2026-10-06 `shasum -a 256` 复算一致；S5_BUILD_EVIDENCE.md §4 |
| .app 大小 | 458,201,479 B（约 437 MiB；Finder 十进制口径约显示 458 MB，目录包） | S5_BUILD_EVIDENCE.md §4 |
| 签名状态 | ad-hoc、未公证（构建日志 `Code signing identity: None`） | S5_BUILD_EVIDENCE.md §3 |
| DMG 内容 | **仅 `Curis.app`**，没有 `/Applications` 快捷方式 | 10/6 只读挂载实测（安装需手动拖拽，见 §4） |

### 1.1 旧包警示：8/31 DMG 不得外发

本机另存在一个 **2026-08-31 的旧 DMG**，与当前基线无关，**严禁作为 Beta 包发布或转交试用者**：

- 文件名：`Curis_0.1.0-beta_arm64.dmg`
- 大小：228,147,450 B
- SHA-256：`726ff86e01bf963d95a39be4ba1a18963fa51528976e203adc97a840154c06fa`

发布时以文件名 + SHA-256 双重确认所传附件为 10/6 基线（或发布时新构建的版本化包，见 §9）。

---

## 2. 下载后核对 SHA-256（必做）

### 2.1 手动比对

在「终端」中进入 DMG 所在目录（通常是「下载」）：

```bash
cd ~/Downloads
shasum -a 256 Curis_0.1.0_manual_aarch64.dmg
```

把输出的十六进制串与发布页公示的 SHA-256 **逐字比对**（长度 64 位；可只比首尾若干段，
但建议全串比对）。当前 10/6 基线应为：

```
0f31ff03763b6d8f108c0c5215ea04d7a2cd8c699face0f544bf6c75ef9aa026
```

### 2.2 用随附 `.sha256` 文件一键校验（发布方提供校验文件时）

发布页同时上传 `Curis_0.1.0_manual_aarch64.dmg.sha256`（内容为
`<64位哈希><两个空格>Curis_0.1.0_manual_aarch64.dmg`），两文件放同一目录后：

```bash
cd ~/Downloads
shasum -a 256 -c Curis_0.1.0_manual_aarch64.dmg.sha256
# 期望输出：Curis_0.1.0_manual_aarch64.dmg: OK
```

该用法已在 macOS 26.5 实跑通过。若输出 `FAILED` 或哈希不一致，**立即停止安装**并联系发布方，
不要自行绕过。

---

## 3. Gatekeeper 与首次放行（macOS Sequoia 15 及更新系统）

本包为 ad-hoc 签名、未经 Apple 公证。通过浏览器下载、多数网盘与聊天工具传输的 App 会带 quarantine
标记，首次打开通常被 Gatekeeper 拦截，这是预期行为。
**全程不需要、也不应该关闭系统级 Gatekeeper 或降低全局安全设置。**

> 个别传输渠道（如 AirDrop、部分网盘同步盘）可能不附 quarantine 标记，双击直接打开、没有拦截弹窗
> 亦属正常——无需特意去找「Open Anyway」，直接进入首启即可。

### 3.1 推荐且受支持的放行路径（系统设置 → Open Anyway）

1. 按 §4 把 `Curis.app` 拖到 `/Applications`（不要直接在 DMG 卷里长期运行）。
2. 在「启动台」或「访达 → 应用程序」中双击 `Curis`。
3. 系统弹窗提示无法打开，含义类似「Apple 无法验证其是否包含恶意软件」，
   新版系统弹窗通常只有「完成/移到废纸篓」类按钮——**点「完成」（不要点移到废纸篓）**。
4. 打开 **系统设置（System Settings）→ 隐私与安全性（Privacy & Security）**。
5. 在页面下方找到关于 Curis 被阻止的提示，点 **「仍要打开（Open Anyway）」**；
   可能要求输入登录密码/Touch ID 确认。
6. 再次启动 Curis，弹出的对话框中会出现 **「打开（Open）」** 按钮，点击后进入首启。
   该放行只作用于 Curis 这一个 App。

> **旧捷径提示**：过去在 App 图标上 **Control-click（或右键）→「打开」** 可以直接得到
> 「打开」按钮。在 macOS Sequoia（15）及更新系统上，这条捷径对未公证 App **已不可靠**
> （常常仍只显示拦截弹窗）。请统一走 §3.1 的「系统设置 → 隐私与安全性 → Open Anyway」。

### 3.2 实测口径与待补证据

- 本文撰写机：macOS **26.5**（Build 25F71, arm64）。§3.1 流程依据 Apple 现行 Gatekeeper
  机制与 Stage A 策略（CURIS_V1_DISTRIBUTION_STRATEGY.md）编写；**Sequoia 15 / Tahoe 26
  的实机弹窗截图或录屏待 QA 在带 quarantine 的隔离环境补录**（路径占位：**待发布时填**）。
- 若文档描述与实机不一致，以实机为准，并在 release notes 标注系统版本与差异
  （Issue §4 Stop 条件）。
- 仅保留一份安装副本，建议固定使用 `/Applications/Curis.app`；不要同时运行
  「下载」目录、DMG 卷内或旧测试副本（同 Bundle ID 多副本会争用数据目录与单实例锁，
  来源：Stage A 策略文档）。

---

## 4. 安装（DMG 内无 /Applications 快捷方式）

10/6 基线 DMG 内**只有 `Curis.app`，没有 `/Applications` 文件夹或别名快捷方式**
（已只读挂载实测），因此：

1. 双击 DMG 挂载卷。
2. 手动把 `Curis.app` **拖拽到 `/Applications`（应用程序）文件夹**：
   可在 Finder 边栏打开「应用程序」，或用快捷键 `Cmd+Shift+G` 前往 `/Applications`。
3. 等待拷贝完成（约 458 MB），推出 DMG 卷。
4. 按 §3 首次放行后启动。

---

## 5. 首次启动与数据默认位置

### 5.1 默认数据根（以代码为准，非推测）

- 解析顺序（desktop/src/lib.rs `application_data()`，L35–48）：
  1. 环境变量 `CURIS_DESKTOP_DATA_ROOT`（为空则忽略；仅供高级/隔离测试使用，普通试用者无需设置）；
  2. 未设置时用 Tauri `app_data_dir()`，结合 Bundle ID 得到 macOS 默认路径。
- 默认数据根：

  ```
  ~/Library/Application Support/com.curis.desktop/
  ```

  首启时 App 会在其中创建：

  | 路径 | 内容 |
  | --- | --- |
  | `data/curis.sqlite` | 唯一业务数据库（SQLite） |
  | `logs/` | workspace/gateway/frontend 各 sidecar 的 `.log` / `.err.log` |
  | `curis-desktop.lock` | 单实例 + 恢复互斥锁（App 与 curis-recovery 共用） |

- 数据库相对路径 `data/curis.sqlite` 同时写入包内 `BUILD-MANIFEST.json`
  （S5 证据 §5），并由 lib.rs L132 以 `CURIS_DB` / `CURIS_WORKSPACE_DB` 注入后端 sidecar。

### 5.2 凭据存放：macOS Keychain（不在数据库、不在备份内）

- 打包后以后端环境变量 `CURIS_CREDENTIAL_BACKEND=macos-keychain` 运行（lib.rs L145）。
- 密钥类凭据通过 macOS Security.framework 存为 **generic password**，
  service 固定为 `com.curis.desktop.credentials.v1`
  （backend/app/credential_vault.py `MacOSKeychainCredentialBackend.SERVICE`）。
- 数据库只保存凭据元数据与摘要，**明文密钥不落 SQLite**。因此：
  - 换电脑、或恢复备份到新机器后，**密钥不随备份迁移，需要在 App 内重新填写/授权**；
  - ad-hoc 包重新构建/升级后代码身份可能变化，macOS 可能**再次弹出 Keychain 授权**，属预期。

### 5.3 启动体感

- 冷启动到窗口可用**约 15 秒量级**（本机 sidecar 冷启口径，实际随机器变化；属已知限制而非故障）。
- 启动后本机各服务只监听 `127.0.0.1`（workspace 8002 / gateway 8080 / frontend 3010，
  来源：BUILD-MANIFEST.json）。

---

## 6. 已知限制（Stage A）

1. **未签名、未公证**：首启与每次换成新的 ad-hoc 包都可能需要 §3 的 Open Anyway 放行。
2. **Keychain 不跨备份迁移、升级后可能重新授权**：见 §5.2。
3. **冷启动约 15 秒**；期间无进度窗口属正常。
4. **无自动更新，内置 updater 不支持**：tauri.conf.json `plugins` 为空、无更新通道；
   未公证下自动更新本身也会再次触发 Gatekeeper（盘点结论：updater 延至 Stage B）。
   所有升级一律走 §8 手动替换。
5. **仅 Apple Silicon（arm64）**；Intel Mac 不在本包支持范围。最低 macOS 12。
6. **单实例**：重复启动会提示「Curis 已经在运行」；恢复时同样受锁保护（§7.4）。
7. **备份只覆盖 SQLite**：见 §7.1，不含 Keychain、不含日志/其他文件。

---

## 7. 备份与恢复（curis-recovery）

### 7.1 工具位置与覆盖范围

发布包内自带命令行 sidecar（PyInstaller onefile，无需另装 Python）：

```
/Applications/Curis.app/Contents/Resources/runtime/recovery/curis-recovery
```

- 源码：desktop/runtime/recovery.py（**本次未改动**；包内二进制由 build-runtime.sh 打包）。
- CLI 用法整理（据 2026-10-06 包内二进制与源码入口实跑 `--help`；非逐字输出，真实顶层帮助为英文 argparse 原文）：

  ```
  usage: curis-recovery [-h] {backup,restore} ...
  Curis V1 release backup/restore utility (SQLite only; Keychain is excluded).

  backup/restore 共用参数：
    --data-root DATA_ROOT   Curis 数据根（默认即 ~/Library/Application Support/com.curis.desktop）
    --archive ARCHIVE       备份 zip 路径
  ```

- **覆盖范围**：备份 zip 内**恰好两个条目**——`manifest.json` 与 `data/curis.sqlite`
  （E2E 实测清单）。manifest 固定含 `"credentials": "EXCLUDED_MACOS_KEYCHAIN"`。
  **不含** Keychain 密钥、日志、配置或其他文件。
- 备份时先用 SQLite online backup API 做一致性快照，再做 `PRAGMA integrity_check`，
  并把快照的 SHA-256、`PRAGMA user_version`（当前 schema 版本）写入 manifest。

### 7.2 备份（先退出 Curis 更稳妥；工具不强制要求备份时退出）

```bash
RECOVERY="/Applications/Curis.app/Contents/Resources/runtime/recovery/curis-recovery"
DATA_ROOT="$HOME/Library/Application Support/com.curis.desktop"
"$RECOVERY" backup \
  --data-root "$DATA_ROOT" \
  --archive "$HOME/Desktop/curis-backup-0.1.0-$(date +%Y%m%d).zip"
```

成功时输出一行 JSON，例如（字段已实测；时间戳每次不同）：

```json
{"createdAt": "2026-10-06T07:55:20+00:00", "credentials": "EXCLUDED_MACOS_KEYCHAIN",
 "databaseEntry": "data/curis.sqlite",
 "databaseSha256": "a57dd728…37d38（示例：以实际输出为准）",
 "format": "curis.release-backup/v1", "schemaVersion": 7}
```

建议把 zip 再复制到与机器物理隔离的位置（网盘/外置盘），换电脑才用得上。

### 7.3 恢复（含「恢复到新位置 / 新 Mac」）

**恢复前必须完全退出 Curis**（菜单退出；锁由工具强制校验，见 §7.4）。

> 以下片段自包含，可直接整段粘贴；若你已按 §7.2 在本终端定义过 `RECOVERY`，重复定义亦无害。

- 原机恢复（覆盖当前库）：

  ```bash
  RECOVERY="/Applications/Curis.app/Contents/Resources/runtime/recovery/curis-recovery"
  "$RECOVERY" restore \
    --data-root "$HOME/Library/Application Support/com.curis.desktop" \
    --archive "$HOME/Desktop/curis-backup-0.1.0-XXXXXXXX.zip"
  ```

- **新 Mac / 新数据根**：`--data-root` 指向目标数据根即可；目录不存在时工具会自动创建
  `data/`。例如在新机器上恢复到默认位置（可在首次启动 App 之前执行）：

  ```bash
  RECOVERY="/Applications/Curis.app/Contents/Resources/runtime/recovery/curis-recovery"
  "$RECOVERY" restore \
    --data-root "$HOME/Library/Application Support/com.curis.desktop" \
    --archive "/Volumes/外置盘/curis-backup-0.1.0-XXXXXXXX.zip"
  ```

  随后再把 App 装到新机器并按 §3 放行首启；密钥需在 App 内重新填写（§5.2）。

恢复成功输出 JSON：`safetyCopy` 为 `null` 表示目标位置原先没有库；若目标已有旧库，
工具会先把旧库就地留档为同目录下的
`curis.sqlite.pre-restore-<UTC时间戳>`，再写入恢复数据（E2E 已实测）。

### 7.4 安全行为（fail-closed，已实测）

- 恢复时依次强制校验：zip 条目集合 = `{manifest.json, data/curis.sqlite}` →
  manifest 格式/版本 → 解压库 SHA-256 == manifest `databaseSha256` →
  `PRAGMA integrity_check` 为 ok → `user_version` 与 manifest 一致。任一不过：**拒绝恢复、
  非零退出、目标库保持不动、不残留 `restored.sqlite`**。
- App 正在运行（`curis-desktop.lock` 被持有）时恢复会被拒绝，报
  `Curis is running; close it before restore`。
- E2E 实测记录（20 项断言全 PASS）：
  artifacts/tasks/CURIS-V1-BETA-DISTRIBUTION-STAGE-A-20261006/e2e-logs/recovery-fresh-e2e.log
- 已登记的小瑕疵（**不影响 fail-closed 安全性**）：当 zip 损坏到无法作为归档打开时，
  当前版本会打印一段 Python `BadZipFile` traceback，而不是统一的
  `restore failed: …` 文案；退出码仍为 1、数据不动。建议后续另立小 issue 收敛错误提示，
  本切片按授权不修改 recovery.py。

---

## 8. 手动升级步骤（每个 Beta 版本通用）

1. **先备份**：按 §7.2 执行一次 backup，确认 JSON 正常输出，并把 zip 复制到安全位置。
2. **完全退出 Curis**（Cmd+Q；确认菜单栏无窗口、无后台进程）。
3. 取得新版本 DMG，按 §2 核对 SHA-256；确认不是 §1.1 的 8/31 旧包。
4. 挂载 DMG，把新 `Curis.app` 拖入 `/Applications`，Finder 提示替换时选择**替换**。
   （数据在 `~/Library/Application Support/com.curis.desktop`，与 .app 分离，替换不删数据。）
5. **首次打开新包同样走 §3 的 Open Anyway**（ad-hoc 身份变化后 Gatekeeper 会再次拦截；
   Keychain 也可能再次要求授权，属预期）。
6. 首启后抽查数据可读（公司/员工/近期内容在）。异常时的回滚：
   - 旧 .app 可从旧 DMG 重新拖回（建议升级前先把旧 .app 改名留档，如 `Curis-0.1.0.app`）；
   - 数据库若被新版改动需要回退，可用最近一次备份恢复（§7.3）；原地恢复产生的
     `curis.sqlite.pre-restore-*` 也可作为留档。

---

## 9. 版本化构建与发布 checklist（发布执行人）

### 9.1 构建脚本参数化（本次已交付）

`desktop/scripts/build-manual-dmg.sh` 支持 `VERSION` 环境变量，默认保持 `0.1.0`
（不传时产物名与旧行为完全一致）：

```bash
# 默认（等价历史行为）：
desktop/scripts/build-manual-dmg.sh
#   -> target/release/bundle/dmg/Curis_0.1.0_manual_aarch64.dmg

# 指定版本：
VERSION=0.2.0-rc1 desktop/scripts/build-manual-dmg.sh
#   -> target/release/bundle/dmg/Curis_0.2.0-rc1_manual_aarch64.dmg
```

脚本结束会自动打印 DMG 的 SHA-256。参数化已用隔离微型假 .app 实跑验证
（默认名不变、版本名正确、挂载内容正确、真实 10/6 DMG 未被触碰）；
未重新全量构建（耗时且非必要）。

### 9.2 发布 checklist 草案

- [ ] 确定发布版本号与 Git tag（tag 字符串：**待发布时填**；本切片禁止 Git 写操作，未代打）。
- [ ] 用显式 `VERSION=x.y.z` 构建（或复用已验收的 10/6 .app），记录 DMG 文件名/大小/SHA-256。
- [ ] 生成并随附 `<dmg名>.sha256` 校验文件（`shasum -a 256 <dmg> > <dmg>.sha256`），
      发布页同时公示人读 SHA-256。
- [ ] Release notes（模板：**待发布时填**，建议含：版本/构建日期、最低系统与架构、
      安装与 Open Anyway 步骤链接本文、相对上版改动摘要、已知限制 §6、
      升级前先备份的提示、实机 Gatekeeper 验证的系统版本）。
- [ ] **附件双确认不是 8/31 旧包** `Curis_0.1.0-beta_arm64.dmg`（SHA §1.1）。
- [ ] 安装说明写明：DMG 内**无 /Applications 快捷方式，需手动拖拽**（§4）。
- [ ] 在至少一台 Sequoia 15 与一台 Tahoe 26 实机走通
      下载→校验→拖拽→Open Anyway→首启→备份→恢复/升级，留存截图或录屏（**待发布时填**路径）。
- [ ] 发布后用全新账号/无写权限视角核对附件可下载、校验值一致。
- [ ] 本仓库 SHA 以 10/6 S5 基线 `0f31ff03…9aa026` 为对照起点；新构建必须重新计算并公示。

---

## 10. 证据索引

- 构建基线：artifacts/tasks/CURIS-V1-APP-VISUAL-INTERACTION-COMPLETION-20261005/development-return/S5_BUILD_EVIDENCE.md
- 本切片全部施工证据：artifacts/tasks/CURIS-V1-BETA-DISTRIBUTION-STAGE-A-20261006/
  （PREHASH/POSTHASH、E2E_SCRIPT.sh 与 e2e-logs/、脚本 dry-run、DEVELOPMENT_RETURN.md）
- 策略依据：docs/reviews/CURIS_V1_DISTRIBUTION_STRATEGY.md（Stage A / B gate，Frozen）
- 关键代码：desktop/runtime/recovery.py、desktop/src/lib.rs、desktop/tauri.conf.json、
  desktop/scripts/build-manual-dmg.sh、backend/app/credential_vault.py
