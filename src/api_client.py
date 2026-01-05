import requests
from .config import config

class WeatherAPIClient:
    def __init__(self):
        self.api_key = config.api_key
        self.api_host = config.weather_url
    def _make_request(self,endpoint,params):
        print("我是智能体第六运行")
        print("7")
        print(f"N:{params}")
        url = f"https://{self.api_host}/{endpoint}"
        print("程序卡在这里了吗？")
        try:
            response = requests.get(url,params=params,timeout=10)
            # print(response.json())
            response.raise_for_status()
            print(response.json())
            return response.json()
           
        except requests.exceptions.RequestException as e:
            raise Exception(f"API请求失败：{e}")
    
    # print(self._make_request())

    def get_city_id(self,location):
        print("6")
        print(f"K:{location}")
        endpoint = "geo/v2/city/lookup"
        params = {
            "location":location,
            "key":self.api_key,
            "adm":location,
            "number":1
        }    
        print(f"L:{location}")
        print(f"M:{self._make_request(endpoint,params)}")
        return self._make_request(endpoint,params)
    
    def get_current_weather(self,city_id):
        print("我是智能体第五运行")
        print("8")
        endpoint = "v7/weather/now"
        params = {
            "location":city_id,
            "key":self.api_key
        }
        # print(self._make_request(endpoint,params))
        return self._make_request(endpoint,params)