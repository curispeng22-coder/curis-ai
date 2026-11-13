# Curis 人才市场产品地图

Status: Review  
日期：2026-08-14  
依据：`Curis_Product_Master_Map.md`、`Curis_Product_Rethink_Reasoning.md`、`Talent_Market_Resource_Audit.md`

## 1. 产品定位

人才市场是 Curis 的第六个主工作区域，负责“发现和扩展公司外部能力”。

```text
人才市场
├── 专家：职业能力组合，招募后成为 Employee
├── 技能：可复用的方法、Instruction、Skill 包和能力依赖
└── 连接器：外部服务连接能力，安装后去设置完成授权
```

不新增第二套组织/Admin 架构：

| 市场产品对象 | 现有 Curis 对象 | 招募/安装后的落点 |
| --- | --- | --- |
| 专家 | EmployeeTemplate | EmployeeInstance → 组织中心 |
| 技能 | SkillTemplate | Company Resource → Employee Skill Binding |
| 连接器 | Capability / Connector registry | 设置授权 → Company Resource → Employee/Workspace Binding |
| 专家团队 | 多个 Employee + Handoff/Workspace | Workspace 团队，不新建平级 Agent 对象 |

## 2. 首版用户路径

```text
打开人才市场
→ 搜索/分类
→ 选择专家
→ 右侧查看身份、职责、能力组合、来源和风险
→ 点击「招募」
→ 选择公司 / 岗位名称
→ 有合适部门时自动推荐，部门可不选
→ Curis 自动带入职责和默认 Skill 组合
→ 确认招募
→ 创建 EmployeeInstance
→ 写入 Skill Binding
→ 在组织中心看到员工
→ 从员工详情进入对话/工作入口（按招募上下文决定）
```

首版不要求用户安装十几个 Skill：专家模板自带默认 Skill 组合；只有 Company 资料、模型/Agent、连接器授权或岗位权限缺失时才显示补充项。Department 是可选组织归属，不是员工进入公司的前置条件。

招募最低门槛是 Company、Employee identity、Position/Responsibility、可用或明确缺口的执行能力，以及必要权限确认。Employee identity 的展示可包含可选 Avatar，支持上传、Curis 预置卡通头像或 fallback；头像不阻塞招募或员工创建。没有 Department 时，员工仍直接进入公司和组织中心；Business/Workspace 是否绑定由招募上下文决定。共享规则见 `docs/reviews/CURIS_AVATAR_IDENTITY_PATTERN.md`。

Skill 路径：

```text
发现 Skill → 查看来源/适用岗位/依赖 → 纳入公司资源
→ 选择员工 → PUT Employee Skill Bindings → 员工运行时读取 Skill excerpt
```

当前 Curis 的官方 Skill 已经是 Company 可见资源，因此首版将“安装”实现为对官方 Skill 的租户化纳入（幂等、保留 `created_from_template_id`），不把静态按钮当成安装完成。

Connector 路径：

```text
发现连接器 → 查看范围和权限 → 进入设置完成授权 → 健康检查
→ 成为 Company Resource → 分配员工/Workspace
```

首版市场展示现有 Connector registry 条目和真实 `mock/real` 模式；没有授权或健康证据时显示“待设置/未验证”，不显示“已连接”。

## 3. 页面与空间

沿用现有 Curis Desktop 壳层：固定一级侧栏、可折叠上下文侧栏、中央浏览区、按需右侧检查器。市场的通用交互参考 WorkBuddy 的成熟信息层级，不复制其品牌视觉、图片或专家内容。

### 左侧上下文栏

- 搜索
- 专家
- 技能
- 连接器
- 分类
- 已安装 / 已招募

### 中央工作区

- 页面标题：人才市场
- 专家/技能/连接器 Tab
- 分类筛选、搜索、排序
- 卡片列表
- 空态、加载态、错误态

### 右侧检查器

- 专家：身份、专业介绍、擅长领域、能帮用户做什么、能力标签、使用案例、来源/许可、招募动作
- 技能：说明、适用岗位、依赖、来源、许可、安装状态、分配员工
- 连接器：服务范围、数据方向、权限、授权状态、设置入口
- 招募装配：专家 → 岗位 → 职责 → Company →（可选）部门/业务/Workspace → 汇报关系 → 资料授权 → 能力检查 → 确认

