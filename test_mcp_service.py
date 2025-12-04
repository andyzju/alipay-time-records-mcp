#!/usr/bin/env python3
"""
MCP服务测试脚本
用于测试MCP服务是否能正常启动和响应
"""

import asyncio
import json
import sys
import os
from dotenv import load_dotenv

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 加载环境变量
load_dotenv()

def test_environment():
    """测试环境变量是否正确加载"""
    print("=== 环境变量测试 ===")
    required_vars = ["AMAP_API_KEY", "SUPABASE_URL", "SUPABASE_KEY"]
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: 已设置")
        else:
            print(f"❌ {var}: 未设置")
    print()

async def test_mcp_initialization():
    """测试MCP服务初始化"""
    print("=== MCP服务测试 ===")
    try:
        # 导入并初始化服务
        from server import app
        print("✅ MCP服务导入成功")
        
        # 显示服务信息
        print(f"✅ 服务名称: {app.name}")
        
        # 列出工具
        tools = await app.list_tools()
        print(f"✅ 已注册工具数量: {len(tools)}")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
        print()
        
    except Exception as e:
        print(f"❌ MCP服务初始化失败: {e}")
        import traceback
        traceback.print_exc()

async def test_amap_service():
    """测试高德地图服务"""
    print("=== 高德地图服务测试 ===")
    try:
        from amap_service import AMapService
        amap = AMapService()
        print("✅ 高德地图服务初始化成功")
        print(f"✅ API Key: {amap.api_key[:10] if amap.api_key else None}...")
        print()
    except Exception as e:
        print(f"❌ 高德地图服务初始化失败: {e}")
        import traceback
        traceback.print_exc()

async def test_supabase_client():
    """测试Supabase客户端"""
    print("=== Supabase客户端测试 ===")
    try:
        from server import get_supabase_client
        client = get_supabase_client()
        print("✅ Supabase客户端初始化成功")
        print(f"✅ Supabase URL: {client.supabase_url}")
        print()
    except Exception as e:
        print(f"❌ Supabase客户端初始化失败: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """主测试函数"""
    test_environment()
    await test_mcp_initialization()
    await test_amap_service()
    await test_supabase_client()
    print("=== 测试完成 ===")

if __name__ == "__main__":
    asyncio.run(main())