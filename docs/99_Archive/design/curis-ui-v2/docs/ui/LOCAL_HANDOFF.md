# Curis UI V2 · 无 Figma 前端交付包

Status: Deprecated

## 前端从这里开始

打开 `docs/ui/index.html`，或访问：

`http://127.0.0.1:8765/docs/ui/index.html`

## 交付内容

- 可运行高保真原型：`pages/*.html`、`assets/*.css`、`assets/*.js`
- 页面截图：`exports/1440/`、`exports/1024/`、`exports/390/`，47 页面 × 3 尺寸
- 截图索引：`frontend/design-spec/curis-ui-v2/docs/ui/exports/manifest.json`、`frontend/design-spec/curis-ui-v2/docs/ui/figma/curis-ui-v2.all-pages.json`
- `exports/` 另保留 `project-miniapp.png`、`project-xhs.png` 两个旧别名截图；实际页面以 `*-detail.png` 为准，别名已在 manifest 标注。
- 交互状态目录：`frontend/design-spec/curis-ui-v2/docs/ui/curis-ui-state-catalog.html` 与 `frontend/design-spec/curis-ui-v2/docs/ui/states/catalog-{size}.png`
- 设计变量：`frontend/design-spec/curis-ui-v2/docs/ui/figma/curis-ui-v2.tokens.json`
- 交互规则：`frontend/design-spec/curis-ui-v2/docs/ui/figma/curis-ui-v2.interactions.json`
- 逐页 Frame：`frontend/design-spec/curis-ui-v2/docs/ui/figma/curis-ui-v2.frames.json`
- 逐页字段/状态：`frontend/design-spec/curis-ui-v2/docs/ui/curis-ui-v2-data-map.json`（19 个核心面）+ `frontend/design-spec/curis-ui-v2/docs/ui/curis-ui-v2-secondary-page-contracts.json`（28 个二级/三级面）+ `frontend/design-spec/curis-ui-v2/docs/ui/figma/curis-ui-v2.all-pages.json`（47 个全量路由）
- 实现规格：`frontend/design-spec/curis-ui-v2/docs/ui/curis-ui-v2-handoff.md`
- 完整性检查：`frontend/design-spec/curis-ui-v2/docs/ui/curis-ui-v2-completion-matrix.md`

## 实现规则

1. 先复用现有 `navigation-ia.css/js`、`colors_and_type.css` 和项目详情资源选择器。
2. 页面结构、导航层级、标题字号、状态文案以 Markdown 和截图为准；不自行重排。
3. 先完成 Default，再按状态目录补 Hover、Focus、Drawer、Empty、Partial、Error、Disabled、Success。
4. 数据缺失显示“未记录 / 未读取事实 / 未分配”，不得用 0 或正常状态补位。
5. 1440、1024、390 三端必须保持同一信息顺序，不产生横向溢出。

这套本地交付包已经替代 Figma，不需要 Figma 账号或文件权限即可开始前端实现。
