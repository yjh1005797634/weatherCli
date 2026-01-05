import click
from .weather import WeatherClient
from .ai_agent import AIWeatherAgent #新增导入ai

print("🔧 cli.py开始加载...")

try:
    from .weather import WeatherClient
    print("✅ 成功导入WeatherClient")
except Exception as e:
    print(f"❌ 导入WeatherClient失败: {e}")

try:
    from .ai_agent import AIWeatherAgent
    print("✅ 成功导入AIWeatherAgent")
except Exception as e:
    print(f"❌ 导入AIWeatherAgent失败: {e}")

@click.group()
def cli():
    """智能天气查询工具"""
   
    pass

# ✅ 修复后的（添加装饰器）：
@cli.command()  # ← 添加这一行
@click.argument('query')  # ← 添加这一行（如果需要参数）
def ai(query):
    """AI智能天气助手 - 用自然语言查询天气"""
    click.echo(f"🤖 AI助手正在思考：'{query}'")
    print(f"A：{query}")
    
    # 创建AI智能体实例
    agent = AIWeatherAgent()
    
    try:
        # 使用智能查询
        response = agent.smart_weather_query(query)
        
        # 美化输出
        click.echo("\n" + "="*50)
        click.echo("✨ AI天气助手")
        click.echo("="*50)
        click.echo(f"💭 您的提问: {query}")
        click.echo("-"*50)
        # print(response)
        click.echo(f"💡 AI回复: {response}")
        click.echo("="*50)
        
    except Exception as e:
        click.echo(f"❌ AI服务出错: {e}", err=True)
        return 1

@cli.command()
def ai_chat():
    """进入AI聊天模式（持续对话）"""
    click.echo("🤖 进入AI天气助手聊天模式（输入'exit'退出）")
    click.echo("="*50)
    
    agent = AIWeatherAgent()
    
    while True:
        # 获取用户输入
        user_input = click.prompt("\n💬 您想问什么", type=str)
        
        # 检查退出
        if user_input.lower() in ['exit', '退出', 'quit', 'q']:
            click.echo("👋 再见！")
            break
        
        # 处理并显示回复
        click.echo("\n" + "-"*50)
        click.echo("🤖 AI思考中...")
        
        response = agent.smart_weather_query(user_input)
        
        click.echo(f"💡 {response}")
        click.echo("-"*50)



@cli.command()
@click.argument('location')
def weather(location):
    """查询指定地点的天气"""
    click.echo(f"正在查询 {location} 的天气...")
    print("2")
    client = WeatherClient()
    
    try:
        print("3")
        weather_data = client.get_weather(location)
        print(weather_data)
        
        # 美化输出
        click.echo("\n" + "="*40)
        click.echo(f"📍 {weather_data['city']} 实时天气")
        click.echo("="*40)
        click.echo(f"🌡️  温度：{weather_data['temperature']}")
        click.echo(f"☀️  天气：{weather_data['condition']}")
        click.echo(f"💨 风力：{weather_data['wind']}")
        click.echo(f"💧 湿度：{weather_data['humidity']}")
        click.echo(f"😌 体感：{weather_data['feels_like']}")
        click.echo(f"🌧️  降水：{weather_data['precipitation']}")
        click.echo("="*40)
        
    except Exception as e:
        click.echo(f"❌ 错误: {e}", err=True)
        return 1

if __name__ == "__main__":
    cli()