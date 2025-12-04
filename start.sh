#!/bin/bash

# 启动脚本
# 用于快速启动支付宝时空印记服务

echo "🚀 启动支付宝时空印记服务"

# 检查虚拟环境
if [ -d "venv" ]; then
    echo "🔄 激活虚拟环境"
    source venv/bin/activate
else
    echo "⚠️  未找到虚拟环境，请先运行:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "⚠️  未找到 .env 文件，请先复制 .env.example 并配置相应参数"
    exit 1
fi

# 启动服务
echo "📡 启动MCP服务 (stdio模式)"
python server.py