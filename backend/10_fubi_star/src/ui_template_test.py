"""
辅弼星辰（扩展层）- UI模板配置单元测试
版本: v2.0
负责人: 康辅星 (162)
功能: 测试UI模板配置模块的所有功能
"""

import asyncio
import tempfile
import shutil
from pathlib import Path
import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.ui_template_config import UITemplateConfig
from src.logo_manager import LogoManager
from src.background_manager import BackgroundManager
from src.animation_manager import AnimationManager
from src.theme_manager import ThemeManager
from src.layout_manager import LayoutManager
from src.ui_template_api import UITemplateAPI


class TestResults:
    """测试结果收集器"""

    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.errors = []

    def add_result(self, test_name: str, success: bool, error: str = None):
        self.total += 1
        if success:
            self.passed += 1
            print(f"✓ {test_name}")
        else:
            self.failed += 1
            print(f"✗ {test_name}")
            if error:
                self.errors.append(f"{test_name}: {error}")
                print(f"  Error: {error}")

    def summary(self):
        print("\n" + "="*60)
        print(f"测试总结: {self.passed}/{self.total} 通过")
        print(f"通过: {self.passed}, 失败: {self.failed}")
        if self.errors:
            print("\n失败详情:")
            for error in self.errors:
                print(f"  - {error}")
        print("="*60)
        return self.failed == 0


class UITemplateConfigTests:
    """UI模板配置测试"""

    def __init__(self, results: TestResults, temp_dir: Path):
        self.results = results
        self.temp_dir = temp_dir

    async def run_all(self):
        """运行所有测试"""
        print("\n[UI模板配置测试]")
        await self.test_init()
        await self.test_get_set_config()
        await self.test_update_config()
        await self.test_reset_config()
        await self.test_validate_config()
        await self.test_export_import_config()

    async def test_init(self):
        """测试初始化"""
        try:
            config_dir = str(self.temp_dir / "test_config")
            config = UITemplateConfig(config_dir)
            self.results.add_result("初始化配置", config.config_file.exists())
        except Exception as e:
            self.results.add_result("初始化配置", False, str(e))

    async def test_get_set_config(self):
        """测试获取和设置配置"""
        try:
            config_dir = str(self.temp_dir / "test_config")
            config = UITemplateConfig(config_dir)

            # 设置配置
            await config.set_config("logo.width", 300)
            width = await config.get_config("logo.width")
            self.results.add_result("设置配置项", width == 300)

            # 获取嵌套配置
            height = await config.get_config("logo.height")
            self.results.add_result("获取嵌套配置", height == 80)
        except Exception as e:
            self.results.add_result("获取/设置配置", False, str(e))

    async def test_update_config(self):
        """测试批量更新配置"""
        try:
            config_dir = str(self.temp_dir / "test_config")
            config = UITemplateConfig(config_dir)

            # 批量更新
            updates = {
                "logo": {
                    "width": 250,
                    "height": 100
                }
            }
            success = await config.update_config(updates)
            width = await config.get_config("logo.width")
            self.results.add_result("批量更新配置", success and width == 250)
        except Exception as e:
            self.results.add_result("批量更新配置", False, str(e))

    async def test_reset_config(self):
        """测试重置配置"""
        try:
            config_dir = str(self.temp_dir / "test_config")
            config = UITemplateConfig(config_dir)

            # 修改配置
            await config.set_config("logo.width", 500)

            # 重置配置
            await config.reset_config("logo.width")
            width = await config.get_config("logo.width")
            self.results.add_result("重置配置项", width == 200)  # 默认值
        except Exception as e:
            self.results.add_result("重置配置", False, str(e))

    async def test_validate_config(self):
        """测试验证配置"""
        try:
            config_dir = str(self.temp_dir / "test_config")
            config = UITemplateConfig(config_dir)

            result = await config.validate_config()
            self.results.add_result("验证配置有效性", result["valid"])
        except Exception as e:
            self.results.add_result("验证配置", False, str(e))

    async def test_export_import_config(self):
        """测试导出和导入配置"""
        try:
            config_dir = str(self.temp_dir / "test_config")
            config1 = UITemplateConfig(config_dir)

            # 修改配置

            await config1.set_config("logo.width", 400)

            # 导出
            exported = await config1.export_config()

            # 导入到新实例
            config_dir2 = str(self.temp_dir / "test_config_import")
            config2 = UITemplateConfig(config_dir2)
            success = await config2.import_config(exported)
            width = await config2.get_config("logo.width")

            self.results.add_result("导出/导入配置", success and width == 400)
        except Exception as e:
            self.results.add_result("导出/导入配置", False, str(e))


