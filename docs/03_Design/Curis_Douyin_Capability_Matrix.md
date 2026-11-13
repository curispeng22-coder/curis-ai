# Curis 中国抖音自动化能力矩阵（DOUYIN CAPABILITY MATRIX）

**阶段**：DOUYIN END-TO-END AUTOMATION FEASIBILITY  
**状态**：DOUYIN END-TO-END AUTOMATION REVIEW REQUIRED  
**范围**：中国抖音（open.douyin.com）。TikTok 国际版不混入。  
**配套**：`Curis_Douyin_End_to_End_Automation_Feasibility.md`（结论/等级/缺口）、`Curis_Douyin_Automation_Requirements.md`（打通条件/反馈环）、`Curis_Douyin_Automation_Gap_Map.md`（缺口地图）。  
**专家角色**：UiDesigner（研究，非开发）

> 等级代码见可行性文档 §0：A0 全自 / A1 自动+审核 / A2 人在环 / A3 CEO决策 / A4 工具辅助手工 / A5 官方无能力 / A6 政策禁止。

---

## D. Publishing Connector 能力矩阵（内容发布）

| 能力 | 官方 API | Scope | 自动化等级 | 缺口/限制 |
|------|----------|-------|-----------|-----------|
| 上传视频文件 | `upload_video` | `video.create.bind` | A1（审核后触发） | 需申请权限 + 用户授权 |
| 创建视频（发布） | `create_video` | `video.create.bind` | A1（审核后触发） | 平台审核期仅自己可见 |
| 话题 / @用户 / 小程序 / POI 锚点 | `create_video` 参数 | `video.create.bind` | A1 | 随发布一并提交 |
| 删除视频 | 官方有 | — | A1 | — |
| 查看审核状态 | 官方有 | — | A0 | Webhook `create_video` 事件回执 |
| 发布回执 | Webhook `create_video` | — | A0 | 需配置回调 + 订阅 |
| **定时发布** | **官方 `create_video` 无 schedule_time** | — | **A5** | 仅 TikTok 国际版第三方工具有；中国抖音官方缺 |
| 视频规格 | 16:9 / 720p+ / mp4·webm / ≤4G / ≤15min | — | — | 硬限制 |

**Connector 设计含义**：
- Publishing Connector 封装 `upload_video` → `create_video` → Webhook 回执，但**必须在调用前嵌入 A1 人工审核门禁**（政策强制，见可行性 §H）。
- 定时发布：Connector 可内部「排期计划」（A1 计划），但**到点必须由人/轻量确认触发即时发布**（因 A5），或待官方能力开放。

---

## E. Engagement Connector 能力矩阵（评论 / 私信）

> 用户要求：评论/私信分类为 **AUTO_REPLY / EMPLOYEE_REVIEW / CEO_DECISION**，且 **CEO 不能逐条审批评论**。

### E1. 评论（Comment）
| 项目 | 官方事实 |
|------|----------|
| Scope | `video.comment`（需「互动管理」权限） |
| 接口 | `videoCommentListGet` / `videoCommentReplyListGet` / `videoCommentReplyPost` / `videoCommentTopPost`（置顶仅企业号） |
| **硬限制** | **只能回复授权用户自己发布的视频** |
| 自动化等级 | A1（回复可自动，但需审核策略） |

**分类路由（三档，CEO 不逐条审批）**：
| 类别 | 触发 | 处理 | 等级 |
|------|------|------|------|
| AUTO_REPLY | FAQ / 常规提问 / 关键词命中知识库 | AI 自动回复（可带人工抽检） | A1 |
| EMPLOYEE_REVIEW | 品牌相关 / 负面情绪 / 需斟酌措辞 / 疑似舆情 | 路由内容审核/发布运营员工复核后回 | A2 |
| CEO_DECISION | 涉及对外承诺 / 商务合作 / 重大舆情风险 | 触发 P7 CEO Decision（**非逐条**，仅升级事件） | A3 |

