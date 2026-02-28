#!/bin/bash
# iMocha 本地离线服务器启动脚本

PORT=8888
DIRECTORY="$(dirname "$0")/www.imocha.io"

echo "🚀 启动 iMocha 本地服务器..."
echo "📁 目录: $DIRECTORY"
echo "🌐 地址: http://localhost:$PORT"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

cd "$DIRECTORY" && python3 -m http.server $PORT
