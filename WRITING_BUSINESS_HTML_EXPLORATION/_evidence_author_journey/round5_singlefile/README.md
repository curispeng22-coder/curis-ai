# 交付物形态复跑（index.single.html）

本目录是**交付物形态**的验收证据：入口 = `index.single.html`（由 `_build.js` 内联 CSS/JS 生成，禁止手改）。

- 命令：`WRITING_ENTRY=index.single.html WRITING_EV=round5_singlefile node _author_journey_acceptance.js`
- 结果：**PASS 28 · PARTIAL 0 · FAIL 0 · Console Error 0 · 截图 22 张**
- 目的：证明**交付物与源码形态行为一致**（避免「源码通过、单文件构建过期或内联后行为不同」这一类问题）。
- 截图索引与逐条说明见同为验收证据的 **`../round5/INDEX.md`** 与 `../round5/PATH_RECORD.md`；本目录的 `PATH_RECORD.md` 为同一套断言在本入口下的实测值。
