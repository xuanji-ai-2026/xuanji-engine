"""
辅弼星辰（扩展层）- 主题管理器
版本: v2.0
负责人: 康辅星 (162)
功能: 主题配置、切换、预览
"""

from typing import Dict, List, Optional, Any
import json
from datetime import datetime
from pathlib import Path
import re


class ThemeManager:
    """主题管理器"""

    def __init__(self, config_dir: str = "configs/themes"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.themes_file = self.config_dir / "themes.json"
        self.config_file = self.config_dir / "theme_config.json"
        self._init_themes()

    def _init_themes(self) -> None:
        """初始化默认主题"""
        if not self.themes_file.exists():
            default_themes = {
                "default": {
                    "name": "默认主题",
                    "description": "系统默认明亮主题",
                    "colors": {
                        "primary": "#1890ff",
                        "secondary": "#722ed1",
                        "success": "#52c41a",
                        "warning": "#faad14",
                        "error": "#f5222d",
                        "info": "#13c2c2",
                        "text": {
                            "primary": "#000000d9",
                            "secondary": "#00000073",
                            "disabled": "#00000040"
                        },
                        "background": {
                            "base": "#ffffff",
                            "elevated": "#fafafa",
                            "overlay": "#00000045"
                        },
                        "border": {
                            "base": "#d9d9d9",
                            "split": "#f0f0f0"
                        }
                    },
                    "fonts": {
                        "family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
                        "size": {
                            "small": 12,
                            "base": 14,
                            "large": 16,
                            "heading": 20
                        }
                    },
                    "created_at": datetime.now().isoformat()
                },
                "dark": {
                    "name": "深色主题",
                    "description": "深色模式主题",
                    "colors": {
                        "primary": "#177ddc",
                        "secondary": "#b37feb",
                        "success": "#49aa19",
                        "warning": "#d89614",
                        "error": "#d32030",
                        "info": "#13a8a8",
                        "text": {
                            "primary": "#ffffffd9",
                            "secondary": "#ffffff73",
                            "disabled": "#ffffff40"
                        },
                        "background": {
                            "base": "#141414",
                            "elevated": "#1f1f1f",
                            "overlay": "#00000073"
                        },
                        "border": {
                            "base": "#434343",
                            "split": "#303030"
                        }
                    },
                    "fonts": {
                        "family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
                        "size": {
                            "small": 12,
                            "base": 14,
                            "large": 16,
                            "heading": 20
                        }
                    },
                    "created_at": datetime.now().isoformat()
                },
                "compact": {
                    "name": "紧凑主题",
                    "description": "紧凑布局主题",
                    "colors": {
                        "primary": "#1890ff",
                        "secondary": "#722ed1",
                        "success": "#52c41a",
                        "warning": "#faad14",
                        "error": "#f5222d",
                        "info": "#13c2c2",
                        "text": {
                            "primary": "#000000d9",
                            "secondary": "#00000073",
                            "disabled": "#00000040"
                        },
                        "background": {
                            "base": "#ffffff",
                            "elevated": "#fafafa",
                            "overlay": "#00000045"
                        },
                        "border": {
                            "base": "#d9d9d9",
                            "split": "#f0f0f0"
                        }
                    },
                    "fonts": {
                        "family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
                        "size": {
                            "small": 11,
                            "base": 13,
                            "large": 14,
                            "heading": 18
                        }
                    },
                    "spacing": {
                        "compact": True,
                        "multiplier": 0.8
                    },
                    "created_at": datetime.now().isoformat()
                }
            }
            self._save_themes(default_themes)

    def _load_themes(self) -> Dict[str, Any]:
        """加载主题配置"""
        if self.themes_file.exists():
            try:
                with open(self.themes_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载主题失败: {e}")
                return {}
        return {}

    def _save_themes(self, themes: Dict[str, Any]) -> bool:
        """保存主题配置"""
        try:
            with open(self.themes_file, 'w', encoding='utf-8') as f:
                json.dump(themes, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存主题失败: {e}")
            return False

    async def create_theme(
        self,
        theme_id: str,
        name: str,
        description: str,
        colors: Dict[str, Any],
        fonts: Optional[Dict[str, Any]] = None,
        base_theme: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        创建新主题

        Args:
            theme_id: 主题ID
            name: 主题名称
            description: 主题描述
            colors: 颜色配置
            fonts: 字体配置
            base_theme: 基础主题（继承配置）
        """
        themes = self._load_themes()

        if theme_id in themes:
            return {
                "success": False,
                "error": f"主题ID已存在: {theme_id}"
            }

        # 验证颜色格式
        validation = await self._validate_colors(colors)
        if not validation["valid"]:
            return {
                "success": False,
                "error": "颜色配置无效",
                "details": validation["errors"]
            }

        # 构建主题
        theme = {
            "name": name,
            "description": description,
            "colors": colors,
            "created_at": datetime.now().isoformat()
        }

        if fonts:
            theme["fonts"] = fonts

        if base_theme and base_theme in themes:
            # 继承基础主题
            base_config = themes[base_theme]
            if "fonts" in base_config and "fonts" not in theme:
                theme["fonts"] = base_config["fonts"]
            if "spacing" in base_config:
                theme["spacing"] = base_config["spacing"]

        themes[theme_id] = theme
        self._save_themes(themes)

        return {
            "success": True,
            "theme_id": theme_id,
            "theme": theme
        }

    async def _validate_colors(self, colors: Dict[str, Any]) -> Dict[str, Any]:
        """验证颜色格式"""
        errors = []
        color_pattern = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')

        def validate_color_dict(color_dict, prefix=""):
            for key, value in color_dict.items():
                if isinstance(value, str):
                    if not color_pattern.match(value):
                        errors.append(f"{prefix}{key}: 无效的颜色值 {value}")
                elif isinstance(value, dict):
                    validate_color_dict(value, f"{prefix}{key}.")

        validate_color_dict(colors)

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }

    async def get_theme(self, theme_id: str) -> Dict[str, Any]:
        """获取主题配置"""
        themes = self._load_themes()

        if theme_id not in themes:
            return {
                "success": False,
                "error": "主题不存在"
            }

        return {
            "success": True,
            "theme_id": theme_id,
            "theme": themes[theme_id]
        }

    async def list_themes(self) -> Dict[str, Any]:
        """列出所有主题"""
        themes = self._load_themes()

        theme_list = []
        for theme_id, theme in themes.items():
            theme_list.append({
                "theme_id": theme_id,
                "name": theme.get("name"),
                "description": theme.get("description"),
                "created_at": theme.get("created_at")
            })

        return {
            "success": True,
            "total": len(theme_list),
            "themes": theme_list
        }

    async def update_theme(
        self,
        theme_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """更新主题"""
        themes = self._load_themes()

        if theme_id not in themes:
            return {
                "success": False,
                "error": "主题不存在"
            }

        # 如果更新颜色，验证格式
        if "colors" in updates:
            validation = await self._validate_colors(updates["colors"])
            if not validation["valid"]:
                return {
                    "success": False,
                    "error": "颜色配置无效",
                    "details": validation["errors"]
                }

        # 更新主题
        theme = themes[theme_id]
        for key, value in updates.items():
            theme[key] = value
        theme["updated_at"] = datetime.now().isoformat()

        self._save_themes(themes)

        return {
            "success": True,
            "theme_id": theme_id,
            "theme": theme
        }

    async def delete_theme(self, theme_id: str) -> Dict[str, Any]:
        """删除主题"""
        # 保护默认主题
        if theme_id in ["default", "dark", "compact"]:
            return {
                "success": False,
                "error": "无法删除默认主题"
            }

        themes = self._load_themes()

        if theme_id not in themes:
            return {
                "success": False,
                "error": "主题不存在"
            }

        del themes[theme_id]
        self._save_themes(themes)

        return {
            "success": True,
            "message": f"主题 {theme_id} 已删除"
        }

    async def set_current_theme(self, theme_id: str) -> Dict[str, Any]:
        """设置当前主题"""
        themes = self._load_themes()

        if theme_id not in themes:
            return {
                "success": False,
                "error": "主题不存在"
            }

        # 保存当前主题配置
        config = {
            "current": theme_id,
            "updated_at": datetime.now().isoformat()
        }

        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            return {
                "success": True,
                "current_theme": theme_id,
                "theme": themes[theme_id]
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"设置失败: {str(e)}"
            }

    async def get_current_theme(self) -> Dict[str, Any]:
        """获取当前主题"""
        config = {}
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            except:
                pass

        theme_id = config.get("current", "default")
        themes = self._load_themes()

        if theme_id not in themes:
            theme_id = "default"

        return {
            "success": True,
            "current_theme": theme_id,
            "theme": themes[theme_id]
        }

    async def generate_css_variables(self, theme_id: str) -> Dict[str, Any]:
        """生成CSS变量"""
        result = await self.get_theme(theme_id)
        if not result["success"]:
            return result

        theme = result["theme"]
        colors = theme.get("colors", {})
        fonts = theme.get("fonts", {})

        def flatten_colors(color_dict, prefix=""):
            vars_list = []
            for key, value in color_dict.items():
                var_name = f"--{prefix}{key}" if prefix else f"--{key}"
                if isinstance(value, str):
                    vars_list.append(f"{var_name}: {value};")
                elif isinstance(value, dict):
                    vars_list.extend(flatten_colors(value, f"{prefix}{key}-"))
            return vars_list

        css_vars = flatten_colors(colors)

        # 添加字体变量
        if "family" in fonts:
            css_vars.append(f"--font-family: {fonts['family']};")
        if "size" in fonts:
            for size_name, size_value in fonts["size"].items():
                css_vars.append(f"--font-size-{size_name}: {size_value}px;")

        return {
            "success": True,
            "theme_id": theme_id,
            "css_variables": "\n  ".join(css_vars)
        }

    async def duplicate_theme(
        self,
        source_theme_id: str,
        new_theme_id: str,
        new_name: str,
        new_description: Optional[str] = None
    ) -> Dict[str, Any]:
        """复制主题"""
        themes = self._load_themes()

        if source_theme_id not in themes:
            return {
                "success": False,
                "error": "源主题不存在"
            }

        if new_theme_id in themes:
            return {
                "success": False,
                "error": f"目标主题ID已存在: {new_theme_id}"
            }

        # 复制主题
        import copy
        new_theme = copy.deepcopy(themes[source_theme_id])
        new_theme["name"] = new_name
        if new_description:
            new_theme["description"] = new_description
        new_theme["created_at"] = datetime.now().isoformat()
        new_theme["based_on"] = source_theme_id

        themes[new_theme_id] = new_theme
        self._save_themes(themes)

        return {
            "success": True,
            "theme_id": new_theme_id,
            "theme": new_theme
        }


__all__ = ["ThemeManager"]
