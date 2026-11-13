# 自包含测试夹具

`music_legacy/` 是音乐 0.1.0 包的固定字节夹具，仅供旧版实例兼容性测试。
从仓库当前音乐包的共有字段恢复旧版：移除 MusicOperatingScope 声明和绑定，
manifest 版本与 song schemaVersion 恢复 0.1.0，导航和主界面标题恢复“歌曲创作”。
JSON 使用 UTF-8、两空格缩进和末尾换行。

恢复后使用生产 validate_package 的逐路径/字节聚合算法校验，摘要为
`5d9f36c36c2461f4540ad59277b56447a1a67cb2953759f43c52afbe5ed2cf76`，
与 app.music_entry_service.LEGACY_DIGEST 完全一致；测试保留该固定摘要断言。
这不是历史 preimages 来源证明，也不代表新的产品发布或 Owner 接受。

写作测试直接使用已纳入版本控制的 app/bundled_workspace_packages/writing_authoring，
保留 WritingChapterService.PACKAGE_DIGEST 精确校验，不依赖 artifacts/tasks。
