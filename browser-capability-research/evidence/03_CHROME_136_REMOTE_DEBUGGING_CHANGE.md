# Evidence 03 — Chrome 136 `--remote-debugging-port` 策略变更（关键约束）

Authority Class: EVIDENCE
Collected: 2026-09-18
Primary source: Chrome for Developers Blog — "Changes to remote debugging switches to improve security", Will Harris, **Published 2025-03-17 UTC**
URL: `https://developer.chrome.com/blog/remote-debugging-port` （原文经检索命中，标注 "Last updated 2025-03-17 UTC"）

---

## 原文关键段落（逐字）

> "We've seen an increase in attackers using Chrome Remote Debugging to extract cookies. ... since App-Bound Encryption was enabled."
>
> "**Therefore, from Chrome 136 we're making changes to the behavior of `--remote-debugging-port` and `--remote-debugging-pipe`. These switches will no longer be respected if attempting to debug the default Chrome data directory.** These switches must now be accompanied by the `--user-data-dir` switch to point to a non-standard directory. A non-standard data directory uses a different encryption key meaning Chrome's data is now protected from attackers."
>
> "For developers who need to debug Chrome (for example, from VSCode), the instructions already specify use of a custom user data dir and we continue to recommend this approach to isolate any debugging from any real profiles."
>
> "**For browser automation scenarios, we recommend using Chrome for Testing** which will continue to respect the existing behavior."

## 运行时错误信息（社区实证）
启动默认 profile + `--remote-debugging-port` 时 Chrome 直接拒绝并输出：
```
DevTools remote debugging requires a non-default data directory.
Specify this using --user-data-dir
```
（来源：ChromeDriver v136 `--user-data-dir` 报错讨论贴，2025-05 社区记录）

---

## 对 Curis 的架构含义（推导，非原文）

1. **"直接挂到用户日常 Chrome 的真实 profile" 这条路在 Chrome 136+ 已被官方关闭。**
   不能再用 `--remote-debugging-port` + 默认 user-data-dir 读取用户既有登录态。
2. 因此 "使用用户正常登录状态" 的**唯一合规且可持续的实现**是：
   **Curis 自己持有一个专用浏览器 profile 目录**（`--user-data-dir` 指向 non-standard 路径），
   用户**在该 profile 内登录一次**，之后登录态随该 profile 持久化。
3. 该 profile 因使用**独立加密密钥**，与用户日常浏览数据天然隔离 —— 这在安全上**优于**原先"复用真实 profile"的设想。
4. Google 官方对自动化场景的推荐路径是 **Chrome for Testing**（一个与 Chrome Stable 分离、专为自动化构建的分发通道）；Playwright 自带的 Chromium 构建亦属同类。
5. 副作用（需在研究中登记为风险，而非缺陷）：全新 profile 首次登录中文平台，会因**设备/环境指纹为"新设备"**而更易触发平台风控（异地/异常登录校验）。这是"独立 profile"方案的固有代价。
