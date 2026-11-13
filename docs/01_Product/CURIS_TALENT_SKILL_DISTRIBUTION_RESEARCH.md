# CURIS 人才与 Skill 分发策略研究（Distribution Strategy Research）

> 身份：Curis 人才与能力情报 / 能力库运营负责人
> 日期：2026-08-19
> 范围：仅研究并提出落地策略；不修改 Blueprint / Master Map / UI Blueprint / 人才与能力页面 / Runtime / Schema；不购买服务器；不建第二套 Catalog；不大规模下载安装 Skill。
> 所有体积数字均来自真实样本实测（本地 Expert 离线快照 + GitHub API 实测 Skill 仓库/目录），来源见文末「实测方法与来源」。

---

## 0. 核心结论（先看这个）

1. **Expert 本身几乎不是安装包压力来源。** 1000 个 Expert 纯 Manifest 仅约 **8 MB**（gzip 后约 **2.4 MB**）；即使 5000 个全部带头像也仅约 **90–115 MB**，仍在可接受范围。
2. **Skill 才是空间与运维压力来源**（含脚本/资源/依赖）。典型 Skill 10–40 KB，中型 50–200 KB，重型可达数 MB；预装 1000 个中型 Skill 可达 200 MB+。
3. **推荐采用 Option A**：Expert Catalog 全量本地预置 + Skill 主要按需安装 + 预置 10–20 个种子 Skill/Expert 保证离线首启。
4. **中国用户不依赖 GitHub 即可安装**：国内主市场 SkillHub（skillhub.cn，11.7 万 Skills，列表 API，安装入口，兼容 MCP）+ ModelScope MCP（7500+）+ Gitee + 预置种子兜底，当前即可满足硬约束。
5. **当前无自建服务器即可跑通**：开发期用 GitHub/原始 source；用户期路由到 SkillHub/ModelScope/Gitee/预置种子。

---

## 1. Expert Size Audit（专家体积审计 · 实测）

### 1.1 真实样本
- 来源：本地 `backend/app/agent_conversion/sources` 中 agency-agents-zh 离线快照（markdown + yaml）。
- 实测：18 个 `.md` 专家清单，平均 **1.9 KB**（1946 B），最大 17 KB，最小 0.3 KB。
- 完整 Expert 资产（Manifest + 中文产品化 + persona + workflow + capability_candidates + security_scan）估算约 **8 KB** 量级（在 1.9 KB 基础 Markdown 上扩展身份/使命/工作流/安全字段）。

### 1.2 体积模型（未压缩配置空间）
| Expert 数 | 纯 Manifest（1.9KB） | 完整资产（8KB/个） | +小型头像（10KB/个） |
|---|---|---|---|
| 100 | 0.19 MB | 0.80 MB | 1.8 MB |
| 500 | 0.95 MB | 4.0 MB | 9.5 MB |
| 1000 | 1.9 MB | 8.0 MB | 18 MB |
| 5000 | 9.5 MB | 40 MB | 90 MB |

### 1.3 压缩后安装包增量（gzip ~70% 压缩率；头像已压缩几乎不再压）
| Expert 数 | 完整资产压缩后 | 带头像压缩后（配置压缩+头像原大小） |
|---|---|---|
| 100 | ~0.24 MB | ~1.0 MB |
| 1000 | ~2.4 MB | ~10 MB（8MB配置压至2.4 + 头像≈10MB） |
| 5000 | ~12 MB | ~50 MB（40MB配置压至12 + 头像≈50MB） |

### 1.4 索引与 Metadata
- JSON 索引（slug/name/description/version/source）每 1000 条约 50–100 KB，可忽略。
- 结论：**Expert Manifest 可直接大量本地预置**；5000 个带完整中文资产+头像也仅约 50 MB，不构成架构压力。

---

## 2. Skill Size Audit（技能体积审计 · 实测，GitHub API）

