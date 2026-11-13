# social-auto-upload 自托管部署（Wave 2 · D2）

来源：[github.com/dreammis/social-auto-upload](https://github.com/dreammis/social-auto-upload)
（MIT，Python + patchright 反检测分支）。

Curis 的**唯一发布通道**（替代被否决的 Relay），覆盖含无 API 平台（小红书 / 视频号）
在内的全部目标平台。创始人以自有 cookie 登录，不注册任何平台原生 OAuth App。

## 部署步骤

```bash
# 1) 拉取上游（真实仓库不进提交，已在 .gitignore 忽略 ./social-auto-upload）
git clone https://github.com/dreammis/social-auto-upload.git ./social-auto-upload

# 2) 起服务（仅发布桥接，对内网 127.0.0.1:8090）
docker compose up -d

# 3) 健康检查
curl http://localhost:8090/health
```

## Curis 侧对接

`backend/app/connectors/social_auto_upload.py` 在 `CURIS_CONNECTOR_MODE=real` 且
`SAU_URL=http://localhost:8090` 时，经内网 POST `/api/publish`
`{platform, account, cookie, package}`。

- `cookie`：创始人该平台 cookie，由 Curis Vault 解析后注入请求体，**仅本次请求使用**，
  不写文件、不进提交。
- `package`：ContentPublishPackage 的 dict（与生成端契约一致），由桥接服务翻译为
  `sau <platform> --account founder --cookie <file> --publish <pkg>` CLI 调用。

## 资源不足降级

若本机无法起 docker（内存/CPU 不足），Curis Connector 保持在 `CURIS_CONNECTOR_MODE=mock`，
发布链路以模拟回执验证 schema 串联，不阻塞前端与成果展示。待 docker 就绪，仅改 env
即可切真实端点，工作流代码无需改动。

## 合规边界

- ❌ 不注册任何平台原生 OAuth App（cookie 登录即最小感知路径）。
- ❌ 不碰 Relay / 任何第三方 SaaS。
- ✅ 创始人自有 cookie 仅来自 Curis Vault（local-dev），真实值不进 git。
