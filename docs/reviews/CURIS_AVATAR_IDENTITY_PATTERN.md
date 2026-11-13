# CURIS AVATAR IDENTITY PATTERN

**Status:** Review
**Authority Class:** REVIEW / PRODUCT + UI IDENTITY PATTERN
**Disposition:** READY FOR CEO / CHATGPT REVIEW
**Scope:** CEO 与 AI Employee 的共享头像展示规则；不新增身份、Profile、Runtime 或资源系统

## 1. Pattern boundary

CEO 与 AI Employee 共用同一 `CURIS AVATAR PATTERN`。头像属于 Identity / Presentation，只帮助识别和形成 Company / Team presence；不改变 Company、Employee、Role、Responsibility、Capability、Model、Provider、Agent runtime、Execution、Conversation history 或权限语义。

头像可替换，不因更换头像重建身份、责任、绑定、历史或运行状态。

## 2. Shared creation pattern

| Stage | Rule |
| --- | --- |
| Upload | 支持常见图片格式；创建后统一裁剪为头像比例；不要求真人照片或社交账号 |
| Preset | 使用 Curis 自有卡通头像集；简洁、现代、可辨识、不幼稚、不夸张；建议 8–12 个基础头像，最终数量与艺术细节由后续 Visual Design 确定 |
| Fallback | 用户跳过时使用名字首字母或系统默认卡通头像；具体策略复用现有实现能力 |
| Display | 所有页面消费同一身份头像来源；尺寸/裁切由 UI 组件处理 |
| Update | CEO / Employee 后续均可从现有 Profile、头像菜单或人才相关入口更换 |

Avatar 是可选项，不是 CEO、Company 或 Employee 创建门槛。Employee 创建不依赖头像；缺失时必须自动 fallback。

## 3. Identity fields

- CEO Display Identity 至少包括 `Display Name` 与可选 `Avatar`。
- Employee Display Identity 至少包括 `Employee Name` 与可选 `Avatar`。
- CEO 与 Employee 不建立两套头像机制；不新增 `Profile V2`、`Identity V2` 或 `Avatar Service V2`。

## 4. Display surfaces

CEO：左下角 CEO 区域、CEO Avatar Menu、Conversation、Decision、Meeting 与 Company-level interaction。
Employee：Employee Conversation、Work Owner、Responsibility Holder、Team / Organization、Meeting、Result / Handoff ownership 与 Employee Workstation。

这些位置只读取同一 Identity truth；头像不代表完成、在线、能力已验证或执行成功。

## 5. Preset visual boundary

预置资源应形成统一 Curis Cartoon Avatar Set，覆盖适度的发型、穿着、面部特征与气质差异，但不把头像选择做成人口属性表单。禁止明星、写实人脸库、儿童卡通、Meme、过度二次元和风格混杂。具体艺术风格仍由 Visual Design 决定，本文件不冻结像素或资源文件。

## 6. Current implementation audit

| Area | Classification | Evidence / boundary |
| --- | --- | --- |
| CEO Display Name / identity | EXISTS / REUSE | 现有 App Entry 与 CEO Identity 合同已定义 Display Name；头像尚未在该合同中统一定义 |
| Employee identity / Profile | EXISTS / REUSE | 现有人才与 Employee Profile 语义承载名称、岗位、责任与绑定；不新增身份对象 |
| Avatar presentation | PARTIAL | `assistant_identities.avatar` 与 Assistant 状态已有轻量头像字段/入口；`persona_templates.image_ref_json` 也可承载模板形象，但未确认其满足 CEO/Employee 统一上传、预置、裁剪与跨页面真源 |
| Employee avatar persistence / preset assets / crop | IMPLEMENTATION GAP | 当前 `employee_instances` 没有统一 Avatar 字段或资源目录；头像上传、预置资产、裁剪、持久化与跨页面 Identity truth 仍需独立 Issue 与真实证据确认 |

以上是实现审计，不把目标体验写成已交付事实；本轮不修改 Runtime、Schema、DB、Frontend 或资产。

## 7. Future design handoff

后续 Trae / Visual Design 在 Create Company 与 Create Employee 中均展示：Name + optional upload + preset selection + fallback。两处消费本 Pattern，不建立两套艺术或交互规则。本轮不启动 Trae、Figma 或高保真设计。

## 8. Registered decision

CEO AVATAR: **UPLOAD + PRESET + FALLBACK**
EMPLOYEE AVATAR: **UPLOAD + PRESET + FALLBACK**
PRESET STYLE: **CURIS CARTOON AVATAR SET**
AVATAR REQUIRED: **NO**
SHARED IDENTITY PATTERN: **YES**
NEW IDENTITY SYSTEM: **NO**