### 2.1 真实样本（GitHub API 实测）
| 仓库 / 来源 | 体积 | 说明 |
|---|---|---|
| anthropics/skills 全量 19 个 | 均值 **29.5 KB**，min 8 KB，max 135 KB，合计 560.5 KB | 轻量 Skill 代表 |
| openai/skills（已 DEPRECATED 2026-06-22） | 仓库整体 2.4 MB | 历史存量 |
| obra/superpowers | 4.5 MB | 开发工作流 Skill 集合 |
| alirezarezvani/claude-skills（362 个） | 19.8 MB（均值 ~55 KB） | 大型集合代表 |
| openai 抽样 | playwright / security-best-practices / figma-components / notion-page / linear：2–40 KB | 中轻量 |
| obra 抽样 | brainstorming / systematic-debugging / receiving-code-review / executing-plans / verification-before-completion：2–15 KB | 纯指令型 |

### 2.2 体积区间
- **轻量 Skill**（仅 SKILL.md + 少量 reference）：10–40 KB
- **中型 Skill**（含 scripts/references/assets）：50–200 KB
- **重型 Skill**（含大型资源/模型/二进制）：数 MB

### 2.3 预装影响估算
| 场景 | 体积影响 |
|---|---|
| 预装 100 个轻量 Skill（30KB 均值） | ~3 MB |
| 预装 100 个含中型（200KB 均值） | ~20 MB |
| 预装 1000 个轻量 Skill | ~30 MB |
| 预装 1000 个含中型 | **200 MB+** |
| 预装 1000 个 alirezarezvani 级（55KB 均值） | ~55 MB |

### 2.4 结论
- **Skill 含脚本/资源/依赖，是真正的空间与更新压力来源**，不适合全部内置。
- 必须主要按需安装；仅预置少量「产品成立必需 / 极高频」的轻量种子 Skill。

---

## 3. Built-in Expert Recommendation（预置专家分级）

原则：仅预置「产品成立必需 + 默认职能组织 + 高频通用」，不为了"人才库丰富"塞安装包。其余进 Catalog 按需招募。

### 3.1 BUILT-IN（随安装包预置，约 10–15 个）
| 专家 | 分级依据 | 备注 |
|---|---|---|
| CEO Assistant | 产品成立必需 | 全局助理 / 通知 / 命令中枢 |
| 空间工程部核心 Employee | 默认职能组织（Gap，Curis 内置定义，不得冒充外部 Expert） | 平台职能，无外部对应 |
| 数据分析部 Company Analyst / 公司经营分析师 | 默认职能组织（Gap，待组合或内置） | 组件齐全待组合验证 |
| 中文文档处理专家（docx/pdf/xlsx/pptx/csv） | 高频通用 | 绑定内置 Office Skill |
| 搜索与研究专家 | 高频通用 | 绑定搜索/研究 Skill + 搜索 MCP |
| 基础编程助手 | 高频通用 | 绑定代码 Skill + git MCP |
| 通用办公协作（飞书/日历/邮件） | 高频通用 | 绑定连接器 |
| 产品/研究通用专家 | 高频通用 | Catalog 优先，安装包可含 1 个轻量默认 |

### 3.2 CATALOG（市场展示，点击「招募/添加」才本地创建）
- 其余所有外部 Expert / Expert Team（设计、产品深度、各行业专家、Code Review、增长、金融、法律、科研、教育、医疗、房地产、制造/供应链、咨询等）。
- 展示字段：中文名称 / 中文介绍 / 分类 / 能力 / Skill·Connector 依赖 / 来源 / 验证状态 / License / 推荐场景。
- 用户点击「招募」→ 写入本地 EmployeeTemplate / 实例化 → 检查并安装 Required Skills → Ready。

---

## 4. Built-in Skill Recommendation（预置技能三层）

### 4.1 Built-in Skills（随产品预置，约 10–20 个轻量种子）
- 中文文档处理：docx / pdf / xlsx / pptx / csv 中文版
- 搜索 / 网页抓取
- 基础编程助手
- 中文办公协作（飞书/日历/邮件基础）
- 保证**离线首启即可用**，零网络兜底。

### 4.2 Curis Catalog Skills（已验证、中文化；市场展示，未安装只存轻量 Catalog 信息）
- 来自候选池中 License 清晰、已中文产品化的 Skill。
- 用户点击「安装」才落本地。

### 4.3 External Marketplace Skills（搜索/打开/接入）
- SkillHub（腾讯）、ClawHub（含中国镜像）、GitHub、Anthropic Skills、OpenAI Plugins、ModelScope Skills。
- Curis 可搜索 / 打开 / 接入这些来源，不内置全部。

