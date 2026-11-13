# CURIS COMPETITIVE SETTINGS MATRIX

> Authority Class: RESEARCH / EVIDENCE
> Status: v3（COMPLETE）——九产品列全部回填。
> Date: 2026-09-12
> 方法：逐产品进入 Settings，字段级记录；UNKNOWN = 无证据。细节见各 FUNCTION_INVENTORY 对应章节。

## 1. Settings 分区存在性

| 分区 | Curis | Zcode | Coze/扣子 | Claude | Cursor | Workbuddy | ChatGPT ⏳ | Manus ⏳ | Devin ⏳ |
|---|---|---|---|---|---|---|---|---|---|
| General | 公司设置（本地草稿） | ✅ | ✅ 个人设置 | ✅ General（快捷键+computer use） | ✅（VS Code Import 等） | ✅（12 条目之一） | | |  | ✅ General | ✅（Settings→各节） | ✅ org/team 设置 | |
| Appearance/Theme | 品牌主题 tab（草稿）；主题跟随系统 | ✅ 主题 | UNKNOWN | ✅ Appearance | PARTIAL（主题继承 VS Code） | ✅ | | |  | ✅ | UNKNOWN | UNKNOWN | |
| Language | ❌ | UNKNOWN | ✅ | UNKNOWN | ✅ | UNKNOWN | | |  | ✅ | UNKNOWN | UNKNOWN | |
| Account/Profile | ❌（左下身份 chip） | ✅ 账号 | ✅ 头像/昵称 | ✅ Account | ✅ Account | ✅（账号/积分/账单独立文档区） | | |  | ✅ Account | ✅ Credits/定价 | ✅（seats/账单） | |
| Models/Providers | 模型管理 UI（accepted 一角） | ✅ 会话级模型 | ✅ Agent 级模型设置 | PARTIAL（模型/effort/thinking 在对话内） | ✅ Models（双池+BYOK+Auto 路由） | ✅ 模型配置（快选 5 家+三档调度） | | |  | ✅ 模型选择 | ✅ 1.6 Lite/Max | UNKNOWN | |
| Skills | ❌ | ✅ 插件/技能启用 | ✅ 技能挂载 | ✅ Capabilities（Skills 开关） | ✅（Customize/MCP 区） | ✅ 技能市场+我的技能 | | |  | PARTIAL（GPTs 停止个人新建/Apps） | ✅ Skills（SKILL.md+Build with Manus） | ✅ Playbooks/Knowledge | |
| Tools/MCP | ❌ | ✅ MCP server 配置 | ✅ 插件 | ✅ Connectors / Extensions | ✅ MCP（含 OAuth 字段） | ✅ 连接器（每项独立授权：OAuth/扫码/MCP） | | |  | ✅ Connected apps/MCP | ✅ Connectors | ✅ Integrations（Slack 等） | |
| Instructions/Rules | ❌ | ✅ AGENTS.md | PARTIAL（人设与回复逻辑在 Agent 配置） | ✅ Instructions（账户级） | ✅ Rules & Memories（四档应用+优先级链） | ✅ 项目指令（项目配置注入） | | |  | ✅ Custom instructions | PARTIAL（Knowledge 偏好学习） | ✅ Knowledge（Trigger Description）+Playbooks | |
| Memory | ❌ | ❌ | ✅ 长期记忆 | ✅ Memory（topic 级逐条查看/编辑/删除/Pause/Reset/导入导出） | ✅ Memories（自动+注入警示） | ✅ "记忆与进化"（每晚摘要/编辑/关闭/跨 AI 导入） | | |  | ✅（memory summary+sources 可解释） | ✅ Knowledge 偏好学习 | ✅ org Knowledge（AI 建议） | |
| Permission/Security | ❌ | ✅ permission mode/allowlist | ✅ 项目/共享权限默认值 | ✅ Cowork 三模式+connector 三档+删除保护 | ✅ Agents（Approvals & Execution：三档 Run Modes+permissions.json+sandbox） | ✅ 权限模式（默认权限/安全沙箱）+安全中心（12 分组+审计中心） | | |  | ✅ Data controls/Security | PARTIAL（Allow Once/Always） | ✅ Security/policy | |
| Privacy/Data | ❌ | ✅ 遥测/保留 | UNKNOWN | PARTIAL（隐身 chat/敏感 opt-in 散布） | ✅ Privacy Mode | ✅ 数据管理 | | |  | ✅ Data controls | UNKNOWN | PARTIAL | |
| Usage/Billing | ❌ | ✅ 用量 | ✅ 积分/账单入口 | ✅ Usage（+usage ring 贴近操作点） | ✅ Usage dashboard | ✅（Credits/Usage/Billing/Invoice 独立区） | | |  | ✅（plan 限额） | ✅ Credits（owner-only Collab） | ✅ ACU/Session Insights | |
| Automation | ❌ | ❌ | ✅ 触发器（仅飞书渠道） | ❌（Cowork 任务非 settings） | ✅（/automate；triggers 7 类；归属三档） | ✅ 自动化（7 配置项：名称/提示词/工作空间/权限模式/模型技能专家连接器/定时规则/推送） | | |  | ✅ Scheduled tasks（3 类含事件触发：Trigger/Condition/Prompt） | ✅ Scheduled Tasks（执行历史） | ✅ Automations（8 触发源×4 动作）+Scheduled Sessions（Run-as） | |
| Notification | 通知偏好 tab（草稿） | ✅ 后台任务通知 | ✅ 通知 | UNKNOWN（字段级） | PARTIAL | ✅ 消息中心+IM 双通道 | | |  | ✅ Notifications | UNKNOWN | ✅ Slack | |
| Shortcuts | ❌ | ❌ | ❌ | ✅ General 内 | ✅ Shortcuts | UNKNOWN | | |  | UNKNOWN | UNKNOWN | UNKNOWN | |
| Voice | ❌ | ❌ | ✅ 语音（对话体验内） | PARTIAL（Quick Entry 语音） | ❌ | ❌ | | |  | ✅ Voice | UNKNOWN | ✅（session voice） | |
| Developer/Advanced | ❌ | ✅ hooks/sandbox | ✅ PAT 令牌 | ✅ Developer mode（UNKNOWN 字段级） | ✅ Customize（hooks 事件全列） | ✅（开放平台/自定义 MCP） | | |  | ✅ Apps & SDK | PARTIAL（CLI/My Computer） | ✅ API/`.devin/wiki.json` | |
| 组织/团队管理 | ❌ | ❌（企业策略层） | ✅ 企业设置（超管） | ✅ Org settings（Owner：Capabilities/Connectors/Skills/权限上界/compliance——org 关能力直接改变个人可用集） | ✅ Teams 档（费率/共享） | ✅ 企业版（custom agent 版本化/共享 skills/experts/ROI 看板） | | |  | ✅（Projects 共享/Work 团队） | ✅ Collab（团队计划） | ✅ org settings/Teams（full/flex seats） | |
| Update/About | ❌ | ✅ | UNKNOWN | UNKNOWN | ✅ Updates | ✅ Download-History/Changelog | | |  | ✅ About | UNKNOWN | UNKNOWN | |