## 4. 专家卡片与详情字段

专家卡片只展示发现所需信息：

- 名称 / 角色
- 一句话职责
- 适用场景
- 3–5 个能力标签
- 来源与许可证
- 状态：可招募 / 需要能力 / 暂不可用
- 主动作：招募

详情按渐进式披露展示：

1. 身份与职责
2. 擅长领域
3. 能帮用户做什么
4. 能力组合：Model/Agent、Skill、Tool、MCP、Knowledge、Connector、权限
5. 使用案例：来自模板定义，不冒充真实使用量
6. 质量信息：只有真实运行/结果数据存在时显示，否则隐藏

## 5. 首批专家

首版资源分为外部 Candidate 与 Curis 官方 EmployeeTemplate。外部 Candidate 优先来自 `agency-agents-zh`，首批选择 5 个与公司运行场景匹配的角色；Curis 同时保留 7 个官方 EmployeeTemplate 作为可运行兜底。

首条验收链路优先 5 个 Curis 模板：

| 专家 | 默认责任 | 首版来源 | 招募后 |
| --- | --- | --- | --- |
| 产品经理 | 需求理解、产品方向和优先级 | Curis `et_product_manager` | EmployeeInstance |
| 架构师 | 系统设计与技术决策 | Curis `et_architect` | EmployeeInstance |
| 后端工程师 | 服务与数据能力实现 | Curis `et_backend_engineer` | EmployeeInstance |
| 前端工程师 | UI 与交互实现 | Curis `et_frontend_engineer` | EmployeeInstance |
| QA 工程师 | 验证、回归和交付质量 | Curis `et_qa_engineer` | EmployeeInstance |
| DevOps 工程师 | 部署、监控和发布 | Curis `et_devops_engineer` | EmployeeInstance |
| Tech Lead | 研发协作和技术交付负责 | Curis `et_tech_lead` | EmployeeInstance |

这些是已有模板的市场化视图，不是批量新造低质量专家。Pilot B / CrewAI / 外部 Skill/MCP 在完成许可证、来源、安全和运行证据后作为后续资源上架。

## 6. 首版验收闭环

必须真实验证：

- 专家：发现 → 详情 → 招募 → EmployeeInstance → 组织中心可见。
- 装配：招募时使用模板默认职责；缺少 Company 时阻塞；没有 Department 时仍创建公司级员工，不创建半成品员工。
- Skill：发现 → 纳入公司资源 → 绑定员工 → 员工 Skill API 可读，运行时 `prompt_excerpt` 能读取其安全 excerpt。
- Connector：发现真实 registry 条目；未完成授权/健康时为待设置或未验证。
- 持久化：刷新/重启后员工与 Skill binding 仍存在；失败不产生孤儿绑定。

不把卡片、路由、静态数量、草稿模板、mock connector 或 API 200 当成业务完成。

## 7. 明确不做

- 不建立第二个 Admin 或 Platform 市场服务。
- 不复制 WorkBuddy/Coze 闭源专家、Prompt、图片或受保护数据。
- 不把“专家团队”新增为组织主对象。
- 不在首版加入市场计费、公开发布、评分造假、虚构使用量或自动授权。
- 不把外部 Agent API 调用伪装成 Curis 原生员工执行；外部来源必须保留 Adapter 和证据边界。

## 8. 当前实现状态

- 已实现：市场入口、专家/技能/连接器浏览与详情、Curis 模板读取、专家招募、默认 Skill 绑定、Skill 安装幂等接口。
- 已接入：`agency-agents-zh` / CrewAI 的公开角色 Candidate、OpenClaw/ClawHub Skill Adapter；资源仍必须经过来源、许可证、安全和运行门禁，不能把下载文件直接视为已上架专家。
- 部分完成：招募后的员工可进入现有组织数据；默认 Tool 仅在 Curis 官方能力可用时绑定，否则明确返回能力缺口。
- 尚缺：Workspace 归属、真实对话/工作运行、连接器授权与维护、外部 Candidate 的真实验证和发布；不能用页面存在或接口可调用替代。

