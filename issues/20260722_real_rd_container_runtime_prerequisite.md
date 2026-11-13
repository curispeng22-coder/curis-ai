# RealRD Container Runtime Prerequisite

**Status: PASS_WITH_NOTE** — classic-builder deny-all context 已由质量独立复核（`8ca63ce7` / image `a2cf1625`）；完整宿主 git status 非 clean 仅为既有 backend untracked，受控镜像 git diff 仍限 fixture，不阻塞取证。

## Objective

为既有 RealRD 单次取证补齐容器内固定运行时，不做泛化重构：镜像已有原生 Python 的绝对 argv 与可审计、固定来源的 Git。

## Preparation

在不构建、不联网、不改代码的前提下，固化：

1. 镜像内实际原生 Python 绝对路径，并确认固定 RealRD 测试 argv 的最小替换点；禁止容器 `.venv`、wrapper 或宿主直跑。
2. Git 的唯一镜像来源、精确版本与校验方式；不得使用未锁定的 latest。
3. 为 Git 获取所需的最小新增 build 域名闭集。

安全 PASS 后，才允许最小实现、一次受控镜像重建与质量验证；随后回到既有 RealRD 单次取证 Gate。

## Non-goals

- 不重构执行器、不改变测试语义、不新增运行时抽象或通用工具安装。
- 不注 Key、不启模型、不出网调用、不执行 RealRD 业务写入。

## Acceptance

1. Python argv、Git 来源/版本/校验和 build 域名均为唯一可审计值。
2. 安全确认来源闭集与镜像内边界后，才实施并重建。
3. 重建后质量仅验证固定 Python、Git、原 command 与现有受控 egress；不执行模型调用。

## Approved Implementation

- named-context 方案已废弃：当前平台不支持，禁止安装 buildx 或下载插件。
- 使用经典 builder 兼容的最小 root build context，并采用 Dockerfile 专属 deny-all whitelist；仅允许 `backend`、批准 fixture 文件与该 Dockerfile。若 Dockerfile 专属 ignore 不受 classic builder 支持，才允许同等效果的 root `.dockerignore` 白名单。
- Dockerfile 仅 COPY 批准 fixture 文件；禁止将仓库根目录、宿主 `.git` 或宿主挂载送入 build context。
- 镜像内在 `/srv/curis` 创建确定性 Git 初始提交，只纳入该 fixture，供既定只读 git diff 使用。
- 固定 Python argv 为 `/usr/local/bin/python`。
- 禁止 wrapper、COPY 全仓、复制宿主 `.git`、额外网络、Key 或模型调用。
- 重建前必须静态确认构建上下文文件清单。

## Route

系统交付席只读固化来源与最小变更 → 安全边界席 PASS → 系统交付席最小实现/一次重建 → 质量运行席验证。
