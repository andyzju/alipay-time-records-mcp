#!/usr/bin/env python3
"""
TCP服务器脚本，用于支持SEE方式连接MCP服务

此脚本用于启动基于TCP协议的FastMCP服务，监听指定端口，
允许通过网络连接访问MCP服务。

使用方法：
    python tcp_server.py
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server import app


def main():
    """主函数，启动FastMCP TCP服务器"""
    print("Starting FastMCP TCP server on localhost:8080")
    
    # 修改app的host和port
    app.host = "localhost"
    app.port = 8080
    
    # 运行服务器
    app.run(transport="streamable-http")


if __name__ == "__main__":
    main()