## 9. 2026-08-14 第一版真实链路实现状态

### 已实现

- 专家市场把 Curis-ready 与外部 Candidate 分开呈现；Curis-ready 五个首批岗位可以从市场进入招募装配。
- 招募装配保持 Company、Employee identity、岗位/职责、模板执行来源、能力/权限检查为最低条件；Department、Business、Workspace 均不作为统一强制前置条件。
- 五个 Curis 模板的招募接口已验证：无 Department 仍创建 EmployeeInstance，默认 Skill Binding 持久化，组织中心可读取；默认 Tool 缺失时返回明确能力缺口。
- Skill 市场继续复用 55 个 active SkillTemplate：发现、详情、纳入公司资源、幂等安装、员工分配和员工详情中的 Skill/Tool Binding 展示均走现有 Runtime/API。
- 公开 `agency-agents-zh` 快照的五个角色已进入 Candidate 市场，来源状态、MIT 许可证、本地快照安全扫描和不可招募状态可见。

### 当前验收边界

- 员工“进入执行中心”使用现有 Curis Execution 入口；真正运行仍要求已有 Workspace/Project、模型和权限上下文。没有这些上下文时显示阻塞，不用聊天占位冒充工作完成。
- 外部 Candidate 需要固定版本、文件摘要、逐项安装验证后才可转为 Installable/Recruitable。
- Connector 授权/健康、真实 Coze Agent 调用和外部 Skill 远程安装仍未完成，不能用 mock 或 API 200 代替。

## 10. Phase 2 人才生产线

人才市场后台能力按成熟度区分资源，不把资源数量当成人才数量：

```text
DISCOVERED → CANDIDATE → COMPOSED → VALIDATED → CURIS_READY
                                      ↘ BLOCKED
```

生产线输出统一来源、许可证、安全扫描、Canonical Identity、去重摘要、职业分类和能力组合建议。前台默认优先 Curis-ready；Candidate 进入社区候选视图，BLOCKED 只在内部审核/诊断中显示。

当前扫描结果为 17 个外部 Agent Candidate、5 个 Skill Resource Candidate、5 个 MCP Resource Candidate；新增 Curis-ready 为 0。当前阶段不人工凑齐 20–30 个专家，先让真实来源完成组合和运行验证。

---

## 11. 2026-08-18 候选宇宙扩充（情报专项）

本轮「人才与能力情报负责人」对 52 个真实来源做了深度枚举，候选宇宙从 27 条扩展到去重后 ~250 条（候选包见 [`Curis_Talent_Candidate_Package_2026-08-18.md`](./Curis_Talent_Candidate_Package_2026-08-18.md)）。

### 11.1 分类覆盖（均已具备真实来源）
设计 ✓ / 产品 ✓ / 数据·BI ✓ / 研究 ✓ / Code Review·QA ✓ / 增长·营销 ✓ / 金融·财务 ✓ / 法律 ✓ / 科研·科学 ✓ / 教育 ✓ / 医疗 ✓ / 房地产 ✓ / 制造·供应链 ✓ / 咨询·行业研究 ✓。

### 11.2 对产品地图的影响
- 专家/技能/连接器三类分离原则不变；本轮新增候选严格按 `asset_kind = expert|skill|connector|mcp|tool` 登记，不与现有 Curis 模板混淆。
- 候选包中的集合型来源（alirezarezvani 362、K-Dense 135、ClawHub、anthropics/openai/obra）未来上架时须逐个生成卡片，不整仓批量进市场。
- 市场左侧上下文栏的「分类」维度可直接复用 §7 的 14 个行业分类，支持未来任意 Business 快速检索现成人才。
- 卡片与详情字段（§4）继续适用；新增候选一律显示 `CANDIDATE / 待验证`，不显示虚构使用量或质量分。
- 设计/产品/数据/BI/研究/法律/金融/教育/科研 等此前空薄的分类，本轮已有可导入真实候选，待 Codex 能力专项完成绑定与 Evidence 后转为可招募。
