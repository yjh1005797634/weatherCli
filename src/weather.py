
# import sys
# from src.weather import main

class WeatherClient:
    class __init__(self,api_key):
       # 1. 核心配置（必须）
        self.api_key = api_key        # API密钥
        self.base_url = "https://devapi.qweather.com/v7"
        self.geo_url = "https://geoapi.qweather.com/v2"
        
        # 2. 状态管理（优化体验）
        self.cache = {}               # 缓存天气数据，减少API调用
        self.city_id_cache = {}       # 缓存城市ID，避免重复查询
        self.session = None           # HTTP会话，提高请求效率
        
        # 3. 统计信息（调试用）
        self.request_count = 0        # 记录请求次数
        self.error_count = 0          # 记录错误次数