import click
from .weather import WeatherClient

@click.group()
def cli():
    """智能天气查询工具"""
    pass

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