"""
AI天气智能体模块
职责：自然语言理解、意图识别、工具调用协调
"""
import json
from openai import OpenAI
from .config import config
from .weather import WeatherClient

class AIWeatherAgent:
    """AI天气智能体 - 自然语言到天气工具的桥梁"""
    # print(f"ai_agent文件拿到deepseek密钥:{config.deepseek_api_key}")
    def __init__(self):
        # 初始化AI客户端
        self.ai_client = OpenAI(
            api_key=config.deepseek_api_key,
            base_url="https://api.deepseek.com",
            timeout=30.0  # 适当超时
        )
        
        # 初始化天气工具
        self.weather_tool = WeatherClient()
        
        # 系统提示词 - 定义智能体的角色和能力
        self.system_prompt = """你是一个专业的天气助手，专门帮助用户查询天气信息。
        你的能力包括：
        1. 理解用户关于天气的自然语言查询
        2. 从用户问题中提取城市名称
        3. 调用天气工具获取实时天气数据
        4. 用友好、自然的语言回复用户
        
        如果用户的问题不是关于天气的，请礼貌地说明你只能处理天气相关问题。
        
        请始终以友好、专业的语气回复。"""
    
    def chat(self, user_input: str) -> str:
        """处理用户输入，返回AI回复"""
        print("########################难道没有执行吗？")
        try:
            # 调用DeepSeek API
            response = self.ai_client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7,  # 控制创造性，0-1之间
                max_tokens=500  # 限制回复长度
            )
            # print(f"RRRRRR:{response.choices[0]}")
            # 提取AI回复
            ai_reply = response.choices[0].message.content
            print(ai_reply)
            
            
            return ai_reply
            
        except Exception as e:
            return f"❌ AI服务暂时不可用: {str(e)}"
    
    def is_weather_query(self, user_input: str) -> bool:
        """判断用户输入是否为天气查询"""
        print(f"C:{user_input}")
        # 简单关键词匹配（后续可升级为AI判断）
        weather_keywords = ['天气', '气温', '温度', '下雨', '下雪', '晴天', '多云', '刮风']
        
        user_input_lower = user_input.lower()
        print(f"D:{weather_keywords}")
        for keyword in weather_keywords:
            if keyword in user_input_lower:
                return True
        return False
    
    def extract_city(self, user_input: str) -> str:
        """从用户输入中提取城市名"""
        # # 简单规则：取第一个中文地名（后续可升级为NER）
        # import re
        # print("我是智能体程序第二运行")
        # # 中文城市名匹配
        # city_pattern = r'[\u4e00-\u9fa5]{2,5}'
        # cities = re.findall(city_pattern, user_input)
        # print(f"E:{cities}")
        # if cities:
        #     print(f"F:{cities[0]}")
        #     return cities[0]  # 返回第一个匹配的城市
        
        # # 如果没有中文城市，尝试英文
        # # 这里简化处理，实际应用需要更复杂的逻辑
        # return None
        
        """简化版城市提取 - 硬编码测试"""
        print("🔍 提取城市名...")
    
    # 简单规则：查找"北京"或"上海"等
        if '北京' in user_input:
            return '北京'
        elif '上海' in user_input:
            return '上海'
        elif '广州' in user_input:
            return '广州'
        elif '深圳' in user_input:
            return '深圳'
    
    # 如果没有明确城市，返回None
        return None  
    
    def smart_weather_query(self, user_input: str) -> str:
        """
        智能天气查询：结合AI和规则判断
        1. 判断是否为天气查询
        2. 提取城市名
        3. 调用天气工具
        4. AI组织回复
        """
        print(f"我是智能体程序第一运行！！！")
        print(f"B：{user_input}")
        # 1. 判断意图
        if not self.is_weather_query(user_input):
            print("我是异常第一执行")
            return "您似乎不是在询问天气，我可以帮您查询任何城市的天气信息哦！"
        
        # 2. 提取城市名
        city = self.extract_city(user_input)
        print(f"G:{city}")
        if not city:
            print("我是异常第二执行")
            return "我没听清您要查询哪个城市，请告诉我城市名称，比如'北京天气怎么样？'"
        
        try:
            # 3. 调用天气工具
            print(f"H:{city}")
            weather_data = self.weather_tool.get_weather(city)
            print(f"WEATHEDATA:{weather_data}")
            # 4. 让AI组织回复
            weather_str = json.dumps(weather_data, ensure_ascii=False)
            print(f"WEATHERSTR:{weather_str}")
            prompt = f"""用户查询{city}的天气，这是获取到的实时天气数据：
            {weather_str}
            
            请用自然、友好的语言向用户回复，包括：
            1. 问候用户
            2. 简要报告天气情况
            3. 给出穿衣或出行建议（根据温度）
            4. 保持专业且亲切的语气
            
            回复时不要用JSON格式，要用自然的中文。"""
            print(f"prompt：{prompt}")
            response = self.ai_client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=300
            )
            # print(f"P:{response}")
            print(f"Q:{response.choices[0]}")
            return response.choices[0].message.content
            
        except Exception as e:
            # 如果天气API失败，让AI基于知识回复
            print(f"O:{city}")
            error_prompt = f"""用户查询{city}的天气，但天气服务暂时不可用（错误：{str(e)}）。
            请你基于一般知识，用友好的语气告诉用户可能的情况，并建议稍后再试。"""
            
            response = self.ai_client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": error_prompt}
                ],
                temperature=0.7
            )
            
            return response.choices[0].message.content