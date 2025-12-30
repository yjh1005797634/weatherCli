import os
from pathlib import Path

class Config:
    def __init__(self):
        # print("1.config类开始初始化")
        from dotenv import load_dotenv

    #.env文件路径
        env_path = Path(__file__).parent.parent / ".env"
        # print(f"2.尝试从{env_path}加载配置")

    #检查文件是否存在
        if env_path.exists():
            print(".env文件存在")
            load_dotenv(env_path)
        else:
            print("env文件不存在")
    #获取api密钥
        self.api_key = os.getenv("QWEATHER_API_KEY")
        print(f"3.读取到的api密钥：{self.api_key}")
        # print(self)

config = Config()
# print(f"4.config属性是：{config}")
# print(vars(config))

# for item in dir(config):
#     if not item.startswith("__"): #过滤内置属性
#         print(f" - {item}")        
# print(dir(config))


