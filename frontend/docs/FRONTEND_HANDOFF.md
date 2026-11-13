# 前端接手指令 · 指针

> **合并版交接指令（先读这条，可直接发送）**：`docs/03_Design/Curis_UI_Frontend_Handoff_Memo_2026-08-05.md`
> **深度展开版（逐条细节）**：`docs/03_Design/Frontend_Handoff_Instructions_2026-08-05.md`
> 二者均在 `Curis AI Workspace/docs/03_Design/`，与 Frozen 规格同目录。

## TL;DR

- **视觉合同 = Frozen 规格** `docs/03_Design/Curis_UI_Frozen_Spec_2026-08-04.md`。字号 ≤7 档（无 <12px）、圆角 ≤5 档、间距 ≤8 档、触达 ≥32px、对比度 ≥4.5:1、令牌纪律，均已审计通过（前端审计 error=0）。
- **✅ 总控裁定（2026-08-05）：之前的前端视觉设计（`terra-*` 体系）全部作废，新版以 Frozen `--ui-*` 为准。** `terra-*` 令牌 / `Terra*` 组件视觉 / `design-spec/curis-ui-v2` 旧文档均 deprecated；仅视觉层按 `--ui-*` 重做，路由/API/数据逻辑保留。详见合并版 §一、深度版 §2/§9。
- `curis-ui-prototype/` 是**高保真参考**（mock 数据），按 Frozen 规格**重建**组件，勿逐行搬 HTML。
- 前端已有 `Terra*` 组件体系与真实路由（ceo-office/* 很完整），本指令是「把现有 `Terra*` 视觉重新按 `--ui-*` 落地」。
- **UI Designer 已落地**：Epic A（令牌/全局层）、B（组件红线层：52px 顶栏/220px 侧栏/触达≥32px/SVG 合规）、D（运行时能力切换器）、A5（Dev Mode + 审计脚本，error=0）。**前端接手 Epic C（页面像素对齐）/ E（无障碍复核）/ F（用户旅程验收）。**

## 开工前必做

1. 读合并版交接指令（文档地址 + 规范介绍 + 重点，已合并在一页）。
2. 读 Frozen 规格 §1–§8；深度版 §2（terra-* → --ui-* 映射）与 §9（D1–D4 裁决项）。
3. 复制 Frozen `tokens.css` 到 `frontend/app/globals.css` 设计层；复用 `scripts/ui-audit.mjs` 做验收（深度版 §6）。
4. 认领 Epic C/E/F 并建 issue（按工作纪律：一个 issue 一提交）。

## 任务 Epic

A 令牌与全局层 ✅ · B 组件库（红线层 ✅，形态随 C） · C 页面接入（对齐 Frozen §4）🔶 · D 运行时能力切换器 ✅ · E 无障碍复核 🔶 · F 验收 🔶

详细尺寸/状态/令牌/数据契约见 Frozen 规格与深度版指令。
