# Curis · Workspace Engineering Product Translation — Review / Closure

**Status**: WORKSPACE ENGINEERING PRODUCT TRANSLATION · **APPROVED CANDIDATE**（设计候选已批准 · 待 P0 返回后 Technical Reality Delta Review）
**阶段**: PRODUCT / WORKSPACE DESIGN — Product Translation + Core Interaction / IA（承接《Workspace Engineering Product Handoff》）
**上位依据（只引用，不重定义）**:
- `CURIS_WORKSPACE_ENGINEERING_PRODUCT_HANDOFF.md`（Review · READY FOR PRODUCT TRANSLATION）
- `Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`（Frozen · P1–P7 · 四独立 Pane · 无 Global Topbar）
- `Curis_Company_OS_Shared_Authority.md` + `Curis_Content_Growth_Domain_Authority.md`（Frozen · M1 语义真相层）
- Content Growth 已收口三阶段：**Frozen Authority（语义真相）** / **UX/IA Exploration（体验探索）** / **Product Model Closure（产品模型收敛）**
- `WORKSPACE_PACKAGE_TECHNICAL_PROPOSAL.md`（TECHNICAL DIRECTION APPROVED CANDIDATE · **`NOT IMPLEMENTED`**）

---

## 1. 本轮交付物

| 文档 | 内容 | 状态 |
|---|---|---|
| `Curis_Workspace_Engineering_Product_Translation.md` | 主翻译文档：IA 总览 + 三条旅程(A新业务/B Template/C进化) CEO 体验 + Business Intent 入口 + Workspace Proposal(6答) + 4 决策点 + 激活 + 进化通知 + 失败/缺口卡 + §12.1 八问答 + Employee/Capability/Rules 进入 + 现在可确定 vs 等 P0 矩阵 + 禁重定义语义 | APPROVED CANDIDATE |

> 本轮**只做 Product Translation + Core Interaction / IA**，不进最终高保真、不产 HTML 结构稿（结构稿留待 VISUAL 阶段）。所有体验落点限定在 Frozen Shell + 允许 Surface 注册表 + Package Domain Schema 概念内。

---

## 2. 范围与纪律核查

| 纪律项 | 是否守住 | 说明 |
|---|---|---|
| 不重新研究业务方法 | ✅ | 直接消费 Handoff，不重做 Domain Research |
| 不重定义 Handoff 已裁定语义 | ✅ | §12 逐条引用 §12.2 裁定，未改名/未重解释 |
| 不暴露 Package/Gate/Router/Schema 等内部概念 | ✅ | §9 Q3 + §12 严禁清单；内部 Gate 不画成 UI（§5） |
| 不进入最终高保真 | ✅ | 仅 Translation + IA；无 Figma/像素/前端 |
| 不修改 Frozen Authority / Shell / P1–P7 | ✅ | 仅引用 |
| 不修改 Product Blueprint / XHS·RD Instance | ✅ | 未触碰 |
| 不开发 Runtime / Connector | ✅ | Package First 标注 `NOT IMPLEMENTED`，未假设已运行 |
| 不写正式前端 | ✅ | 仅 markdown 设计文档 |
| 复用 Content Growth 已落地用户面 | ✅ | Business Home 八问 / 三态 / Shared Employee Detail / 同一份方法 / 失败缺口卡 直接复用 |
| 不用「M1/M2/M3」简称 | ✅ | 全文写完整阶段名（Frozen Authority / UX-IA Exploration / Product Model Closure） |

---

## 3. 三条旅程翻译结论（CEO 体验要点）

- **A 新业务首次创建**：轻量表达经营意图 → 背景系统构建（CEO 不可见）→ 看 Workspace Proposal → 决策（意图确认 / 规则适配 / 激活）→ 投入运营。全程不配置内部机制。
- **B 已验证 Template 实例化**：选 Template → 填最少信息（经营方向名+主要目标+启用账号）→ 能力检查（复用已验证证据）→ Proposal → 激活。不重做领域研究。
- **C 已有 Workspace 进化**：空间「自己变好了」；轻量微调留痕可查、不需批准；仅结构性变更走 P7 决策包；未受影响上游证据复用。

---

## 4. 回答 Handoff §12.1 八问（结论汇总）

| 问题 | 结论 |
|---|---|
| Q1 Business Home 最少信息 / 防 Dashboard | 总览层 status-owner summary + activity timeline；业务层复用 CG 八问；指标只在 Evidence list 按需展开 |
| Q2 对话 vs 直接编辑 / 同一份方法 | 两者改同一底层经营方法，禁止两套存储 |
| Q3 复杂度隐藏 / 禁暴露原语 | 隐藏 Handoff §9 全部；需懂内部 Primitive 才能用=翻译失败 |
| Q4 三态自然表达 | 「默认按经营方式运行 / 这个账号单独设置 / 这次例外」pill |
| Q5 Employee 怎么工作可见 ≠ 后台配置 | Shared Employee Detail 内「工作方式」扩展（T5 裁定） |
| Q6 缺失 Capability 用户语言 | 按三分类自然语言（启用前需连接 X / 连接 X 后可用 Y / 可稍后连接 X 获得增强）；仅 Required for Activation 阻塞激活，不暴露 Primitive（主文档 §8.1） |
| Q7 失败/空/缺口卡对齐 Shell | 全部用 empty-failure-gap card Surface 三态 |
| Q8 Template 目标适配最少信息 | 经营方向名 + 主要目标(候选) + 启用账号(已连接) |

---

## 5. 现在可确定 vs 等 P0 Runtime 验证（摘要，详见主文档 §11）

**现在可确定**（落在 Frozen Shell + 允许 Surface + Package Domain Schema 概念内）：IA 布局、Surface 类型（9 种注册表）、内部概念隐藏、4 决策点语义、Proposal 6 答、三态表达、Employee 可见方式、Capability 缺口语言、进化通知、同一份方法、失败/空/缺口三态、Package First 思维。

**必须等 P0 Runtime 验证**（Handoff §11 禁止现在假设可行）：
1. 动态安装未知 Workspace（不改源码/不重建）；
2. 任意新 Surface 类型；
3. 自定义领域对象自动运行；
4. Capability 检查自动通过（权限 request，缺失即诚实呈现不静默降级；是否阻塞激活取决于产品三分类 §8.1，仅 Required for Activation 阻塞）；
5. 签名 / 市场 / 第三方信任；
6. 升级 / 迁移 / 回滚。

> 当前交付路径 = Instance Design → Gap Audit → bounded Issue → 改源码 → Rebuild；**不能冒充** Target Package Runtime。CEO 体验两层一致，但「能否自助上新业务」须 P0 用真实证据回答。

---

## 6. 停止状态

```text
WORKSPACE ENGINEERING PRODUCT TRANSLATION APPROVED CANDIDATE
```

（本文档与主翻译文档均为 **APPROVED CANDIDATE**；不进高保真；不修改任何 Frozen / Blueprint / Shell / P1–P7 / XHS·RD / Runtime / Connector / 代码 / UI；内部语义零重定义；§11.2 六项明确标注待 P0。本轮仅做一处产品语义修正：Capability Gap 三分类（Required for Activation / Required for Specific Action / Optional·Enhancement），用户侧仍只用自然语言、不暴露 Capability Primitive。暂不进入最终高保真；待 Workspace Engineering P0 返回真实 Runtime / PoC 结果后，做一次 **Technical Reality Delta Review**，再决定 Visual Design。）

---

*Curis Workspace Engineering Product Translation Review · APPROVED CANDIDATE（非 Frozen · 非高保真 · 非 Runtime · 非新架构）*