---

## 5. Expert Catalog Strategy（专家目录策略）

- **推荐：Expert Catalog 全量本地预置**（Manifest 轻量，见 §1，1000 个仅 8MB）。
- 只有真正大型的 Skill / Tool 按需下载。
- 不引入不必要的远程 Catalog 基础设施（无服务器条件下 Option B/C 不可行）。
- Expert Manifest 已存在 → 用户招募 → 检查 Required Skills → 已装直接绑定 / 未装提示或自动安装 → Employee Ready。

---

## 6. SkillHub Integration Research（SkillHub 集成调研）

### 6.1 SkillHub 是什么（实测）
- **腾讯 SkillHub**：`https://skillhub.cn/`，标题"专为中国用户优化的 Skills 社区"，已 **11.7 万个 AI Skills**，提供高速下载、一键安装。
- 2 个月累计下载 3000 万次；内置 **SkillPay**（微信支付）打通技能付费；**兼容 MCP 协议**；可在 WorkBuddy、QClaw、Kimi、Claude 等多生态使用。
- 公开能力：
  - **列表接口**（"Find Skill"技能基于 skills 列表接口，关键词分词搜索 + 一级标签筛选）
  - **安装入口**：`https://skillhub.cn/install/skillhub.md`
  - 企业技能：`https://skillhub.cn/enterprise/org-...`
- 来源：`https://skillhub.cn/`、`https://tech.cnr.cn/techgd/20260605/t20260605_527649169.shtml`

### 6.2 EvoFlow「打开 SkillHub」与安装流程
- EvoFlow（EvovexAI）为本地优先桌面 AI 运行时（Tauri/React 控制面板 EvoPanel），加载 SKILL.md 包。其"打开 SkillHub"模式 = 在 Curis 类 UI 内跳转/嵌入 SkillHub → 用户选 Skill → 接收安装信息 → 后台下载校验安装。
- 对 Curis 的启示：Curis UI 内置"技能市场"页 → 路由 SkillHub 列表 API → 中文产品化展示 → 用户点击安装。

### 6.3 Curis 能否一键安装
- **可行**。行业已验证模型：Skill = 含 `SKILL.md` 的文件夹；安装 = 下载 + 解包 + 复制到约定目录。
- 直接对齐 **Agent Skills 开放标准**（`https://agentskills.io`，Claude Code/Cursor/Codex/GitHub Copilot/VS Code 已兼容），一次构建跨生态复用。
- 若无直接安装 API，最简合法路径：Curis「打开 SkillHub / 跳转」→ 用户选 Skill → Curis 接收 URL/Package/Deep Link → 后台 download+verify+land。

---

## 7. On-demand Installation Flow（按需安装流）

### 7.1 Expert 招募流（Curis 内）
```
Expert Manifest 已本地预置（Catalog）
→ 用户点击「招募 / 添加」
→ 写入 EmployeeTemplate / 实例化
→ 检查 Required Skills / Connectors
→ 已安装 → 直接绑定
→ 未安装 → 提示用户或自动安装（走 §7.2 Skill 安装流）
→ Employee Ready
```

### 7.2 Skill 安装流（后台自动完成，用户零摩擦）
```
用户在市场点击「安装 Skill」
→ Curis 解析来源（SkillHub / ClawHub / GitHub / Anthropic / 内置）
→ 下载器：codeload zip / raw / ClawHub package download / sparse-checkout
→ 解包器：zip/tar 解压 + 路径穿越防护（realpath 校验）
→ 校验器：① SKILL.md 存在性 ② name/description 前置 YAML ③ SHA-256 完整性 ④ 内容安全扫描（信任层）
→ 落位器：复制到约定 skills 目录（全局/项目级），幂等（已存在提示/跳过/覆盖）
→ 触发宿主 Agent 重新扫描 skills 目录 → 刷新即用
```
- **普通用户不应自己复制 GitHub 地址、运行命令或理解 Skill 工程结构。**
- 参考范本：ClawHub CLI `clawhub install <slug>` + `package verify`（npm integrity + ClawHub SHA-256）；OpenAI `install-skill-from-github.py`（路径穿越防护 + SKILL.md 校验 + 名称单段校验 + 幂等）。

