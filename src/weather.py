
# import sys
# from src.weather import main
from .api_client import WeatherAPIClient 

class WeatherClient:
    def __init__(self):
        self.api_client = WeatherAPIClient()
    
    def get_city_info(self,location):
        print("5")
        try:
            data = self.api_client.get_city_id(location)
            #业务逻辑：验证api返回
            if data.get("code") != "200":
                raise BaseException(f"API业务错误:{data.get('message')}")
            city = data["location"][0]
            return {
                "name":city["name"],
                "id":city["id"],
                "lat":city["lat"],
                "lon":city["lon"]
            }
        except Exception as e:
            raise Exception(f"获取城市信息失败：{e}")

    def get_weather(self,location):
        print("4")
        try:
            city_info = self.get_city_info(location)
            city_id = city_info["id"]
            print("第几次调用？")
            data = self.api_client.get_current_weather(city_id)

            if data.get("code") != "200":
                raise Exception(f"天气api错误：{data.get('message')}")

            now = data["now"]
            return {
                "city": city_info["name"],
                "temperature": f"{now['temp']}℃",
                "condition": now["text"],
                "wind": f"{now['windDir']} {now['windScale']}级",
                "humidity": f"{now['humidity']}%",
                "feels_like": f"{now['feelsLike']}℃",
                "precipitation": f"{now['precip']}毫米"
            }  
        except Exception as e:
            raise Exception(f"获取天气失败：{e}")
            