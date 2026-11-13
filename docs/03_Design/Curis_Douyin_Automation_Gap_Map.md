# Curis 中国抖音自动化缺口地图（DOUYIN AUTOMATION GAP MAP）

**阶段**：DOUYIN END-TO-END AUTOMATION FEASIBILITY  
**状态**：DOUYIN END-TO-END AUTOMATION REVIEW REQUIRED  
**范围**：中国抖音（open.douyin.com）。TikTok 国际版不混入。  
**配套**：可行性文档（结论/等级）、能力矩阵（D/E/G）、打通条件（C/F/H）。  
**专家角色**：UiDesigner（研究，非开发）

> 七类缺口：Product / Connector / Runtime / Account / Platform / Policy / Tool。  
> 阻断标记：🔴 阻断 MVP / 🟠 阻断 FULL（MVP 可绕）/ 🟡 弱化体验。

---

## I. 缺口清单

### 1. Product Gap（产品层）
| Gap | 描述 | 阻断 | 备注 |
|-----|------|------|------|
| PG-1 | TTK Instance Spec 尚未批准（仍 REVIEW REQUIRED） | 🔴 | 无 Video / Script / Analytics 运行时对象模型；必须先批准 Instance 才能落地 |
| PG-2 | 发布前人工审核门禁 UI 未定义 | 🔴 | 政策强制点，必须在产品里体现（A1 门禁） |
| PG-3 | AIGC 披露 UI / 运行时未定义 | 🟠 | 合规强制，FULL 前必须有 |
| PG-4 | Engagement 三档路由 UI 未定义 | 🟡 | 评论/私信 AUTO_REPLY/EMPLOYEE_REVIEW/CEO_DECISION 需产品承载 |

### 2. Connector Gap（连接器层）
| Gap | 描述 | 阻断 | 备注 |
|-----|------|------|------|
| CG-1 | 抖音 Publishing Connector 未建 | 🔴 | 封装 upload/create_video + Webhook 回执 |
| CG-2 | 抖音 Engagement Connector 未建 | 🔴 | 评论/私信拉取 + 三档路由 + 越权 fail-closed |
| CG-3 | 抖音 Analytics Connector 未建 | 🔴 | /video/data/ + 经营号深度数据接入 |
| CG-4 | 生产工具连接器未接（CapCut/即梦/可灵/HeyGen/Runway） | 🔴 | 五者均未接入运行时 |

### 3. Runtime Gap（运行时层）
| Gap | 描述 | 阻断 | 备注 |
|-----|------|------|------|
| RG-1 | 无定时发布调度器 | 🟠 | 官方 A5 → 需「到点即时发布」变通或等官方能力 |
| RG-2 | 无完播率数据摄取路径 | 🟠 | 需经营号授权 + 小程序层（Account Gap 联动） |
| RG-3 | 无 Webhook 事件处理器（create_video/authorize/receive_msg） | 🔴 | 回执/授权状态机缺失 |
| RG-4 | 无 AIGC 标识运行时 | 🟠 | 合规强制 |

### 4. Account Gap（账号/资质层）
| Gap | 描述 | 阻断 | 备注 |
|-----|------|------|------|
| AG-1 | 无企业开发者账号 + 已审应用 | 🔴 | 一切官方能力前提 |
| AG-2 | 无 Scope 授权（video.create.bind/comment/data/data.bind/im） | 🔴 | 需逐个申请 |
| AG-3 | 无企业号认证 | 🟠 | 评论置顶/私信 receive_msg/经营号数据依赖 |
| AG-4 | 无经营抖音号授权（完播率） | 🟠 | FULL 需；MVP 可先用计数 |
| AG-5 | 无生产工具 API Key/订阅 | 🔴 | CapCut 本机 / 即梦 AK/SK / 可灵 / HeyGen / Runway Enterprise |

### 5. Platform Gap（平台能力层 · 官方事实）
| Gap | 描述 | 阻断 | 备注 |
|-----|------|------|------|
| PL-1 | 官方 `create_video` **无定时发布参数** | 🟠 | A5；仅 TikTok 国际版第三方有 |
| PL-2 | 完播率仅小程序经营号授权层；OpenAPI 层仅计数 | 🟠 | 深度指标需经营号 |
| PL-3 | 评论**只能回复自己视频** | 🟡 | Connector 必须越权 fail-closed |
| PL-4 | 私信 `receive_msg` **仅企业号** | 🟡 | 个人号无接收能力 |
| PL-5 | 2 秒跳出 / 平均观看时长官方 API 未确认 | 🟡 | UNK，待连接验证 |
| PL-6 | 数据时效：首授权次日才全；视频数据限 30 天 | 🟡 | 反馈环需容错 |

### 6. Policy Gap（政策/法规层）
| Gap | 描述 | 阻断 | 备注 |
|-----|------|------|------|
| PO-1 | **抖音严打「AI 托管类账号」，全自动托管 = 封禁** | 🔴（FULL 根因） | 仅「AI 辅助 + 人工审核发布」安全 → FULL 不可达 |
| PO-2 | AIGC 披露强制（网信办 6 类标签 + 抖音 AIGC 规范） | 🟠 | 生成内容须标识 |
| PO-3 | 广告法 / 版权 / 平台政策合规 | 🟠 | 触发 CEO_DECISION（P7） |

### 7. Tool Gap（生产工具层）
| Gap | 描述 | 阻断 | 备注 |
|-----|------|------|------|
| TG-1 | CapCut = 草稿生成器，非云端渲染 | 🟡 | 生成草稿后需桌面端导入渲染（A1+A4） |
| TG-2 | Runway API 仅 Enterprise（~$800/月） | 🟡 | 成本/订阅门槛 |
| TG-3 | HeyGen 成本高（Avatar IV ~$10K–20K/月） | 🟡 | 数字人需披露 |
| TG-4 | 即梦/可灵 一致性丢弃率 20–40% | 🟡 | 生成片段需人工/审核筛除 |

---

## 缺口优先级（MVP 路径）

**MVP 必须清除（🔴）**：PG-1/2、CG-1/2/3/4、RG-3、AG-1/2/5、PO-1（用 A1 门禁规避）。
**MVP 可绕（🟠）**：RG-1（即时发布变通）、RG-2/4（先计数）、AG-3/4（先企业号基础 + 后续经营号）、PO-2/3（披露 + P7）。
**体验弱化（🟡）**：PL-3/4/5/6、TG-1~4——fail-closed 或后续优化。

**FULL 升级额外必须**：PL-1 官方定时发布（或变通成熟）、RG-2 完播率通路、AG-4 经营号、PO 政策放宽无人值守判定。

---

**状态**：DOUYIN END-TO-END AUTOMATION REVIEW REQUIRED  
**UI Designer** · 2026-08-15 · RESEARCH ONLY
