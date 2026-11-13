#!/bin/zsh
# _serve.sh — 用 http:// 把工作台原型供出来，供其他 Agent / 浏览器工具查看
#
# 为什么需要它：
#   多数 Agent 的浏览器工具（Playwright MCP / agent-browser / CDP 附着等）出于安全策略
#   **只允许 http(s) 协议**，不会操作 file:// 页面；file:// 也无法在无特权参数下被稳定读取。
#   本原型零外部依赖（无 fetch / XHR / ES module / Worker），走 http 与 file:// 表现完全一致。
#
# 用法：
#   ./_serve.sh              # 默认 8777 端口
#   ./_serve.sh 8899         # 指定端口
#   ./_serve.sh 8777 &       # 后台常驻
#
# 拿到地址后：
#   分文件版（改动用） : http://127.0.0.1:<PORT>/index.html
#   单文件版（交付用） : http://127.0.0.1:<PORT>/Content%20Growth%20Workspace.html

PORT="${1:-8777}"
DIR="$(cd "$(dirname "$0")" && pwd)"
PY="/Users/yy/.workbuddy/binaries/python/versions/3.13.12/bin/python3"

echo "服务目录：$DIR"
echo "分文件版：http://127.0.0.1:${PORT}/index.html"
echo "单文件版：http://127.0.0.1:${PORT}/Content%20Growth%20Workspace.html"
echo "（本机探测请加 --noproxy 127.0.0.1，本环境设有 HTTP_PROXY）"
echo ""

cd "$DIR" && exec "$PY" -m http.server "$PORT" --bind 127.0.0.1
