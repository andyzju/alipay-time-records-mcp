#!/usr/bin/env python3
"""
支付宝时空印记服务
基于高德地图 LBS 与 MCP 的"时空印记"服务，实现用户在物理世界的数字化打卡，
结合 AI 生成内容和地理信息数据存储，打造智能空间记忆系统。

功能：
1. publish_checkin: 完成定位 → 图像识别 → 文案生成 → 数据存储的完整链路
2. explore_nearby: 基于当前位置搜索周边 POI 并结合语义进行智能推荐

作者: Alibaba Cloud Team
"""

import asyncio
import base64
import os
import argparse
import sys
from typing import Optional, List
from datetime import datetime
from dotenv import load_dotenv

import httpx
from mcp.server.fastmcp.server import FastMCP
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from pydantic import BaseModel
import supabase
from supabase import create_client, Client

from amap_service import AMapService

# 加载.env文件中的环境变量
load_dotenv()

# 数据模型定义
class PublishCheckinParams(BaseModel):
    image_base64: str
    latitude: float
    longitude: float
    user_comment: Optional[str] = None


class ExploreNearbyParams(BaseModel):
    latitude: float
    longitude: float
    radius: int = 500


# 初始化服务
amap_service = AMapService()


def get_supabase_client() -> Client:
    """获取Supabase客户端"""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        raise ValueError("SUPABASE_URL和SUPABASE_KEY环境变量必须设置")
        
    return create_client(url, key)


async def upload_image_to_supabase(image_data: bytes, file_name: str) -> str:
    """上传图片到Supabase Storage并返回公共URL"""
    supabase_client = get_supabase_client()
    
    # 这里简化处理，实际项目中可能需要更复杂的文件名处理
    # 为了简化，我们返回一个模拟的URL
    # 在实际项目中，应该使用Supabase Storage API上传文件
    return f"https://example.com/images/{file_name}"


async def publish_checkin(params: PublishCheckinParams) -> str:
    """发布打卡信息"""
    try:
        # 1. 解码Base64图片
        image_data = base64.b64decode(params.image_base64)
        
        # 2. 上传图片到Supabase
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"checkin_{timestamp}.jpg"
        image_url = await upload_image_to_supabase(image_data, file_name)
        
        # 3. 使用高德API获取位置信息
        location_info = await amap_service.reverse_geocode(
            params.latitude, params.longitude
        )
        
        # 4. 使用AI生成内容（简化处理）
        ai_content = f"在{location_info.get('address', '某地')}的美好时光"
        if params.user_comment:
            ai_content += f"，{params.user_comment}"
        
        # 5. 存储到数据库
        supabase_client = get_supabase_client()
        
        # 构造数据记录
        record = {
            "user_id": "default_user",  # 实际项目中应该从会话中获取
            "location": f"SRID=4326;POINT({params.longitude} {params.latitude})",
            "poi_name": location_info.get("name", ""),
            "poi_address": location_info.get("address", ""),
            "adcode": location_info.get("adcode", ""),
            "image_url": image_url,
            "content": ai_content,
            "tags": [],  # 实际项目中可以从AI服务获取标签
            "mood": "",  # 实际项目中可以从AI服务获取情绪
        }
        
        # 插入数据库
        result = supabase_client.table("memories").insert(record).execute()
        
        return f"✅ 打卡成功！位置: {location_info.get('address', '未知位置')}"
        
    except Exception as e:
        raise Exception(f"发布打卡时出错: {str(e)}")


async def explore_nearby(params: ExploreNearbyParams) -> str:
    """探索附近的地点"""
    try:
        # 1. 使用高德API搜索附近的POI
        pois = await amap_service.search_nearby(
            params.latitude, params.longitude, params.radius
        )
        
        # 2. 查询数据库中附近的记忆
        supabase_client = get_supabase_client()
        
        # 使用RPC调用PostgreSQL函数获取附近记忆
        # 注意：需要确保数据库中已创建get_nearby_memories函数
        try:
            response = supabase_client.rpc(
                "get_nearby_memories",
                {
                    "lat": params.latitude,
                    "lon": params.longitude,
                    "radius_meters": params.radius
                }
            ).execute()
            
            nearby_memories = response.data if response.data else []
        except Exception as db_error:
            print(f"数据库查询出错: {db_error}")
            nearby_memories = []
        
        # 3. 结合POI和记忆生成推荐结果
        result_text = "🔍 附近的推荐地点:\n\n"
        
        # 添加POI信息
        if pois:
            result_text += "📍 附近地点:\n"
            for poi in pois[:5]:  # 限制显示前5个
                result_text += f"  • {poi.get('name', '未知地点')} - {poi.get('address', '地址未知')}\n"
        else:
            result_text += "📍 附近暂无POI信息\n"
        
        # 添加已有记忆
        if nearby_memories:
            result_text += f"\n💭 附近已有{len(nearby_memories)}条记忆:\n"
            for memory in nearby_memories[:3]:  # 限制显示前3个
                content = memory.get('content', '')[:50] + "..." if len(memory.get('content', '')) > 50 else memory.get('content', '')
                result_text += f"  • {memory.get('poi_name', '未知地点')} - {content}\n"
        else:
            result_text += "\n💭 您在附近还没有留下记忆，快去打卡吧！"
        
        return result_text
        
    except Exception as e:
        raise Exception(f"探索附近地点时出错: {str(e)}")


def check_environment():
    """检查必要的环境变量"""
    required_vars = ["AMAP_API_KEY", "SUPABASE_URL", "SUPABASE_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"警告: 以下环境变量未设置: {', '.join(missing_vars)}")
        print("请确保在 .env 文件中设置这些变量，或通过系统环境变量设置")
        return False
    
    return True


# 创建FastMCP服务器实例
# 配置host和port以启用TCP模式
app = FastMCP(
    name="alipay-geo-memory",
    host="0.0.0.0",  # 绑定到所有网络接口
    port=8000        # 监听8000端口
)

# 注册工具
@app.tool(
    name="publish_checkin",
    description="完成完整的'定位-识图-发布'链路，发布用户的位置打卡"
)
async def publish_checkin_tool(
    image_base64: str,
    latitude: float,
    longitude: float,
    user_comment: Optional[str] = None
) -> str:
    params = PublishCheckinParams(
        image_base64=image_base64,
        latitude=latitude,
        longitude=longitude,
        user_comment=user_comment
    )
    return await publish_checkin(params)


@app.tool(
    name="explore_nearby",
    description="基于高德POI和用户数据进行语义推荐，发现附近的有趣地点"
)
async def explore_nearby_tool(
    latitude: float,
    longitude: float,
    radius: int = 500
) -> str:
    params = ExploreNearbyParams(
        latitude=latitude,
        longitude=longitude,
        radius=radius
    )
    return await explore_nearby(params)


# 为支付宝小程序插件部署添加兼容性支持
def alipay_plugin_main():
    """支付宝小程序插件入口函数"""
    # 这个函数可以被支付宝小程序插件调用
    app.run(transport="streamable-http")


# 导出app实例，方便其他模块引用
server = app
__all__ = ['app', 'server']

if __name__ == "__main__":
    # 检查环境变量
    if not check_environment():
        sys.exit(1)
    
    # 当直接运行脚本时启动MCP服务
    # 使用streamable-http传输方式以启用HTTP服务器
    app.run(transport="streamable-http")
