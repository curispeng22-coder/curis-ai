# Curis Professional Workspace Quality Model Candidate

Status: Review

Authority Class: RESEARCH / PRODUCT QUALITY CANDIDATE

Disposition: READY FOR CEO REVIEW

Date: 2026-08-22

Implementation: Not authorized

---

## 1. Purpose

本模型防止四个词被混用：Professional、Verified、Generated、Generic。

```text
Professional = 产品深度
Verified     = 证据状态
Generated    = 产生方式
Generic      = 产品形态
```

它们不是同一条单轴等级。

## 2. Professional

Professional Workspace 指针对稳定 Domain / Operating Problem 形成的专业 Domain Application，通常包含：

- Domain / Operating Model；
- Professional IA 与 Multi-Surface UX；
- Specialized View / Detail / Editor / Tool；
- Responsibility / Capability / Method；
- Evaluation / Value Semantics；
- Domain-specific failure and provider boundaries。

“Professional”不自动表示已验证。一个产品设计完整但没有真实 E2E、Desktop、migration 或 Provider evidence 的 Workspace，应称为 `Professional Candidate`。

## 3. Verified

Verified 是证据状态。它表示某个明确版本、适用范围和能力边界通过了规定验证，不表示永远正确，也不表示所有 Optional Capability 都可用。

Verified 必须带：

- Package / Workspace version；
- verified scope；
- evidence date；
- publisher / maintainer；
- required connections and permissions；
- provider and platform boundaries；
- known gaps；
- migration / support policy。

不能单凭以下事实获得 Verified：

- Package 能安装；
- 页面能打开；
- Runtime API 返回 200；
- 有设计稿；
- 有 Domain Research；
- 某个模块独立通过测试；
- 使用 Official publisher。

## 4. Generated

Generated 描述产生方式：内容、配置、IA、Surface 或 Package Candidate 由 AI / Workspace Engineering 在当前请求中生成。

Generated 可以未来通过验证成为 Verified，但在验证前必须标为 Candidate。它的默认边界是：

- 假设和证据可见；
- UX 未验证；
- Domain gaps 明确；
- 外部副作用收紧；
- 自动化更保守；
- CEO / specialist review required。

Generated 不是贬义，也不是“自动失败”；它只是不能借生成速度冒充验证质量。

## 5. Generic

Generic Workspace 是使用通用 Object、View、Work、Responsibility、Artifact、Result、Evidence 与 Company OS projection 形成的经营环境。

Generic 可以是稳定、可靠、长期使用的产品，但它不承诺已经编码某行业的最佳 IA、Specialized UX、Evaluation 或 Value Semantics。

Generic 的质量评价重点是：

- 数据与身份真实；
- 责任与权限正确；
- Work / Result / Evidence 可追溯；
- failure / unknown / gap 诚实；
- 可配置但不要求用户成为系统工程师；
- 可原地升级。

## 6. Three-axis Quality Model

### 6.1 Product Form

| 值 | 含义 |
|---|---|
| Professional | Domain-specific application with professional semantics and UX |
| Generic | General operating environment using shared objects and views |

### 6.2 Provenance

| 值 | 含义 |
|---|---|
| Curis Official | Curis 维护并承担版本责任 |
| Verified Partner | 经 Curis 规则验证的合作维护者 |
| Community | 第三方发布，验证范围需单独说明 |
| User / AI Generated | 用户或 AI 在当前 Company context 中生成 |

### 6.3 Assurance

| 值 | 可对用户说什么 | 不可说什么 |
|---|---|---|
| Verified | 明确版本和范围已通过专业、运行与演进验证 | 所有连接可用、所有场景无风险 |
| Candidate | 方向或功能候选已形成，仍需指定验证 | 已适合关键生产经营 |
| Unverified | 尚无足够证据 | 专业可靠、自动化安全 |
| Deprecated | 保留读取 / 迁移，停止作为新建推荐 | 当前推荐方案 |

## 7. Verification Domains

| 验证域 | Professional Verified 要求 | Generic Verified 要求 |
|---|---|---|
| Domain research | 必须，且关键结论可追溯 | 可选；必须明确未知 Domain boundary |
| Object / semantic model | 专业分类与状态稳定 | 通用对象 schema 正确、限制透明 |
| Operating / responsibility model | 必须形成专业责任与 Handoff | 通用 responsibility / assignment 正确 |
| Professional IA / UX | 必须，多 Surface 与 specialized interaction 通过验证 | 通用 view / detail / work 体验通过验证 |
| Capability / provider | 专业能力、权限、失败和副作用边界 | 已配置 capability 真实；缺口 fail-closed |
| Evaluation / value | 必须，能说明什么算有效和值得继续 | 可以是用户定义目标，但不得伪装行业标准 |
| Domain E2E | 必须至少一条真实链 | 必须证明真实 Work / Result / Evidence 闭环 |
| Desktop / responsive | 必须按适用设备验证 | 必须按通用产品支持范围验证 |
| Version / migration | 必须保护对象、running Work 与 history | 必须保护通用对象、identity 与 history |
| Stewardship | 必须有维护者和支持范围 | 必须有 Core owner 和 deprecation policy |

## 8. User-facing Trust Levels

面向普通用户可以压缩为以下候选表达：

