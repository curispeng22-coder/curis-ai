# CURIS_HTML_PIXEL_FIDELITY_RECHECK

> Authority Class: RESEARCH / EVIDENCE · Date: 2026-09-13
> 方法：Codex M1–M8 测量表 + Final Decisions 7 类局部 L4 目标逐项对照；HTML 数值为 CSS EXACT（DOM），参考为 APPROXIMATE raster；不宣称 Pixel Exact。

| L4 目标 | 参考（Codex 测量） | HTML 本轮 | 判定 |
|---|---|---|---|
| Expert Card（M1/Z033） | 275×128 raster、4 列、avatar32、2 行截断、~3 tags、radius~12 | 284×~128 CSS、4 列（c4 grid）、avatar32、2 行截断、3 tags、radius12、padding12 | **VERIFIED**（结构+几何+状态；hover NOT OBSERVED 如实保留） |
| Skill Card（M2/Z036） | 274×91、icon24、紧凑说明、内联安装 | ~284×91、icon24、内联 + 安装/已安装、2 行说明、meta 行 | **VERIFIED**（同上备注） |
| File Reference（M3/Z048） | E1：对象身份/标题/meta/打开独立；上传过程 UNKNOWN | 附件=可选择对象（3 项 picker）、chip 可移除、Result 卡两列+打开 | **PARTIAL**（几何未逐值校准；上传过程态未实现） |
| Message Actions（M4/Z059） | ~7 动作贴近消息 + More 渐进披露 | 4 动作 + 复制/重新生成有 handler；More 未做 | **PARTIAL** |
| Claude Model Selector（M5/Z067） | 右侧锚定菜单、描述、当前 check | 就近锚定（含上方翻转）、当前项 check、未配置项解释禁用 | **VERIFIED**（结构+交互；菜单 260 宽级） |
| ChatGPT User Bubble（M6/Z045） | 448×68、p10/16、r22、右对齐浅底 | 右对齐浅紫底、限宽 82%、radius12、内嵌附件卡 | **VERIFIED**（结构+对齐；radius 取 Curis token 12 而非 22——语义覆盖竞品） |
| Linear Navigation（M7/Z125–126） | 行/缩进/分组节奏（234 raster 宽） | 组标签 11px 大写、行 32/28、子树缩进、计数徽章；宽 220=Frozen Shell | **VERIFIED**（节奏；宽度服从 Shell，不复制 234） |

- 其余原 L4 声明（0/24 VERIFIED）维持 Codex 降级结论：L3/L2 借鉴不冒充 L4。
- 22 项 NEED MORE EVIDENCE 未施工。
- 交互态（hover/focus/disabled）已在 CSS 定义（:hover/:focus-visible/disabled），像素级 hover 对照仍未执行——Codex 复验时可实测。