## 2. 关键分区字段级对照（已有证据的最深层次）

### 2.1 Models/Providers

| 字段 | Curis | 最佳竞品参照 |
|---|---|---|
| Provider 列表/凭据状态 | Runtime 有（Keychain/健康检查 accepted），产品面缺 | Workbuddy：自定义模型本地存 Key；Cursor BYOK |
| 模型字段（Name/ID/Vision/Reasoning/Context/默认/成本） | Registry 为 Review 文档，UI 无 | Cursor 双池+Auto 路由三档+计价细节；Workbuddy 内置 14 模型 |
| 每 Agent/员工默认模型 | 缺 | Coze 节点级独立模型；Workbuddy 专家×模型解耦 |
| 用量贴近操作点 | 缺 | Claude usage ring 双显（session+plan）；"哪些操作耗用量"教育 |

### 2.2 Permission（竞品已进入"四层体系"时代）

| 层 | Claude | Cursor | Workbuddy | Curis |
|---|---|---|---|---|
| 档位模式 | Cowork 三模式/Code 五模式 | 三档 Run Modes | 权限模式+安全沙箱 | Scope 模型（Runtime，无档位面） |
| 粒度 allowlist | 逐站/逐 app 清单 | permissions.json 自然语言 allow/block_instructions | 逐连接器授权+公共/个人票据双轨 | ❌ |
| 高危特殊保护 | 删除显式批准 | 三道硬保护闸 | 批量删除阈值 50+IM 远程批准 | ❌ |
| 组织上界 | Org settings 能力上界 | Teams 归属/计费身份 | 管理员审计中心（拦截/放行日志导出） | 四层 scope 数据隔离（Runtime，强） |

