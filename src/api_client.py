import requests
from .config import config

class WeatherAPIClient:
    def __init__(self):
        self.api_key = config.api_key
        self.api_host = config.weather_url
    def _make_request(self,endpoint,params):
        print("7")
        url = f"https://{self.api_host}/{endpoint}"

        try:
            response = requests.get(url,params=params,timeout=10)
            response.raise_for_status
            # print(response.json())
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API请求失败：{e}")
        
    def get_city_id(self,location):
        print("6")
        endpoint = "geo/v2/city/lookup"
        params = {
            "location":location,
            "key":self.api_key,
            "adm":location,
            "number":1
        }    
        return self._make_request(endpoint,params)
    
    def get_current_weather(self,city_id):
        print("8")
        endpoint = "v7/weather/now"
        params = {
            "location":city_id,
            "key":self.api_key
        }
        print(self._make_request(endpoint,params))
        return self._make_request(endpoint,params)