| 显示 | 含义 | 示例说明 |
|---|---|---|
| 专业验证 | Professional + Verified | “小红书专业经营 v1.2；已验证研究、内容、增长主链；发布连接需单独授权。” |
| 专业候选 | Professional + Candidate | “专业结构已设计，真实 Domain E2E 尚未完成。” |
| 通用可靠 | Generic + Verified | “通用经营环境；数据、责任、恢复已验证，不代表行业最佳实践。” |
| AI 生成候选 | Generated + Candidate / Unverified | “由当前目标生成；需审查专业结构、能力与风险。” |
| 已停止推荐 | Deprecated | “历史可读；请迁移到受支持版本。” |

Publisher 可作为第二标签显示，例如“Curis 官方”“合作方”“社区”，不能替代质量标签。

## 9. Verification Inheritance Rules

### 9.1 Instance Configuration

如果变化只属于合同允许的名称、目标、品牌语气、账号连接、Team、规则或 Optional Module 开关，可继承 Package 的产品验证；实例仍需通过 capability、permission、connection、scope 与 data validation。

### 9.2 Derived Package

Derived 只能继承未受影响的 Base evidence。新增对象、状态、Surface、Specialized UX、Provider boundary、Evaluation 或 migration 必须验证 delta，并完成回归。

### 9.3 Composed Workspace

Module verification 不自动合并。组合后必须重新验证：

- one Workspace / one accountable Team boundary；
- navigation and IA coherence；
- object identity and cross-module references；
- Responsibility / Handoff；
- capability conflicts；
- evaluation / value conflicts；
- combined Domain E2E；
- upgrade compatibility。

### 9.4 Generated Candidate

Generated 没有继承验证，除非它仅选择并配置未修改的 Verified assets。任何生成的 semantic、interaction、condition、method 或 evaluation 都保持 Candidate，直到通过相应 Gate。

## 10. Downgrade Rules

以下变化应使相关范围从 Verified 降为 Candidate / Unverified，直到重新验证：

- Package digest 或关键 contract 未知变化；
- Specialized View / Action 改变业务语义；
- Provider API / permission / platform policy 发生重大变化；
- Evaluation / Value Semantics 改变；
- migration 无法证明历史与 running Work 安全；
- maintainer 或签名失效；
- 已验证 Domain E2E 不再可复现；
- 必需 Capability 变为 unavailable / stale / unauthorized。

Capability 暂时不可用可以让某个 Surface / Action 降为 Gap，不必把整个 Workspace 永久降级；用户必须能看见影响范围。

## 11. Current Curis Classification Snapshot

| 资产 | 当前最诚实分类 | 原因 |
|---|---|---|
| Multi-Surface Package v2 substrate | Generic technical substrate — Implemented / Accepted | 已证明 navigation、Surface registry、routing、resolution、projection、restart；未证明完整 Domain 专业质量 |
| AI 科技 / XHS model | Professional Candidate | Domain Research、Authority reconciliation 与 UX candidate 已形成；XHS migration、真实 Domain E2E、完整 provider boundaries 未完成 |
| RD Workspace Instance | Professional Candidate / Approved Instance Spec | RD specialized UX 与 responsibility semantics 已明确；最终 Multi-Surface migration 与完整产品验证仍缺 |
| Customer Feedback proof Package | Generic verified proof scope | 证明 bounded Package / Company OS integration，不等于行业 Professional Verified |
| 未知业务现场生成 Workspace | Generated Candidate 或 Generic | 取决于是否只用受验证通用组件；不能标 Professional Verified |

本快照是 Research interpretation，不修改 Current Authority 或 Implementation State。

## 12. Claims Policy

允许的产品文案：

- “经过专业验证的小红书经营工作空间”；前提是对应版本确实完成全部验证。
- “基于已验证模块组合”；同时说明整体组合验证状态。
- “通用经营工作空间”；说明它可配置、可运行、可升级。
- “AI 生成候选”；说明需审查和能力缺口。

禁止的产品文案：

- “安装成功，所以已专业验证”；
- “Curis 官方，所以已验证”；
- “使用专业模块，所以整体已验证”；
- “AI 已理解任何行业”；
- “Connector 已列出，所以真实可用”；
- “有数据页面，所以已具备 Evaluation / Value Semantics”。

## 13. Verification Record Candidate

未来每个 Verified Workspace 的可展开记录至少包含：

```text
Workspace / Package name and version
Product form
Publisher / maintainer
Assurance status
Verified domain and operating scope
Verified Surfaces / Modules
Required capabilities / connections
Provider and permission boundaries
Domain E2E evidence
Desktop / device evidence
Migration / rollback evidence
Known gaps and unavailable capabilities
Evidence date / expiry / revalidation trigger
```

本节只定义信息责任，不定义 Schema 或 UI。

## 14. Decision Candidate

建议 CEO 接受以下语义原则：

1. Professional、Verified、Generated、Generic 四词分开使用。
2. Verified 必须绑定版本、范围、证据和维护者。
3. Official / Community 只表示来源，不代替验证。
4. Module 验证不自动等于组合后的 Workspace 验证。
5. Generated 默认是 Candidate，不得自动获得 Professional 或 Verified 承诺。
6. Generic 可以可靠和长期使用，但必须诚实说明不等于专业行业产品。
7. 任何层都继续复用同一 Company OS / Autonomous Core。

## 15. Non-goals

本 Candidate 不修改产品文案、Badge、Package Contract、Schema、Runtime、Frontend、Template Library 或 Marketplace，也不授予任何 Workspace Verified 状态。

STOP FOR CEO REVIEW.