class LogoManagerTests:
    """LOGO管理器测试"""

    def __init__(self, results: TestResults, temp_dir: Path):
        self.results = results
        self.temp_dir = temp_dir

    async def run_all(self):
        """运行所有测试"""
        print("\n[LOGO管理器测试]")
        await self.test_upload_logo()
        await self.test_list_logos()
        await self.test_delete_logo()

    async def test_upload_logo(self):
        """测试上传LOGO"""
        try:
            storage_dir = str(self.temp_dir / "test_logos")
            manager = LogoManager(storage_dir)

            # 创建测试图片数据
            from PIL import Image
            import io
            img = Image.new('RGB', (200, 80), color='red')
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            file_data = img_bytes.getvalue()

            # 上传
            result = await manager.upload_logo(file_data, "test.png", "light")
            self.results.add_result("上传LOGO", result["success"] and "file_id" in result)
        except Exception as e:
            self.results.add_result("上传LOGO", False, str(e))

    async def test_list_logos(self):
        """测试列出LOGO"""
        try:
            storage_dir = str(self.temp_dir / "test_logos")
            manager = LogoManager(storage_dir)

            result = await manager.list_logos()
            self.results.add_result("列出LOGO", result["success"])
        except Exception as e:
            self.results.add_result("列出LOGO", False, str(e))

    async def test_delete_logo(self):
        """测试删除LOGO"""
        try:
            storage_dir = str(self.temp_dir / "test_logos")
            manager = LogoManager(storage_dir)

            # 先上传一个LOGO
            from PIL import Image
            import io
            img = Image.new('RGB', (200, 80), color="blue")
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            file_data = img_bytes.getvalue()

            upload_result = await manager.upload_logo(file_data, "delete_test.png", "dark")
            if upload_result["success"]:
                file_id = upload_result["file_id"]
                delete_result = await manager.delete_logo(file_id)
                self.results.add_result("删除LOGO", delete_result["success"])
            else:
                self.results.add_result("删除LOGO", False, "上传失败")
        except Exception as e:
            self.results.add_result("删除LOGO", False, str(e))


class ThemeManagerTests:
    """主题管理器测试"""

    def __init__(self, results: TestResults, temp_dir: Path):
        self.results = results
        self.temp_dir = temp_dir

    async def run_all(self):
        """运行所有测试"""
        print("\n[主题管理器测试]")
        await self.test_list_themes()
        await self.test_create_theme()
        await self.test_get_theme()
        await self.test_set_current_theme()
        await self.test_generate_css_variables()

    async def test_list_themes(self):
        """测试列出主题"""
        try:
            config_dir = str(self.temp_dir / "test_themes")
            manager = ThemeManager(config_dir)

            result = await manager.list_themes()
            self.results.add_result("列出主题", result["success"] and result["total"] >= 3)
        except Exception as e:
            self.results.add_result("列出主题", False, str(e))

    async def test_create_theme(self):
        """测试创建主题"""
        try:
            config_dir = str(self.temp_dir / "test_themes")
            manager = ThemeManager(config_dir)

            colors = {
                "primary": "#ff0000",
                "secondary": "#00ff00",
                "success": "#0000ff"
            }

            result = await manager.create_theme(
                "test_theme",
                "测试主题",
                "测试主题描述",
                colors
            )
            self.results.add_result("创建主题", result["success"])
        except Exception as e:
            self.results.add_result("创建主题", False, str(e))

    async def test_get_theme(self):
        """测试获取主题"""
        try:
            config_dir = str(self.temp_dir / "test_themes")
            manager = ThemeManager(config_dir)

            result = await manager.get_theme("default")
            self.results.add_result("获取主题", result["success"])
        except Exception as e:
            self.results.add_result("获取主题", False, str(e))

    async def test_set_current_theme(self):
        """测试设置当前主题。"""
        try:
            config_dir = str(self.temp_dir / "test_themes")
            manager = ThemeManager(config_dir)

            result = await manager.set_current_theme("dark")
            self.results.add_result("设置当前主题", result["success"])
        except Exception as e:
            self.results.add_result("设置当前主题", False, str(e))

    async def test_generate_css_variables(self):
        """测试生成CSS变量"""
        try:
            config_dir = str(self.temp_dir / "test_themes")
            manager = ThemeManager(config_dir)

            result = await manager.generate_css_variables("default")
            self.results.add_result("生成CSS变量", result["success"] and "css_variables" in result)
        except Exception as e:
            self.results.add_result("生成CSS变量", False, str(e))


