# social-auto-upload 发布桥接镜像（Wave 2 · D2）
FROM python:3.11-slim

# patchright 依赖系统浏览器与基础库
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        git curl ca-certificates fonts-liberation libnss3 libatk1.0-0 \
        libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 \
        libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/bridge
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 桥接服务（翻译 Curis Connector 的 /api/publish 为 sau CLI 调用）
COPY publish_server.py .

# 上游仓库由 docker-compose 以 volume 挂载到 /app/social-auto-upload（不进镜像）。
# 安装 patchright 浏览器（首次启动容器内执行）。
RUN pip install --no-cache-dir patchright \
    && patchright install chromium || true

EXPOSE 8090
CMD ["python", "publish_server.py"]
