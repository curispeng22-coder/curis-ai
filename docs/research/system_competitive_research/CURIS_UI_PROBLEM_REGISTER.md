# CURIS UI PROBLEM REGISTER

> Authority Class: RESEARCH / EVIDENCE
> Status: v1 COMPLETE（来源：CURIS_CURRENT_UI_AUDIT.md §0–§14；修复责任归属仅到"应进入 Final UI Master 的哪个工作流"，不派发代码任务）
> Date: 2026-09-12
> 分级定义：P0 Directional（方向性错误，不动摇结构但决定产品观感）/ P1 Structural（结构性缺陷，影响可用与完整）/ P2 Polish（打磨）。
> 边界：所有条目均为 UI / Interaction 层；不推翻 Frozen Product Structure。

## A. 全局系统性问题（跨页）

| ID | 级别 | 问题 | 证据 | 影响 | 修复方向（输入 Final UI Master） |
|---|---|---|---|---|---|
| G-01 | P0 | 视觉身份碎片化：`#32f08c`（前端 frozen token）/ `#806BE5`（Visual Standard V1 + 内联样式）/ 黑+绿（A 代原型）/ 黑+中性（B 代）并存 | UI AUDIT §0-S1、EVIDENCE CATALOG §1 | 产品没有可识别的脸；任何新页面都在加深分裂 | Final UI Master 先做唯一 token 层裁决（ accent、中性阶、状态色、深浅色），再谈页面 |
| G-02 | P0 | 已废弃"办公室"模型仍流通于 A 代原型整套资产 | UI AUDIT §0-S2 | 与 08-24 CEO 裁决冲突；误导设计研究 | 将 A 代资产标记 HISTORY / VISUAL REFERENCE ONLY，Pointer 登记 |
| G-03 | P0 | 四套 IA 并存（A 代侧栏 / B 代七区 / C 代真实前端 4 项+更多 / Figma 基线） | UI AUDIT §0-S3、§13-C6 | "当前 UI 是什么"无法回答 | 以 Structure Baseline 七区为唯一 IA 收敛，其余资产降级 |
| G-04 | P0 | 空状态范式 = 零值统计仪表盘 | UI AUDIT §0-S4、§2、§3、§6、§7、§13-C3 | first-run 与新公司体验是"空报表"，不是"公司等你启动" | 空态规范：单一主行动 + 一句叙事 + 每区专属空态插画/结构 |
| G-05 | P0 | 网页后台语汇（统计卡联排/tab 计数/表单卡）代替桌面对象语汇 | UI AUDIT §0-S5 | 像 SaaS 后台，不像桌面 AI 公司 OS | 引入对象卡/活动流/密度层级等桌面语言（见 PATTERN LIBRARY） |
| G-06 | P1 | 无全局搜索 / ⌘K / 命令面 | UI AUDIT §1、GAP MATRIX Global Search 行 | 七区+全对象导航只能靠侧栏 | Global Object Search P1 与命令面合并设计 |
| G-07 | P1 | 实现细节泄漏为用户文案：SimulationRun、Company Runtime、--ui-* token 注释、aware 机制、模型名/工具清单/¥0.18 | UI AUDIT §4、§9、§13-C1/C5 | 用户语言缺失（CURRENT_STATE P1 同源） | 建立用户语言映射表（Capability 用户语言 P1 的一部分） |
| G-08 | P1 | 状态词汇与色彩语义不统一（制作中/进行中；装修中；等待启动误用告警色） | UI AUDIT §3、§4、§7 | 状态不可信 | 统一状态机词典 + 状态色规范 |
| G-09 | P1 | 助理/员工对话无结构化回复与成熟 Composer | UI AUDIT §9、§13-C3/C4 | "工作伴侣"呈现为文本堆+迷你报表 | Composer/回复卡规范（见 PATTERN LIBRARY） |
| G-10 | P2 | 深色模式仅 A 代有且 accent 错误；1024/无障碍无证据 | UI AUDIT §10、GAP MATRIX | 打包债务 | Final UI Master 含 Dark/1024 适配规范 |

