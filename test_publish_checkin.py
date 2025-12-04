#!/usr/bin/env python3
"""
测试publish_checkin功能的脚本
"""

import asyncio
import base64
import os
import sys
from dotenv import load_dotenv

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 加载环境变量
load_dotenv()

async def test_publish_checkin():
    """测试publish_checkin功能"""
    print("=== 测试publish_checkin功能 ===")
    
    try:
        # 导入必要的模块
        from server import app, PublishCheckinParams
        
        # 准备测试参数，使用有效的Base64图像数据（1x1像素的PNG图像）
        valid_base64_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
        
        test_params = {
            "image_base64": valid_base64_image,
            "latitude": 30.263,
            "longitude": 120.122,
            "user_comment": "玉泉旁边的蛋糕店，居然除了榴莲蛋糕，太好吃了"
        }
        
        print(f"测试参数:")
        print(f"  - 纬度: {test_params['latitude']}")
        print(f"  - 经度: {test_params['longitude']}")
        print(f"  - 评论: {test_params['user_comment']}")
        print(f"  - 图片大小: {len(test_params['image_base64'])} 字符")
        
        # 创建参数对象
        params = PublishCheckinParams(**test_params)
        
        # 直接调用publish_checkin函数进行测试
        from server import publish_checkin
        result = await publish_checkin(params)
        
        print(f"\n✅ 调用成功:")
        print(f"  {result}")
            
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """主函数"""
    await test_publish_checkin()
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    asyncio.run(main())