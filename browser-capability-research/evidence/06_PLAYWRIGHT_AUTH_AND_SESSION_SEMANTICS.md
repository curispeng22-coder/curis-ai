# Evidence 06 — Playwright 认证与会话语义（官方文档原文）

Authority Class: EVIDENCE
Collected: 2026-09-18
Primary source: `https://playwright.dev/docs/auth`（Authentication，官方文档）

---

## 1. 核心概念（原文）

> "Playwright executes tests in isolated environments called **browser contexts**."
> "Regardless of the authentication strategy you choose, you are likely to store authenticated browser state **on the file system**."

## 2. `storageState` 的安全警示（原文，关键）

> **danger**
> "The browser state file **may contain sensitive cookies and headers that could be used to impersonate you or your test account**. We strongly discourage checking them into private or public repositories."

官方建议：建立 `playwright/.auth` 目录并加入 `.gitignore`。

**含义**：`storageState` 导出的 JSON 文件在安全等级上**等同于该账号的一把万能钥匙**（可直接冒用身份）。官方定位是"测试产物 + 隔离目录"，**不是**面向商业产品的凭据安全方案。

## 3. 覆盖范围（原文）

> "Reusing authenticated state covers **cookies, local storage, IndexedDB and passkey (WebAuthn) based authentication**."

**例外**（原文）：
> "**session storage** ... is specific to a particular domain and is not persisted across page loads. **Playwright does not provide API to persist session storage**, but the following snippet can be used to save/load session storage."
（官方给出手工 `page.evaluate(() => JSON.stringify(sessionStorage))` + `context.addInitScript` 的 workaround）

## 4. 状态过期（原文）

> "Note that you **need to delete the stored state when it expires**."
> "If you don't need to keep the state between test runs, write the browser state under `testProject.outputDir`, which is **automatically cleaned up** before every test run."

**含义**：**Playwright 不负责会话有效期管理**。过期检测、失效识别、重新登录触发，**全部是 Curis 自己的责任**。这直接构成 CGAP-04 Authentication Stop Gate 的实现必要性。

## 5. API 形态（原文摘要）

```js
// 保存
await page.context().storageState({ path: authFile });
// 复用（config 级）
storageState: 'playwright/.auth/user.json'
// 复用（context 级，多角色并存）
const adminContext = await browser.newContext({ storageState: 'playwright/.auth/admin.json' });
const userContext  = await browser.newContext({ storageState: 'playwright/.auth/user.json' });
// 显式清空（模拟未登录）
test.use({ storageState: { cookies: [], origins: [] } });
```

要点：`storageState: { cookies: [], origins: [] }` 说明状态对象**只有 cookies 与 origins 两个顶层字段**（即 localStorage 挂在 origins 下）。

---

## 6. 两种持久化路径的对比（对 Curis 的架构含义）

| 维度 | `newContext({ storageState })` | `launchPersistentContext(userDataDir)` |
|---|---|---|
| 持久化内容 | cookies + localStorage + IndexedDB + passkey（显式导出） | 整个 profile 目录：cookies、localStorage、IndexedDB、**Service Workers、Cache、扩展、站点权限** |
| 与用户可见浏览器共存 | 可（context 附着于同一 browser 进程） | 可（headed 模式即真实可见窗口） |
| 隔离粒度 | **天然适合"每 Business 一个 context"** | 每 profile 一个目录 → **天然适合"每 Business 一个 profile"** |
| 凭据落盘 | 单一 JSON 文件（**高危，等于明文凭据**） | 目录内多文件（含 Chromium 自身加密的 cookie 库，但仍有可用明文索引） |
| 与 Chrome 136 限制的关系 | 不涉及 `--remote-debugging-port` 默认目录问题 | **正是 Google 推荐的正确形态**（non-default `--user-data-dir`） |

## 7. 由此产生的**必须由 Curis 自行裁定的新问题**（本证据的直接产出）

Curis 既有硬约束（见项目记忆 §8）：
> 「不可能明文落盘：`LocalDevCredentialBackend` 只存进程内存；DB 只存 `credential_ref` + `secret_digest`(sha256)」

而 `storageState` / `userDataDir` 内的 cookie 与 token **本质上是可冒用凭据**，且**必须落盘**（因为会话必须跨进程重启存活）。

→ **冲突**：Curis 现有凭据边界只覆盖了「用户配置的 API Key」，**未覆盖"浏览器会话材料"这一类新凭据**。

→ **必须在 Capability 立项时新增裁定项**（建议编号 **CGAP-04 附则**）：
1. 浏览器会话材料是否纳入 Curis 凭据治理体系（`credential_ref` 类比）？
2. 存储形态：明文 profile 目录 / Chromium 内建加密 / OS Keychain 包裹 / 全盘加密？
3. 是否允许离开本机？（与 Cloud Browser 选项直接相关）
4. 删除/登出语义：用户"删除 Business"时，profile 是否连带销毁？

> 本条是设计 CGAP-04 时**最容易遗漏**但风险最高的一环。