## B. 分页面问题（按区）

| 区 | ID | 级别 | 问题 |
|---|---|---|---|
| CEO 工作台 | P-CEO-01 | P0 | 视觉重心错误：空态六维度"等待启动"重复六遍占半屏；最大 CTA 与页面任务错位（A 代） |
| CEO 工作台 | P-CEO-02 | P1 | 顶部 meta 文字条 5 组状态纯文本平铺，无层级 |
| CEO 工作台 | P-CEO-03 | P1 | 三个"等待"框同质堆叠，无注意力优先级 |
| CEO 工作台 | P-CEO-04 | P0 | 真实前端助理默认标题"未命名 Assistant/尚未设置角色"直接可见（C2） |
| 业务空间/门户 | P-BIZ-01 | P0 | 四联 0 值统计卡占据黄金位 |
| 业务空间/门户 | P-BIZ-02 | P1 | 双/三重空态重复且 CTA 文案不一致 |
| 专业工作区 | P-WS-01 | P1 | Utility 打开时面包屑折叠换行、与 Surface tabs 挤压 |
| 专业工作区 | P-WS-02 | P1 | Utility 面板元数据缺失（负责人/状态/版本/证据/时间） |
| 专业工作区 | P-WS-03 | P1 | 交接 chip 可点性不可辨；行内 chip 三连（类型+人+状态）密度过载 |
| 专业工作区 | P-WS-04 | P1 | Employee Quick Panel 很好，但"打开完整员工工作站"目标页不存在证据（断层面） |
| 专业工作区 | P-WS-05 | P0 | A 代 workspace-runtime 是单列长滚动 dashboard，与 Frozen Four-Pane Shell 冲突（资产代际问题） |
| 会议 | P-MTG-01 | P0 | 会议页最大 CTA 是"创建公司"，层级错误（A 代） |
| 会议 | P-MTG-02 | P1 | 与已验收 Figma 214 基线不同体系（资产代际问题） |
| 资料库 | P-KNW-01 | P1 | 空库四联统计卡占首屏；左右栏密度失衡 |
| 资料库 | P-KNW-02 | P1 | 与已验收 Figma 187 基线不同体系（A 代资产） |
| 经营洞察 | P-OPS-01 | P0 | 公司脉搏 6 卡同文案重复；空态风险维度误用告警色 |
| 经营洞察 | P-OPS-02 | P1 | 与已验收 Figma 172 基线不同体系（A 代资产） |
| 人才与能力 | P-TAL-01 | P0 | 全资产无一张 Expert/Marketplace/Employee Detail 界面（脸面缺位） |
| 全局助理 | P-AST-01 | P1 | 面板内 Composer 不可见/缺位（B 代）；面板=报表+表单（C 代） |
| Settings | P-SET-01 | P1 | 真实 Settings 仅公司档案本地草稿；模型/员工/权限/隐私/数据全缺；开发者注释入 UI（C5） |
| 错误态 | P-ERR-01 | P1 | 全屏裸错误 + 英文 "Failed to fetch"，无解释无路径（C8） |
| 侧栏 | P-NAV-01 | P2 | 标语重复占位；图标平铺无折叠；选中/hover 区分弱 |

## C. 处置说明

- 标"资产代际问题"的条目（P-WS-05、P-MTG-02、P-KNW-02、P-OPS-01 部分、G-02/G-03）的正确处置**不是重画**，而是：① 在 Pointer/EVIDENCE CATALOG 中标记资产代际与效力；② Final UI Master 以已验收 Figma 基线 + B 代结构 + 冻结 token 重建。
- 其余条目应整体进入 `CURIS_DESKTOP_PRODUCT_AND_DESIGN_DIRECTION.md` 的设计要求清单。
