# Evidence 02 — License 原文核验记录

Authority Class: EVIDENCE
Collected: 2026-09-18
Method: GitHub REST API (`/repos/{owner}/{repo}` → `license.spdx_id`) + `raw.githubusercontent.com` LICENSE 原文抓取

---

## A. 通过 GitHub API 核验（SPDX 由 GitHub 判定）

| 仓库 | SPDX | Stars | Archived | pushed_at | 语言 |
|---|---|---|---|---|---|
| microsoft/playwright | Apache-2.0 | 96,315 | false | 2026-09-18 | TypeScript |
| microsoft/playwright-mcp | Apache-2.0 | 37,242 | false | 2026-09-17 | TypeScript |
| puppeteer/puppeteer | Apache-2.0 | 95,590 | false | 2026-09-18 | TypeScript |
| browser-use/browser-use | MIT | 115,108 | false | 2026-09-15 | Python |
| browserbase/stagehand | MIT | 24,332 | false | 2026-09-18 | TypeScript |
| steel-dev/steel-browser | Apache-2.0 | 7,661 | false | 2026-09-16 | TypeScript |
| **Skyvern-AI/skyvern** | **AGPL-3.0** | 23,030 | false | 2026-09-18 | Python |
| trycua/cua | MIT | 23,071 | false | 2026-09-18 | HTML |
| microsoft/OmniParser | **CC-BY-4.0** | 25,404 | false | 2026-07-20 | Jupyter |
| OpenAdaptAI/OpenAdapt | MIT | 1,729 | false | 2026-09-14 | Python |
| simular-ai/Agent-S | Apache-2.0 | 12,318 | false | 2026-09-05 | Python |
| chromiumembedded/cef | NOASSERTION（实为 BSD-3-Clause，见下） | 4,788 | false | 2026-09-17 | C++ |
| tauri-apps/tauri | Apache-2.0 | 111,161 | false | 2026-09-18 | Rust |
| electron/electron | MIT | 123,135 | false | 2026-09-18 | C++ |
| **browserbase/mcp-server-browserbase** | Apache-2.0 | 3,411 | **true（已归档）** | 2026-07-20 | TypeScript |
| modelcontextprotocol/servers | NOASSERTION（MIT→Apache-2.0 迁移中） | 90,444 | false | 2026-09-03 | TypeScript |
| Kaliiiiiiiiii-Vinyzu/patchright | Apache-2.0 | 4,623 | false | 2026-09-13 | TypeScript |
| seleniumbase/SeleniumBase | MIT | 13,025 | false | 2026-09-18 | Python |
| **ultrafunkamsterdam/undetected-chromedriver** | **GPL-3.0** | 12,843 | false | 2025-07-05 | Python |
| cloudflare/puppeteer | Apache-2.0 | 371 | false | 2026-09-12 | TypeScript |
| openai/openai-cua-sample-app | MIT | 1,861 | false | 2026-09-04 | TypeScript |
| anthropics/claude-quickstarts | MIT | 17,691 | false | 2026-09-17 | TypeScript |
| browser-use/web-ui | MIT | 16,569 | false | 2026-05-15 | Python |
| browser-use/macOS-use | MIT | 1,987 | false | 2025-03-05 | Python |
| nanobrowser/nanobrowser | Apache-2.0 | 13,810 | false | 2026-08-18 | TypeScript |
| e2b-dev/E2B | Apache-2.0 | 13,870 | false | 2026-09-18 | Python |
| browserless/browserless | NOASSERTION（见下，SSPL-1.0 OR 商业） | 13,712 | false | 2026-09-18 | TypeScript |
| **lightpanda-io/browser** | **AGPL-3.0** | 35,422 | false | 2026-09-18 | Zig |
| screenpipe/screenpipe | NOASSERTION（自定义 LICENSE.md） | 21,619 | false | 2026-09-18 | TypeScript |
| unclecode/crawl4ai | Apache-2.0 | 83,818 | false | 2026-09-18 | Python |
| ScrapeGraphAI/Scrapegraph-ai | MIT | 31,079 | false | 2026-09-07 | Python |
| **firecrawl/firecrawl** | **AGPL-3.0** | 181,903 | false | 2026-09-18 | TypeScript |
| microsoft/playwright-python | Apache-2.0 | 15,012 | false | 2026-09-15 | Python |
| webdriverio/webdriverio | MIT | 9,835 | false | 2026-09-17 | TypeScript |
| SeleniumHQ/selenium | Apache-2.0 | 34,499 | false | 2026-09-18 | Java |

> Stars 数据仅作生态活跃度参考，**不作为质量结论**（符合研究口径）。

---

## B. LICENSE 原文核验（`raw.githubusercontent.com`）

