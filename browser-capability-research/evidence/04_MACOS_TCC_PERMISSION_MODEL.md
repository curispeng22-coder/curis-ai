# Evidence 04 — macOS TCC 权限模型（决定 Browser 与 Computer Use 的成本差异）

Authority Class: EVIDENCE
Collected: 2026-09-18
Sources:
- OpenClaw Docs — `https://documentation.openclaw.ai/platforms/mac/permissions`
- 社区技术指南（Swift 权限申请）— `https://gist.github.com/Looking4OffSwitch/493e1f9fb9132f2826c4c377b3ce27fe/revisions`（Last Updated February 2026，Target macOS 11+）
- Nektony — `https://nektony.com/how-to/manage-app-permissions-mac`（macOS Tahoe 26 语境）

---

## 1. TCC 的绑定对象（原文要点）

OpenClaw 文档：
> "TCC associates a permission grant with the app's **code signature, bundle identifier, and on-disk path**. If any of those change, macOS treats the app as new and may drop or hide prompts."

稳定授权的四个必要条件：
1. 同一路径（发布版放 `/Applications`；开发版固定单一路径）
2. 同一 bundle identifier（发布/开发各自独立身份）
3. 已签名（unsigned / ad-hoc 签名**不持久**）
4. 签名一致（用真实 Apple Development 或 Developer ID 证书；ad-hoc 每次构建都生成新身份）

## 2. 关键权限分类与风险（Nektony）

| 权限 | 授予能力 | 滥用风险 |
|---|---|---|
| Full Disk Access | 读取磁盘全部文件（含 Mail/Messages 数据库） | 全部信件/文档/凭据存储 |
| **Accessibility** | 控制其他 App 界面、合成键鼠输入 | **键盘记录 + 静默 UI 控制** |
| Automation (Apple Events) | 通过 AppleScript 驱动其他 App | 控制 Finder 即等价于大范围文件访问 |
| **Screen & System Audio Recording** | 截屏与系统音频 | 屏幕内容持续采集（含明文密码） |
| Input Monitoring | 后台读取按键 | 跨 App 后台键击采集 |
| Local Network | 访问局域网设备 | 设备发现与横向移动 |

## 3. 不可绕过的硬约束（Swift 指南，2026-02）

- **无障碍权限没有干净的编程式授予方式**，用户必须手动在系统设置中开启。
- **`AXIsProcessTrustedWithOptions` 在 App Sandbox 启用时不弹系统提示** — 需同时使用 Accessibility 与 Screen Recording 的 App "几乎必然需要跑在沙箱之外"（Apple DTS 论坛确认的已知限制）。
- Screen Recording **无对应 Info.plist key**，由系统自行处理提示。
- **macOS Sequoia/Tahoe：Screen Recording 会周期性要求重新确认**（Sequoia beta 期为每周，正式版放宽为每月；Tahoe 维持每月）。没有受支持的关闭方式。
- 开发期重置：`tccutil reset Accessibility <bundle-id>` / `tccutil reset ScreenCapture <bundle-id>`

## 4. 分成两个独立权限桶（OpenClaw 明确记载）

> "macOS keeps **Accessibility, Event Posting, input listening, and Screen Recording in separate TCC buckets.** One successful grant does not prove the others are usable. ... this is why screenshots can succeed while clicks and typing fail."

还有一条安全警示值得 Curis 直接采纳：
> "Prefer granting Accessibility to the signed app ... instead of a generic `node` binary. ... any JavaScript package launched through that same executable may inherit GUI automation privileges. ... **Avoid granting Accessibility to node unless you trust every script and package launched through that exact Node install.**"

---

## 5. 对 Curis 的架构含义（推导）

| 能力形态 | 所需 TCC 权限 | 用户摩擦 | 稳定性 |
|---|---|---|---|
| **A. Browser Automation**（Playwright 驱动自带 Chromium，经 CDP 控制） | **无需 Accessibility / Screen Recording**；仅按需 Files&Folders（下载落盘）、Local Network（访问本机服务） | 低 | 高（不依赖 TCC） |
| **B. Computer Use**（合成键鼠 + 截屏） | **Accessibility + Screen Recording + Automation** 三项手动授权 | 高 | 低（签名/路径/版本变更即失效，且 Screen Recording 每月需复认） |

**核心结论**：Browser Automation 与 Computer Use 在 macOS 上是**两个成本量级完全不同**的能力。把 Web 自动化实现为"Computer Use 的一个用例"（即用截屏+点坐标去操作浏览器）会**主动继承 Computer Use 的全部授权摩擦与脆弱性**，属于明显的架构降级。这一条是本轮研究中最强的"应分层"论据。
