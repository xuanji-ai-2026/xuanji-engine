"""
辅弼星辰（扩展层）- UI模板配置核心
版本: v2.0
负责人: 康辅星 (162)
功能: LOGO/背景/启动动画/主题/布局配置统一管理
"""

from typing import Dict, List, Optional, Any
import json
import asyncio
from datetime import datetime
from pathlib import Path
import hashlib


class UITemplateConfig:
    """UI模板配置核心管理器"""

    def __init__(self, config_dir: str = "configs/ui_templates"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.cache: Dict[str, Any] = {}
        self.config_file = self.config_dir / "ui_templates.json"
        self._load_config()

    def _load_config(self) -> None:
        """加载配置文件"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.cache.update(data)
            except Exception as e:
                print(f"加载配置失败: {e}")
                self._init_default_config()
        else:
            self._init_default_config()

    def _init_default_config(self) -> None:
        """初始化默认配置"""
        self.cache = {
            "logo": {
                "light": None,
                "dark": None,
                "width": 200,
                "height": 80,
                "format": "png"
            },
            "background": {
                "login": None,
                "dashboard": None,
                "mode": "cover"  # cover, contain, stretch
            },
            "animation": {
                "startup": None,
                "loading": None,
                "duration": 3000,
                "enabled": True
            },
            "theme": {
                "current": "default",
                "default": {
                    "primary": "#1890ff",
                    "secondary": "#722ed1",
                    "success": "#52c41a",
                    "warning": "#faad14",
                    "error": "#f5222d",
                    "text": "#000000",
                    "background": "#ffffff"
                },
                "dark": {
                    "primary": "#177ddc",
                    "secondary": "#b37feb",
                    "success": "#49aa19",
                    "warning": "#d89614",
                    "error": "#d32030",
                    "text": "#ffffff",
                    "background": "#141414"
                }
            },
            "layout": {
                "sidebar": {
                    "width": 240,
                    "collapsed_width": 64,
                    "position": "left",
                    "fixed": True
                },
                "header": {
                    "height": 64,
                    "fixed": True
                },
                "content": {
                    "padding": 24,
                    "max_width": None
                }
            },
            "version": "2.0",
            "updated_at": datetime.now().isoformat()
        }
        self._save_config()

    def _save_config(self) -> bool:
        """保存配置到文件"""
        try:
            self.cache["updated_at"] = datetime.now().isoformat()
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存配置失败: {e}")
            return False

    async def get_config(self, key: str) -> Optional[Any]:
        """获取配置项"""
        keys = key.split('.')
        value = self.cache
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return None
        return value

    async def set_config(self, key: str, value: Any) -> bool:
        """设置配置项"""
        keys = key.split('.')
        config = self.cache
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        return self._save_config()

    async def update_config(self, updates: Dict[str, Any]) -> bool:
        """批量更新配置"""
        def deep_update(target: Dict, source: Dict) -> None:
            for key, value in source.items():
                if isinstance(value, dict) and isinstance(target.get(key), dict):
                    deep_update(target[key], value)
                else:
                    target[key] = value

        deep_update(self.cache, updates)
        return self._save_config()

    async def reset_config(self, key: str) -> bool:
        """重置配置项为默认值"""
        default_config = UITemplateConfig(str(self.config_dir))
        default_config._init_default_config()
        default_value = await default_config.get_config(key)
        return await self.set_config(key, default_value)

    async def export_config(self) -> Dict[str, Any]:
        """导出完整配置"""
        return {
            "data": self.cache,
            "checksum": self._calculate_checksum(),
            "exported_at": datetime.now().isoformat()
        }

    async def import_config(self, config_data: Dict[str, Any]) -> bool:
        """导入配置"""
        if "data" not in config_data:
            return False
        self.cache = config_data["data"]
        return self._save_config()

    def _calculate_checksum(self) -> str:
        """计算配置校验和"""
"""
辅弼星辰（扩展层）- UI模板配置核心
版本: v2.0
负责人: 康辅星 (162)
功能: LOGO/背景/启动动画/主题/布局配置统一管理
"""

from typing import Dict, List, Optional, Any
import json
import asyncio
from datetime import datetime
from pathlib import Path
import hashlib


class UITemplateConfig:
    """UI模板配置核心管理器"""

    def __init__(self, config_dir: str = "configs/ui_templates"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.cache: Dict[str, Any] = {}
        self.config_file = self.config_dir / "ui_templates.json"
        self._load_config()

    def _load_config(self) -> None:
        """加载配置文件"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.cache.update(data)
            except Exception as e:
                print(f"加载配置失败: {e}")
                self._init_default_config()
        else:
            self._init_default_config()

    def _init_default_config(self) -> None:
        """初始化默认配置"""
        self.cache = {
            "logo": {
                "light": None,
                "dark": None,
                "width": 200,
                "height": 80,
                "format": "png"
            },
            "background": {
                "login": None,
                "dashboard": None,
                "mode": "cover"  # cover, contain, stretch
            },
            "animation": {
                "startup": None,
                "loading": None,
                "duration": 3000,
                "enabled": True
            },
            "theme": {
                "current": "default",
                "default": {
                    "primary": "#1890ff",
                    "secondary": "#722ed1",
                    "success": "#52c41a",
                    "warning": "#faad14",
                    "error": "#f5222d",
                    "text": "#000000",
                    "background": "#ffffff"
                },
                "dark": {
                    "primary": "#177ddc",
                    "secondary": "#b37feb",
                    "success": "#49aa19",
                    "warning": "#d89614",
                    "error": "#d32030",
                    "text": "#ffffff",
                    "background": "#141414"
                }
            },
            "layout": {
                "sidebar": {
                    "width": 240,
                    "collapsed_width": 64,
                    "position": "left",
                    "fixed": True
                },
                "header": {
                    "height": 64,
                    "fixed": True
                },
                "content": {
                    "padding": 24,
                    "max_width": None
                }
            },
            "version": "2.0",
            "updated_at": datetime.now().isoformat()
        }
        self._save_config()

    def _save_config(self) -> bool:
        """保存配置到文件"""
        try:
            self.cache["updated_at"] = datetime.now().isoformat()
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存配置失败: {e}")
            return False

    async def get_config(self, key: str) -> Optional[Any]:
        """获取配置项"""
        keys = key.split('.')
        value = self.cache
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return None
        return value

    async def set_config(self, key: str, value: Any) -> bool:
        """设置配置项"""
        keys = key.split('.')
        config = self.cache
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        return self._save_config()

    async def update_config(self, updates: Dict[str, Any]) -> bool:
        """批量更新配置"""
        def deep_update(target: Dict, source: Dict) -> None:
            for key, value in source.items():
                if isinstance(value, dict) and isinstance(target.get(key), dict):
                    deep_update(target[key], value)
                else:
                    target[key] = value

        deep_update(self.cache, updates)
        return self._save_config()

    async def reset_config(self, key: str) -> bool:
        """重置配置项为默认值"""
        default_config = UITemplateConfig(str(self.config_dir))
        default_config._init_default_config()
        default_value = await default_config.get_config(key)
        return await self.set_config(key, default_value)

    async def export_config(self) -> Dict[str, Any]:
        """导出完整配置"""
        return {
            "data": self.cache,
            "checksum": self._calculate_checksum(),
            "exported_at": datetime.now().isoformat()
        }

    async def import_config(self, config_data: Dict[str, Any]) -> bool:
        """导入配置"""
        if "data" not in config_data:
            return False
        self.cache = config_data["data"]
        return self._save_config()

    def _calculate_checksum(self) -> str:
        """计算配置校验和"""
        data = json.dumps(self.cache, sort_keys=True).encode('utf-8')
        return hashlib.md5(data).hexdigest()

    async def validate_config(self) -> Dict[str, Any]:
        """验证配置有效性"""
        errors = []
        warnings = []

        # 验证主题颜色格式
        for theme_name, theme in self.cache.get("theme", {}).items():
            if theme_name == "current":
                continue
            if isinstance(theme, dict):
                for color_key, color_value in theme.items():
                    if isinstance(color_value, str) and color_value.startswith('#'):
                        if len(color_value) not in [4, 7]:
                            errors.append(
                                f"主题 {theme_name} 的颜色 {color_key} 格式无效: {color_value}"
                            )

        # 验证布局尺寸
        layout = self.cache.get("layout", {})
        if "sidebar" in layout:
            sidebar = layout["sidebar"]
            if sidebar.get("width", 0) < 64 or sidebar.get("width", 0) > 400:
                warnings.append("侧边栏宽度超出推荐范围 (64-400px)")
            if sidebar.get("collapsed_width", 0) < 48 or sidebar.get("collapsed_width", 0) > 100:
                warnings.append("侧边栏折叠宽度超出推荐范围 (48-100px)")

        if "header" in layout:
            header = layout["header"]
            if header.get("height", 0) < 48 or header.get("height", 0) > 100:
                warnings.append("头部高度超出推荐范围 (48-100px)")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }

    async def get_theme_preview(self, theme_name: str) -> Dict[str, Any]:
        """获取主题预览数据"""
        theme = self.cache.get("theme", {}).get(theme_name)
        if not theme:
            return {"error": "主题不存在"}
        return {
            "name": theme_name,
            "colors": theme,
            "preview": self._generate_theme_preview(theme)
        }

    def _generate_theme_preview(self, theme: Dict[str, str]) -> Dict[str, str]:
        """生成主题预览样式"""
        return {
            "primary_bg": theme.get("primary", "#1890ff"),
            "primary_text": "#ffffff",
            "success_bg": theme.get("success", "#52c41a"),
            "warning_bg": theme.get("warning", "#faad14"),
            "error_bg": theme.get("error", "#f5222d"),
            "body_bg": theme.get("background", "#ffffff"),
            "text_color": theme.get("text", "#000000")
        }


__all__ = ["UITemplateConfig"]
