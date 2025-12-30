from src.config import config

print("=== 配置测试 ===")
print(f"配置状态: {config}")
print(f"API密钥: {'*' * 8}{config.api_key[-4:] if len(config.api_key) > 4 else ''}")
print(f"默认城市: {config.default_city}")
print(f"模拟模式: {config.is_mock_mode}")

if config.is_mock_mode:
    print("\n⚠️  当前为模拟模式，将使用本地数据")
    print("   请前往和风天气官网获取API密钥")
else:
    print("\n✅ 配置正常，可以连接API")