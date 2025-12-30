#1.为何需要两个URL？“城市搜索”和“天气查询”
#2.参数怎么传？requests.get()的params参数会自动把字典拼接成？location=北京&key=xxx的格式
#3.如何判断成功？看http状态码200.再看api返回json数据中code字段为“200”

import os
import requests
from dotenv import load_dotenv

print("开始真实api连通性测试……")

#加载环境变量 获取密钥
load_dotenv()
API_KEY = os.getenv("QWEATHER_API_KEY")
# print(API_KEY)
#测试城市搜索api
# city_search_url = "https://geoapi.qweather.com/geo/v2/city/lookup"
# city_search_url = "https://geoapi.qweather.com/geo/v2/city/lookup"
API_HOST = os.getenv("QWEATHER_API_HOST") 
# print(API_HOST)
# print(f"使用host：{API_HOST}")

#2.文档设置认证请求头
# headers = {
#     "Authorization": f"Bearer {API_KEY}"
# } 
#3.文档构建城市搜索URL
city_search_url = f"https://{API_HOST}/geo/v2/city/lookup"
params = {
    "location":"北京",
    "key":API_KEY,
    "adm":"北京",
    "number":1
}
# print(f"\n请求详情：")
# print(f"  URL:{city_search_url}")
# print(f"  参数：{params}")

#4.发送请求，传入headers
try:
    response = requests.get(city_search_url,params=params,timeout=10)
    #调试信息
    # print(f"\n响应状态码：{response.status_code}")
    # print(response.json)
    # print(f"响应内容（前300字符）:\n{response.text[:300]}\n")

#5.文档判断成功：先http200，再code200
    if response.status_code == 200:
        data = response.json()
        if data.get("code") == "200":
            city = data["location"][0]
            city_id = city['id']

            #构建天气实况api的url和参数
            weather_url = f"https://{API_HOST}/v7/weather/now"
            weather_params = {
                "location":city_id,
                "key":API_KEY
            }
            print(f"成功！")
            print(f"天气URL：{weather_url}")
            print(f"天气参数：{weather_params}")
            # print(f"  城市：{city['name']}(ID:{city['id']})")
            # print(f"  经纬度：[{city['lat']},{city['lon']}]")

            #发送请求实况天气
            try:
                weather_response = requests.get(weather_url,params=weather_params,timeout=10)
                print(f"天气api响应状态码：{weather_response.status_code}")
                if weather_response.status_code == 200:
                    weather_data = weather_response.json()
                    if weather_data.get("code") == "200":
                        now = weather_data["now"]
                        print("实时天气查询成功")
                        print(f" 温度：{now['temp']}℃")
                        print(f"天气状况：{now['text']}")
                        print(f"风向风力：{now['windDir']} {now['windScale']}级")
                        print(f"湿度:{now['humidity']}%")
                        print(f"体感温度：{now['feelsLike']}℃")
                        print(f"降水量:{now['precip']}毫米")
                    else:
                        print(f"天气api业务错误：{weather_data.get('message')}")
                else:
                    print(f"天气请求http错误")
            except requests.exceptions.RequestException as e:
                print(f"天气查询请求异常：{e}")


        else:
            print(f"api业务错误：{data.get('message','未知错误')}")
    else:
        print(f"http请求失败，请检查API_HOST和密钥")

except  requests.exceptions.RequestException as e:
    print(f"网络请求异常：{e}")           


















# import requests
# import json

# API_KEY = "e50854e9b44c47f58cde805408cac06e"
# base_urls = [
#     "https://geoapi.qweather.com/v2/city/lookup",
#     "https://geoapi.qweather.com/geo/v2/city/lookup",
#     "https://devapi.qweather.com/v2/city/lookup",
#     "https://devapi.qweather.com/geo/v2/city/lookup",
#     "https://api.qweather.com/v2/city/lookup",
#     "https://api.qweather.com/geo/v2/city/lookup"
# ]

# params = {
#     "location": "北京",
#     "key": API_KEY,
#     "number": 1
# }

# for url in base_urls:
#     try:
#         response = requests.get(url, params=params, timeout=10)
#         print(f"URL: {url}")
#         print(f"状态码: {response.status_code}")
#         if response.status_code == 200:
#             data = response.json()
#             print(f"返回数据: {json.dumps(data, ensure_ascii=False)}")
#             if data.get("code") == "200":
#                 print("成功！")
#                 break
#         else:
#             print(f"失败，响应文本: {response.text}")
#         print("---")
#     except Exception as e:
#         print(f"请求异常: {e}")
#         print("---")