---

## 8. China Accessibility（中国用户可用性 · 硬约束）

### 8.1 海外源在大陆可访问性
| 市场 | 国内可访问性 |
|---|---|
| GitHub raw / git clone | ⚠️ 可达但严重不稳定，raw 常失败（DNS 污染），需镜像 |
| ClawHub（clawhub.ai） | ⚠️ 海外源龟速；**已有官方中国镜像** `https://cn.clawhub-mirror.com/`（字节/火山引擎赞助，全中文语义搜索） |
| mcp.so | ✅ 大概率国内可达（广州公司运营），18000+ MCP |
| Anthropic/OpenAI Skills | ⚠️ 依赖其服务，国内普遍受限/慢，不宜作主源 |
| Hugging Face | ❌ 长期被墙，需 hf-mirror |

### 8.2 国内可用源（真实 URL）
- **腾讯 SkillHub** `https://skillhub.cn/` — 主市场，11.7 万 Skills，列表 API，安装入口，兼容 MCP。✅
- **魔搭 ModelScope MCP** `https://modelscope.cn/mcp` — 7500+ MCP，OpenAPI，Skills 中心。✅
- **Gitee** `https://gitee.com` — Curis 自有 Skill 仓库首发地（GitHub 仅作 upstream）。✅
- **火山引擎 AgentKit** `https://www.volcengine.com/docs/86681/` — 企业级能力源。✅
- **飞书/钉钉开放能力** — 预置连接器/专家来源。✅

### 8.3 Fallback 与硬约束判断
- 三级 Fallback：① 安装包内预置种子（离线可用）② Catalog 元数据缓存、安装时再拉 ③ 未来 Curis Mirror。
- **结论：中国用户不需要 GitHub 也能安装 Curis 人才/Skill，当前即可满足。**

---

## 9. No-server Current Strategy（无服务器当前策略）

- **开发期**：直接用 GitHub / 原始 source（开发者环境已有代理/镜像，可接受）。
- **用户期（现在）**：路由到 SkillHub + ModelScope MCP + Gitee + 预置种子，完全不触碰 GitHub 即可完成"发现→安装→运行"。
- **不要求立即购买服务器。**

---

## 10. Future Mirror Strategy（未来 Mirror 策略）

- 已有成功先例：ClawHub 由火山引擎/BytePlus 赞助建成 `cn.clawhub-mirror.com`（同步 4.3 万+ Skills，全中文）。
- **成本**：对象存储 + CDN 国内节点 + 增量同步任务，早期可控；走国内云按量付费，无需自建机房。
- **合规**：ICP 备案 + 《网络安全法》《数据安全法》《生成式 AI 服务管理暂行办法》内容审核 + 上架留痕 + 许可合规（MIT/Apache 可镜像，专有需授权）。
- **安全**：ClawHub 早期约 17% 技能含恶意载荷，Mirror 必须做安全扫描（VirusTotal/ClawScan 类）+ 人工精选。

---

## 11. Option A / B / C Comparison（方案比较）

| 维度 | Option A：Expert 全本地 + Skill 按需 | Option B：少量 Expert 本地 + Expert Catalog 远程 + Skill 按需 | Option C：Expert/Skill 都主要远程 Catalog |
|---|---|---|---|
| 安装包大小 | 小（Expert Manifest 轻，1000 仅 8MB） | 小 + 需远程 Catalog 服务 | 最小，但依赖远程 |
| 首次使用体验 | 开箱即用（Expert 全在，Skill 点装） | 需联网拉 Catalog | 强依赖网络 |
| 离线能力 | Expert 全离线；Skill 需联网装 | Expert 依赖远程 Catalog | 差 |
| 中国用户可用性 | ✅ Expert 无碍；Skill 靠 SkillHub/ModelScope | ⚠️ 远程 Catalog 需国内可达节点 | ❌ 强依赖远程 |
| 更新能力 | Expert 随包更新；Skill 市场更新 | 远程 Catalog 更新 | 远程更新 |
| 运维成本 | 低（无服务器） | 中（需 Catalog 服务） | 高（需服务器+CDN） |
| 安全 | 本地可控 | Catalog 服务需防护 | 远程攻击面大 |
| License | 本地审计清晰 | 远程源许可追踪复杂 | 复杂 |
| 未来扩展 | ✅ 5000 Expert 仅 ~50MB 带头像 | 受 Catalog 服务限制 | 受服务器限制 |
| 当前无服务器条件 | ✅ 可行 | ❌ 不可行（需远程基础设施） | ❌ 不可行 |

