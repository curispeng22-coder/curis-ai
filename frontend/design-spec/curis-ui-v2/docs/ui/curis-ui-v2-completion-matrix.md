# Curis UI V2 交付完整性矩阵

Status: Deprecated

更新时间：2026-07-27

## 已完成

| 项 | 状态 | 证据 |
|---|---|---|
| 页面 Frame 清单 | PASS | `figma/curis-ui-v2.all-pages.json`，47/47 |
| 一级页面默认态预览 | PASS | 13/13 默认预览 + 三端导出 |
| 对象/配置页默认态预览 | PASS | 6/6 默认预览 + 三端导出 |
| 二级/三级页面预览 | PASS | 28/28 三端导出 |
| 三端页面预览 | PASS | `exports/1440`、`exports/1024`、`exports/390`，47×3 |
| 可视状态目录 | PASS | `states/catalog-{1440,1024,390}.png` + `curis-ui-state-catalog.html` |
| 颜色、字体、间距、布局 Token | PASS | `figma/curis-ui-v2.tokens.json` |
| 导航、创建流、资源选择器交互清单 | PASS | `figma/curis-ui-v2.interactions.json` |
| 前端规格 Markdown | PASS | `curis-ui-v2-handoff.md` |
| 默认标题、导航宽度、导航层级 | PASS | 当前原型已统一并完成浏览器核对 |

## 外部边界（不阻塞前端实现）

| 缺口 | 当前状态 | 前端交付影响 |
|---|---|---|
| 真实 Figma 文件 | OPTIONAL | 不再作为前端交付前置条件；本地 HTML/PNG/JSON/Markdown 替代 |
| Figma 状态帧 | REPLACED | 状态目录已覆盖 Hover、Focus、Drawer、Empty、Partial、Error、Disabled、Success |
| 三端图像导出 | PASS | 严格生成 1440×900、1024×768、390×844 |
| 页面级 Dev Mode 标注 | PASS（本地替代） | Token JSON + 规格 Markdown + 状态目录 + 页面截图 |
| 数据字段逐页映射 | PASS | 19 个核心面在 `curis-ui-v2-data-map.json`，28 个二级/三级面在 `curis-ui-v2-secondary-page-contracts.json`，全量路由在 `figma/curis-ui-v2.all-pages.json` |
| Git diff / commit | BLOCKED | TRAE 原型目录不是 Git 仓库，当前文件可本地 diff，但没有 commit/PR 证据 |

## 结论

前端现在可以直接按本地交付包实现：47 个页面、三端截图、状态目录、Token、交互规则、逐页字段映射和 Markdown 均已齐。唯一外部缺口是 Git：当前 TRAE 原型目录不是 Git 仓库，因此需要将 `docs/ui/` 复制或提交到前端实际仓库后才能形成 commit/PR。
