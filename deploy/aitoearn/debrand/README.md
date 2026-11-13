# 去品牌补丁（AiToEarn）

本目录用于存放覆盖 AiToEarn 前端品牌资源的补丁（`debrand.patch`），使自托管实例
仅作为 Curis 内部生成地基，去除 aitoearn 标识（合规要求：不得白标第三方 Relay）。

应用方式（在克隆的 ./aiToEarn 内）：

```bash
cd ../aiToEarn && git apply ../debrand/debrand.patch
```

若上游版本差异导致 patch 不适用，可手动替换前端品牌文案/Logo 资源（不影响生成 API）。
本目录在 docker-compose 中以只读卷挂载到 `/app/debrand`；未提供 patch 时为空挂载，
不影响服务启动。
