import requests
import json

# === 第一步：配置你的参数 ===
# 在和风天气控制台（https://dev.qweather.com/console）获取你的 API Key
API_KEY = "58CE" 

# 请求的地址（注意：开发者版使用 devapi.qweather.com）
API_URL = "https://mj5pwdde98.re.qweatherapi.com/v7/weather/now"
# API_URL = "https://mj5pwdde98.re.qweatherapi.com/v7/weather/now"

# 目标城市/地点的 ID (例如：北京是 101010100，上海是 101020100)
# 你也可以使用经纬度，例如：location="116.41,39.92"
LOCATION_ID = "101010100" 

# === 第二步：构造请求 ===
# 设置请求头，这是鉴权的关键，不能放在 URL 参数里
headers = {
    'Authorization': f'Bearer {API_KEY}'
}

# 设置请求参数
params = {
    'location': LOCATION_ID
}

try:
    # 发送 GET 请求
    # 注意：和风天气默认返回 Gzip 压缩的数据，requests 会自动解压，所以不用手动处理
    response = requests.get(API_URL, params=params, headers=headers, timeout=10)
    print(response)
    
    # 检查 HTTP 状态码 (200 表示连接成功)
    if response.status_code == 200:
        # 解析 JSON 数据
        data = response.json()
        
        # === 第三步：解析并打印数据 ===
        # 检查 API 返回的业务状态码 (code)
        if data['code'] == '200':
            now = data['now']
            print("✅ 请求成功！")
            print(f"观测时间: {data['updateTime']}")
            print(f"地点ID: {data['location'][0]['id']}")
            print("-" * 30)
            print(f"🌡️  温度: {now['temp']}°C")
            print(f"☁️  天气: {now['text']}")
            print(f"🍃 风向: {now['windDir']}")
            print(f"📊 湿度: {now['humidity']}%")
            print(f"🔽 气压: {now['pressure']} hPa")
            print(f"👀 能见度: {now['vis']} km")
        else:
            print(f"❌ API 返回错误: {data['code']} - {data['message']}")
    else:
        print(f"❌ HTTP 请求失败，状态码: {response.status_code}")
        print(f"响应内容: {response.text}")

except requests.exceptions.RequestException as e:
    print(f"❌ 网络请求发生异常: {e}")