### chromiumembedded/cef → BSD-3-Clause
原文（节选）：
```
// Copyright (c) 2008-2020 Marshall A. Greenblatt. Portions Copyright (c)
// 2006-2009 Google Inc. All rights reserved.
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//    * Redistributions of source code must retain the above copyright notice...
//    * Redistributions in binary form must reproduce the above copyright notice...
//    * Neither the name of Google Inc. nor the name Chromium Embedded
//      Framework nor the names of its contributors may be used to endorse
//      or promote products derived from this software without specific prior
//      written permission.
```
**结论**：典型三条款 BSD。允许闭源商业分发，需保留版权声明且不得使用其名义背书。GitHub API 报 NOASSERTION 仅因其非标准文件头。

### chromium/src → BSD-3-Clause
`https://chromium.googlesource.com/chromium/src/+/main/LICENSE?format=TEXT`（base64 解码）：
```
// Copyright 2015 The Chromium Authors
//    * Neither the name of Google LLC nor the names of its
// contributors may be used to endorse or promote products derived from
// this software without specific prior written permission.
```
**结论**：BSD-3-Clause。**注意**：源码许可允许闭源分发，但 **"Chrome"/Google 品牌与商标不可使用**；且出厂二进制含大量第三方许可（MPL/LGPL 等）需随附 notices。

### browserless/browserless → SSPL-1.0 OR Browserless Commercial License ⚠️
原文：
```
This work is dual-licensed under the MongoDB Server-Side Public License OR the
browserless commercial license.
If you want to use browserless to build commercial sites, applications, or in a
continuous-integration system that's closed-source then you'll need to purchase
a commercial license.
SPDX-License-Identifier: SSPL-1.0 OR Browserless Commercial License
```
**结论**：**闭源商业产品不可直接集成自托管版**，须购买商业许可或仅用其云服务。

### browser-use/browser-use → MIT（Copyright (c) 2024 Gregor Zunic）
### browserbase/stagehand → MIT（Copyright (c) 2024 Browserbase Inc.）
### trycua/cua → MIT（LICENSE.md，Copyright (c) 2025 Cua AI, Inc.）
### microsoft/playwright-mcp → Apache-2.0
### browser-use/web-ui → MIT（Copyright (c) 2024 Browser Use Inc.）
### Skyvern-AI/skyvern → AGPL-3.0（原文首段为 GNU Affero General Public License v3）
### modelcontextprotocol/servers → MIT → Apache-2.0 迁移中
原文：
```
The MCP project is undergoing a licensing transition from the MIT License to the
Apache License, Version 2.0 ("Apache-2.0"). All new code and specification
contributions to the project are licensed under Apache-2.0. Documentation
contributions (excluding specifications) are licensed under CC-BY-4.0.
Contributions ... originally licensed ... under the MIT License and who have
not yet granted explicit permission to relicense remain licensed under the MIT License.
```
### screenpipe/screenpipe → 自定义（LICENSE.md，非 SPDX 标准）
### trycua/cua、browser-use/browser-use（`/main/LICENSE`）——路径差异，已二次确认

---

## C. Microsoft WebView2 运行时分发条款（技术文档，非法律条款）
Source: `https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/distribution`
- Microsoft 提供 Evergreen Bootstrapper / Standalone Installer 与 **Fixed Version** 两种分发模型；文档明确指导开发者将运行时**打包进自有应用**（`package it with your WebView2 app`）。
- 生产应用**不得**以 Microsoft Edge Stable 频道作为承载平台，只能使用 WebView2 Runtime。
- Fixed Version 二进制 **> 250MB**，不可从网络位置/UNC 路径运行。
- **备注**：该页为部署指南，未含法律许可文本；正式条款以运行时随附的 Microsoft 软件许可条款为准。**结论：商业分发被实操允许，但法律文本需另行核验 → 标记为未完全验证。**

---

## D. 商用集成结论（Curis 为闭源商业桌面产品）

| 判定 | 项目 |
|---|---|
| ✅ 可闭源集成/分发 | Playwright (Apache-2.0)、Playwright MCP (Apache-2.0)、Puppeteer (Apache-2.0)、Electron (MIT)、Tauri (Apache-2.0)、CEF (BSD-3)、Chromium (BSD-3)、Stagehand (MIT)、browser-use (MIT)、cua (MIT)、nanobrowser (Apache-2.0)、E2B (Apache-2.0)、steel-browser (Apache-2.0)、SeleniumBase (MIT)、patchright (Apache-2.0)、Agent-S (Apache-2.0)、OpenAdapt (MIT)、crawl4ai (Apache-2.0)、ScrapeGraphAI (MIT) |
| ⚠️ 需评估/附 notices | OmniParser (CC-BY-4.0：署名义务，且**模型权重条款另计**)、WebView2（法律文本待核）、screenpipe（自定义许可） |
| ⛔ 闭源分发受阻 | **Skyvern (AGPL-3.0)**、**Firecrawl (AGPL-3.0)**、**Lightpanda (AGPL-3.0)**、**undetected-chromedriver (GPL-3.0)**、**browserless (SSPL-1.0 或商业许可)** |

> AGPL/GPL/SSPL 对闭源分发构成实质障碍；作为**外部 Provider 或仅借鉴**则不受同一约束（须逐案评估）。