---

## 12. Final Recommendation（最终推荐）

> **Curis 当前阶段采用 Option A。**

1. **Expert Catalog 全量本地预置**（Manifest 轻量，无架构压力；5000 个带头像也仅 ~50MB）。
2. **Skill 主要按需安装**（含脚本/资源，是压力源；仅预置 10–20 个轻量种子 Skill）。
3. **预置种子保证离线首启**：CEO Assistant + 空间工程/数据分析默认职能 + 中文文档/搜索/编程/办公 高频专家与 Skill。
4. **国内源优先**：SkillHub（主市场）+ ModelScope MCP + Gitee + 预置种子兜底；ClawHub 中国镜像 / mcp.so 作为海外优质 Skill 的国内可达增强。
5. **信任层必须内置**：来源 allowlist / 审核 + SKILL.md 静态检查 + `allowed-tools` 约束 + 沙箱执行；安装时 SHA-256 校验 + 路径穿越防护（对齐 ClawHub/OpenAI 范本）。
6. **不引入远程 Catalog 基础设施**，当前无服务器即可跑通。

---

## 13. CEO Decisions Required（需 CEO 决策项）

1. 确认 **Option A**（Expert 全本地 + Skill 按需）为当前阶段分发架构。
2. 确认 **BUILT-IN 预置清单**（§3.1 的 10–15 个专家 + §4.1 的 10–20 个种子 Skill）。
3. 确认是否接入 **SkillHub 列表 API** 作为国内主市场（开发期 GitHub，用户期 SkillHub）。
4. 确认 **未来 Curis Mirror** 的建设时机（当前不急，先靠 SkillHub/ModelScope/Gitee）。
5. 确认 **信任层/安全扫描策略**（来源审核 + SHA-256 + 沙箱）的落地优先级。

---

## 附：实测方法与来源

### Expert 体积实测
- 本地快照：`backend/app/agent_conversion/sources`（agency-agents-zh 离线 markdown/yaml）
- 命令：`find ... -name '*.md' -print0 | xargs -0 wc -c`，18 个文件，均值 1.9 KB。

### Skill 体积实测（GitHub API，2026-08-19）
- 仓库整体 git size：openai/skills 2.4 MB、obra/superpowers 4.5 MB、alirezarezvani/claude-skills 19.8 MB。
- anthropics/skills 全量 19 个目录：均值 29.5 KB（8–135 KB）。
- openai/obra 单 Skill 抽样：2–40 KB。

### 联网调研来源（真实 URL）
- 腾讯 SkillHub：`https://skillhub.cn/`
- ClawHub 国际：`https://www.clawhub.ai/` ｜ 中国镜像：`https://cn.clawhub-mirror.com/`
- 魔搭 ModelScope MCP：`https://modelscope.cn/mcp`
- mcp.so：`https://mcp.so`
- Gitee：`https://gitee.com`
- 火山引擎 AgentKit：`https://www.volcengine.com/docs/86681/`
- ClawHub npm：`https://www.npmjs.com/package/clawhub`
- Anthropic skills：`https://github.com/anthropics/skills` ｜ Agent Skills 标准：`https://agentskills.io`
- OpenAI skills（DEPRECATED）：`https://github.com/openai/skills` ｜ 安装脚本：`https://github.com/openai/skills/blob/main/skills/.system/skill-installer/scripts/install-skill-from-github.py`
- GitHub 归档下载：`https://docs.github.com/en/rest/repos/contents`
- 国内可访问性依据：CSDN/53AI/AI-Indeed 等公开报道（ClawHub 镜像、GitHub raw 国内问题）

---

CURIS TALENT & SKILL DISTRIBUTION STRATEGY
— RESEARCH COMPLETE
— STOP FOR CEO REVIEW