**结论**：Curis 的 scope 隔离是独有强项，但权限的**用户可配置四层体系**（档位/白名单/高危保护/组织上界）全面缺位——这是 M-09 的具体化。

### 2.3 Memory

| 能力 | Claude | Cursor | Workbuddy | Coze | Curis |
|---|---|---|---|---|---|
| 逐条查看/编辑/删除 | ✅ | ✅（自动） | ✅ | ✅ | ❌（共识归档 Runtime only） |
| 自动沉淀 | ✅ topic 级 | ✅ | ✅ 每晚摘要 | ✅ 长期记忆 | ✅（会议决议/知识沉淀，Runtime） |
| 安全设计 | 敏感主题 opt-in+保存通知 | 注入警示（官方承认风险） | 可关闭/导入导出 | 范围归属 | UNKNOWN |
| 导入/导出 | ✅ 跨工具导入导出 | UNKNOWN | ✅ 跨 AI 导入 | UNKNOWN | ❌ |

## 3. Curis Settings 应有全量清单

见 `CURIS_DESKTOP_PRODUCT_AND_DESIGN_DIRECTION.md` §2.7。吸收竞品 IA 洞察（Claude P11）：**能力开关（Capabilities）/ 个性化（Appearance/Memory）/ 接入（Connectors/Extensions）/ 用量（Usage）/ 组织管理（Org）** 五类分开，不做大一统"偏好"页；组织上界与个人自选双层嵌套（Claude P10）。

## 4. 结论

1. 竞品 Settings 共性骨架 = 个人偏好 + 模型/能力 + 接入 + 权限/隐私 + 用量/账单 + 通知 + 组织管理 + 关于；Curis 仅"公司档案"一角且为本地草稿。
2. 权限四层体系、Memory 透明化、Usage 贴近操作点是 2026 竞品 Settings 的三个成熟标志，Curis 全缺。
3. Curis 独有可转化素材：四层 scope 隔离（→权限与数据节用户语言）、Meeting cycle budget（→运行与成本预算语义）。

## 更新记录

- 2026-09-12 v1：Zcode/Coze/Curis 列成稿。
- 2026-09-12 v2：回填 Claude/Cursor/Workbuddy；新增 2.2 权限四层对照与 2.3 Memory 对照。
- 2026-09-12 v3：回填 ChatGPT/Manus/Devin；SETTINGS MATRIX COMPLETE。要点：定时/事件自动化在 ChatGPT（3 类含事件触发）、Manus（Scheduled Tasks+执行历史）、Devin（8 触发源×4 动作+Scheduled Sessions Run-as）已全部标配；Devin Knowledge 的 Trigger Description（"何时使用这条知识"）是组织知识产品的最佳字段设计；ChatGPT Memory 已带 sources 可解释性。
