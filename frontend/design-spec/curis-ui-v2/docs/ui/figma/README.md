# Figma / Dev Mode 交付说明

Status: Deprecated

完整性状态见 [`../curis-ui-v2-completion-matrix.md`](../curis-ui-v2-completion-matrix.md)。

## 建立顺序

1. 新建 Figma Page：`Curis CEO Office / V2 Handoff`。
2. 按 `curis-ui-v2.all-pages.json` 建立 47 个页面 Frame；每个 Frame 复制 Desktop、Tablet、Mobile 三个尺寸。`curis-ui-v2.frames.json` 保留 19 个核心产品面的高保真 Frame 定义。
3. 将 `curis-ui-v2.tokens.json` 导入 Variables，变量名保持 JSON key，不改名。
4. 以 `curis-ui-v2.interactions.json` 建立 Prototype 连线和状态变体。
5. Dev Mode 中每个 Frame 的 Code Connect/source 指向 `pages/*.html`，组件名称与本文档第 3 节保持一致。

当前已导出全部 47 个 HTML 页面，三端截图共 47×3；全量路由与截图映射见 `curis-ui-v2.all-pages.json`。13 个一级页面、对象/配置页和所有二级/三级页面均已覆盖。Hover、Drawer、Empty、Error 等状态以 `interactions.json` 的变体规则在本地状态目录复用。

不使用 Figma 时，直接打开 `../index.html`；它汇总可运行原型、规格、47×3 三端截图、状态目录和逐页数据映射。

## 高保真要求

- 使用当前原型截图或页面作为视觉基准，不重新发明颜色、字体、阴影和布局。
- 每个页面至少保留 Default、Hover、Focus、Empty、Partial、Error；有抽屉/对话框的页面额外保留 Open/Selected/Success。
- 状态帧使用同一内容宽度与导航，不用裁剪图伪造响应式。
- 空态、错误态和未接入状态必须写明原因，不能用正常数字或绿色运行状态替代。

## 文件事实

这三个 JSON 是可 diff 的 Figma 建稿/校对源；当前未绑定具体 Figma team/file，因此不声称已经生成线上 `.fig` 文件。拿到 Figma 文件地址后，按上述顺序导入即可进入 Dev Mode 交付。