class LayoutManagerTests:
    """布局管理器测试"""

    def __init__(self, results: TestResults, temp_dir: Path):
        self.results = results
        self.temp_dir = temp_dir

    async def run_all(self):
        """运行所有测试"""
        print("\n[布局管理器测试]")
        await self.test_list_layouts()
        await self.test_create_layout()
        await self.test_get_layout()
        await self.test_set_current_layout()

    async def test_list_layouts(self):
        """测试列出布局"""
        try:
            config_dir = str(self.temp_dir / "test_layouts")
            manager = LayoutManager(config_dir)

            result = await manager.list_layouts()
            self.results.add_result("列出布局", result["success"] and result["total"] >= 4)
        except Exception as e:
            self.results.add_result("列出布局", False, str(e))

    async def test_create_layout(self):
        """测试创建布局"""
        try:
            config_dir = str(self.temp_dir / "test_layouts")
            manager = LayoutManager(config_dir)

            sidebar = {"width": 300, "position": "right"}
            header = {"height": 80}

            result = await manager.create_layout(
                "test_layout",
                "测试布局",
                "测试布局描述",
                sidebar,
                header
            )
            self.results.add_result("创建布局", result["success"])
        except Exception as e:
            self.results.add_result("创建布局", False, str(e))

    async def test_get_layout(self):
        """测试获取布局"""
        try:
            config_dir = str(self.temp_dir / "test_layouts")
            manager = LayoutManager(config_dir)

            result = await manager.get_layout("default")
            self.results.add_result("获取布局", result["success"])
        except Exception as e:
            self.results.add_result("获取布局", False, str(e))

    async def test_set_current_layout(self):
        """测试设置当前布局"""
        try:
            config_dir = str(self.temp_dir / "test_layouts")
            manager = LayoutManager(config_dir)

            result = await manager.set_current_layout("compact")
            self.results.add_result("设置当前布局", result["success"])
        except Exception as e:
            self.results.add_result("设置当前布局", False, str(e))


class UITemplateAPITests:
    """UI模板API测试"""

    def __init__(self, results: TestResults, temp_dir: Path):
        self.results = results
        self.temp_dir = temp_dir

    async def run_all(self):
        """运行所有测试"""
        print("\n[UI模板API测试]")
        await self.test_api_init()
        await self.test_api_get_config()
        await self.test_api_list_themes()
        await self.test_api_list_layouts()

    async def test_api_init(self):
        """测试API初始化"""
        try:
            config_dir = str(self.temp_dir / "test_api")
            api = UITemplateAPI(config_dir)
            self.results.add_result("API初始化", api is not None)
        except Exception as e:
            self.results.add_result("API初始化", False, str(e))

    async def test_api_get_config(self):
        """测试API获取配置"""
        try:
            config_dir = str(self.temp_dir / "test_api")
            api = UITemplateAPI(config_dir)

            result = await api.api_get_config()
            self.results.add_result("API获取配置", result["success"])
        except Exception as e:
            self.results.add_result("API获取配置", False, str(e))

    async def test_api_list_themes(self):
        """测试API列出主题"""
        try:
            config_dir = str(self.temp_dir / "test_api")
            api = UITemplateAPI(config_dir)

            result = await api.api_list_themes()
            self.results.add_result("API列出主题", result["success"])
        except Exception as e:
            self.results.add_result("API列出主题", False, str(e))

    async def test_api_list_layouts(self):
        """测试API列出布局"""
        try:
            config_dir = str(self.temp_dir / "test_api")
            api = UITemplateAPI(config_dir)

            result = await api.api_list_layouts()
            self.results.add_result("API列出布局", result["success"])
        except Exception as e:
            self.results.add_result("API列出布局", False, str(e))


async def main():
    """主测试函数"""
    print("="*60)
    print("UI模板配置模块 - 单元测试")
    print("="*60)

    # 创建临时目录
    temp_dir = Path(tempfile.mkdtemp(prefix="ui_templates_test_"))
    print(f"\n临时目录: {temp_dir}")

    results = TestResults()

    try:
        # 运行所有测试套件
        config_tests = UITemplateConfigTests(results, temp_dir)
        await config_tests.run_all()

        logo_tests = LogoManagerTests(results, temp_dir)
        await logo_tests.run_all()

        theme_tests = ThemeManagerTests(results, temp_dir)
        await theme_tests.run_all()

        layout_tests = LayoutManagerTests(results, temp_dir)
        await layout_tests.run_all()

        api_tests = UITemplateAPITests(results, temp_dir)
        await api_tests.run_all()

    finally:
        # 清理临时目录
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
            print(f"\n临时目录已清理: {temp_dir}")

    # 输出测试总结
    return results.summary()


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
