import click
from .weather import WeatherClient
# from colorama_config import ColorConfig
# ColorConfig.init_colors()

@click.command()
@click.argument('city')
def main(city):
    """查询城市天气"""
    client = WeatherClient(city)
    result = client.get_weather()
    click.echo(f"🌤️ {result}")   


   
if __name__ == "__main__":
    main()
