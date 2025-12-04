import httpx
import os
from typing import Dict, Optional, Tuple, List


class AMapService:
    def __init__(self):
        self.api_key = os.getenv("AMAP_API_KEY")
        self.base_url = "https://restapi.amap.com/v3/geocode/regeo"
        self.poi_search_url = "https://restapi.amap.com/v3/place/around"
        
    async def get_poi_info(self, latitude: float, longitude: float) -> Dict[str, Optional[str]]:
        """
        通过高德地图API获取POI信息
        
        Args:
            latitude: 纬度
            longitude: 经度
            
        Returns:
            包含POI信息的字典
        """
        if not self.api_key:
            raise ValueError("AMAP_API_KEY环境变量未设置")
            
        # 注意：高德API要求经度在前，纬度在后
        location = f"{longitude:.6f},{latitude:.6f}"
        
        params = {
            "key": self.api_key,
            "location": location,
            "extensions": "all",
            "output": "JSON"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.base_url, params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                
                result = {
                    "poi_name": None,
                    "poi_address": None,
                    "adcode": None
                }
                
                if data.get("status") == "1":  # 请求成功
                    regeocode = data.get("regeocode", {})
                    
                    # 获取地址信息
                    result["poi_address"] = regeocode.get("formatted_address")
                    result["adcode"] = regeocode.get("addressComponent", {}).get("adcode")
                    
                    # 尝试获取POI名称
                    pois = regeocode.get("pois", [])
                    if pois:
                        result["poi_name"] = pois[0].get("name")
                    else:
                        # 如果没有POI信息，则使用格式化地址作为备选
                        result["poi_name"] = result["poi_address"]
                        
                return result
                
            except httpx.TimeoutException:
                raise Exception("高德地图API请求超时")
            except httpx.RequestError as e:
                raise Exception(f"高德地图API请求错误: {str(e)}")
            except Exception as e:
                raise Exception(f"处理高德地图API响应时出错: {str(e)}")

    async def reverse_geocode(self, latitude: float, longitude: float) -> Dict[str, str]:
        """
        逆地理编码，根据经纬度获取地址信息
        
        Args:
            latitude: 纬度
            longitude: 经度
            
        Returns:
            包含地址信息的字典
        """
        return await self.get_poi_info(latitude, longitude)

    async def search_nearby(self, latitude: float, longitude: float, radius: int = 500) -> List[Dict]:
        """
        搜索附近的POI
        
        Args:
            latitude: 纬度
            longitude: 经度
            radius: 搜索半径（米），默认500米
            
        Returns:
            POI列表
        """
        if not self.api_key:
            raise ValueError("AMAP_API_KEY环境变量未设置")
            
        # 注意：高德API要求经度在前，纬度在后
        location = f"{longitude:.6f},{latitude:.6f}"
        
        params = {
            "key": self.api_key,
            "location": location,
            "radius": str(radius),
            "output": "JSON",
            "offset": "20",  # 返回数量
            "types": ""  # 空表示所有类型
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.poi_search_url, params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                
                if data.get("status") == "1":  # 请求成功
                    pois = data.get("pois", [])
                    return pois
                else:
                    error_msg = data.get("info", "未知错误")
                    raise Exception(f"高德地图POI搜索失败: {error_msg}")
                    
            except httpx.TimeoutException:
                raise Exception("高德地图API请求超时")
            except httpx.RequestError as e:
                raise Exception(f"高德地图API请求错误: {str(e)}")
            except Exception as e:
                raise Exception(f"处理高德地图API响应时出错: {str(e)}")