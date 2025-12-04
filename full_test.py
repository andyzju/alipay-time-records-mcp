#!/usr/bin/env python3
"""
完整的端到端测试脚本
测试publish_checkin和explore_nearby两个功能
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
        from server import PublishCheckinParams, publish_checkin
        
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
        
        # 调用publish_checkin函数进行测试
        result = await publish_checkin(params)
        
        print(f"\n✅ 打卡功能调用成功:")
        print(f"  {result}")
        return True
            
    except Exception as e:
        print(f"❌ 打卡功能测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_explore_nearby():
    """测试explore_nearby功能"""
    print("\n=== 测试explore_nearby功能 ===")
    
    try:
        # 导入必要的模块
        from server import ExploreNearbyParams, explore_nearby
        
        # 准备测试参数
        test_params = {
            "latitude": 30.263,
            "longitude": 120.122,
            "radius": 500
        }
        
        print(f"测试参数:")
        print(f"  - 纬度: {test_params['latitude']}")
        print(f"  - 经度: {test_params['longitude']}")
        print(f"  - 搜索半径: {test_params['radius']} 米")
        
        # 创建参数对象
        params = ExploreNearbyParams(**test_params)
        
        # 调用explore_nearby函数进行测试
        result = await explore_nearby(params)
        
        print(f"\n✅ 探索功能调用成功:")
        print(f"  {result}")
        return True
            
    except Exception as e:
        print(f"❌ 探索功能测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """主函数"""
    print("开始端到端测试...")
    
    # 测试publish_checkin功能
    publish_success = await test_publish_checkin()
    
    # 测试explore_nearby功能
    explore_success = await test_explore_nearby()
    
    print("\n=== 测试总结 ===")
    if publish_success and explore_success:
        print("✅ 所有测试通过!")
    else:
        print("❌ 部分测试失败")
        if not publish_success:
            print("  - publish_checkin 功能测试失败")
        if not explore_success:
            print("  - explore_nearby 功能测试失败")

if __name__ == "__main__":
    asyncio.run(main())