### E2. 私信（Direct Message）
| 项目 | 官方事实 |
|------|----------|
| Scope | `im.direct_message` 等（需用户授权） |
| 接收事件 | `receive_msg` **要求当前抖音用户是企业号** |
| Webhook | 需配置回调 + 订阅 `receive_msg`(enterprise.im) / `enter_im` |

**分类路由（同三档）**：
| 类别 | 触发 | 处理 | 等级 |
|------|------|------|------|
| AUTO_REPLY | 关键词 / 常见咨询 | AI 自动回复 | A1 |
| EMPLOYEE_REVIEW | 订单/客诉/需人工判断 | 路由员工复核 | A2 |
| CEO_DECISION | 商务合作 / 重大承诺 / 风险 | P7 CEO（仅升级事件） | A3 |

**Engagement Connector 设计含义**：
- 评论/私信的**自动回复**是 A1（可自动），但敏感/品牌/舆情走 EMPLOYEE_REVIEW（A2），仅升级事件走 CEO_DECISION（A3）。
- **CEO 绝不为每条评论/私信做审批**——这是 Frozen P7「高风险才打断 CEO」原则的直接应用。
- 范围硬限制（评论仅自己视频、私信仅企业号）必须在 Connector 内 fail-closed：越权请求直接拒，不伪造。

---

## G. 生产自动化工具矩阵（程序化可调用，Tool Capability ≠ Employee Responsibility）

| 工具 | 官方调用方式 | 能力 | 账号/成本依赖 | 自动化等级 | 关键限制 |
|------|--------------|------|---------------|-----------|----------|
| **CapCut / 剪映** | CapCutAPI（开源，HTTP REST :9001 + MCP 11 tools） | 直接操作剪映/JianYing 草稿文件（dfd_ 文件夹），生成草稿导入桌面端渲染导出 | 本机安装剪映桌面端 | A1（生成草稿）+ A4（渲染需桌面导入） | **= 草稿生成器，非云端渲染服务**；15min 限制 |
| **即梦 Jimeng** | 火山视觉 API `visual.volcengineapi.com`（`CVSync2AsyncSubmitTask` / `GetResult`） | 文生/图生视频、分镜、视觉素材 | Volcengine AK/SK | A1（生成 + 版权/披露复核） | 异步提交 + 轮询；一致性丢弃率 20–40% |
| **可灵 Kling** | Volcengine(dashscope) / 腾讯 TokenHub / kling.ai API | 文生/图生/Omni 视频 | AK/SK 或 Bearer Key + 订阅 | A1 | 异步提交 + 轮询 |
| **HeyGen** | 官方 MCP（5+ tools，stdio + remote OAuth） | 数字人 Avatar 视频 | API 按量计费；Avatar IV 约 $10K–20K/月 | A1 | 成本高；数字人需披露 |
| **Runway** | 官方 MCP，Gen-4.5 | 文生/图生视频、高级编辑 | **API 仅 Enterprise（约 $800/月 5 seats）** | A1 | 企业订阅门槛 |

**统一结论（TOOL）**：
- 五类工具均满足「API/MCP/SDK 可程序化调用、需账号/Key/订阅、结果轮询/webhook/URL 回收、可自动继续」→ 生产自动化在**工具层可达 A1**。
- 但均为 **Tool Capability（执行）**，不是 Employee Responsibility：制作员工的「方向/审美/成片判断/版权/披露」责任不随工具升格（继承首轮 Proposal §E + Reuse Matrix #5）。
- CapCut **非渲染服务**——生成草稿后仍需桌面端导入渲染导出，是 A1+A4 混合，不能当作「云端一键成片」。

---

**状态**：DOUYIN END-TO-END AUTOMATION REVIEW REQUIRED  
**UI Designer** · 2026-08-15 · RESEARCH ONLY
