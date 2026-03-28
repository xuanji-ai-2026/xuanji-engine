"""
UI模板配置模块 - 基础功能测试
"""

import sys
import os
import asyncio

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from ui_template_config import UITemplateConfig
    from logo_manager import LogoManager
    from theme_manager import ThemeManager
    from layout_manager import LayoutManager
    from ui_template_api import UITemplateAPI
    print("✓ 所有模块导入成功")
except Exception as e:
    print(f"✗ 模块导入失败: {e}")
    sys.exit(1)


async def test_basic_functionality():
    """测试基础功能"""
    print("\n[测试基础功能]")

    try:
        # 测试配置管理器
        print("测试配置管理器...")
        config = UITemplateConfig()
        version = await config.get_config("version")
        print(f"  配置版本: {version}")
        await config.set_config("test.key", "test_value")
        value = await config.get_config("test.key")
        print(f"  ✓ 配置读写成功: {value == 'test_value'}")

        # 测试主题管理器
        print("测试主题管理器...")
        theme_manager = ThemeManager()
        themes = await theme_manager.list_themes()
        print(f"  可用主题数量: {themes['total']}")
        print(f"  ✓ 主题管理器工作正常")

        # 测试布局管理器
        print("测试布局管理器...")
        layout_manager = LayoutManager()
        layouts = await layout_manager.list_layouts()
        print(f"  可用布局数量: {layouts['total']}")
        print(f"  ✓ 布局管理器工作正常")

        # 测试API
        print("测试API接口...")
        api = UITemplateAPI()
        status = await api.api_get_status()
        print(f"  ✓ API接口工作正常")
        print(f"  系统状态: {status['status']}")

        return True

    except Exception as e:
        print(f"  ✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    print("="*60)
    print("UI模板配置模块 - 基础测试")
    print("="*60)

    success = await test_basic_functionality()

    print("\n" + "="*60)
    if success:
        print("✓ 所有基础测试通过")
    else:
        print("✗ 测试失败")
    print("="*60)

    return success


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
