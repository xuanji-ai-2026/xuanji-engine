"""
辅弼星辰（扩展层）- 布局管理器
版本: v2.0
负责人: 康辅星 (162)
功能: 布局配置、管理、预览
"""

from typing import Dict, List, Optional, Any
import json
from datetime import datetime
from pathlib import Path


class LayoutManager:
    """布局管理器"""

    def __init__(self, config_dir: str = "configs/layouts"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.layouts_file = self.config_dir / "layouts.json"
        self.config_file = self.config_dir / "layout_config.json"
        self._init_layouts()

    def _init_layouts(self) -> None:
        """初始化默认布局"""
        if not self.layouts_file.exists():
            default_layouts = {
                "default": {
                    "name": "默认布局",
                    "description": "标准左右布局",
                    "sidebar": {
                        "width": 240,
                        "collapsed_width": 64,
                        "position": "left",
                        "fixed": True,
                        "collapsible": True
                    },
                    "header": {
                        "height": 64,
                        "fixed": True,
                        "show_breadcrumb": True
                    },
                    "footer": {
                        "height": 48,
                        "fixed": False
                    },
                    "content": {
                        "padding": 24,
                        "max_width": None,
                        "full_width": False
                    },
                    "created_at": datetime.now().isoformat()
                },
                "wide": {
                    "name": "宽屏布局",
                    "description": "适合宽屏的布局",
                    "sidebar": {
                        "width": 280,
                        "collapsed_width": 80,
                        "position": "left",
                        "fixed": True,
                        "collapsible": True
                    },
                    "header": {
                        "height": 64,
                        "fixed": True,
                        "show_breadcrumb": True
                    },
                    "footer": {
                        "height": 48,
                        "fixed": False
                    },
                    "content": {
                        "padding": 32,
                        "max_width": 1600,
                        "full_width": False
                    },
                    "created_at": datetime.now().isoformat()
                },
                "compact": {
                    "name": "紧凑布局",
                    "description": "节省空间的紧凑布局",
                    "sidebar": {
                        "width": 200,
                        "collapsed_width": 56,
                        "position": "left",
                        "fixed": True,
                        "collapsible": True
                    },
                    "header": {
                        "height": 56,
                        "fixed": True,
                        "show_breadcrumb": False
                    },
                    "footer": {
                        "height": 40,
                        "fixed": False
                    },
                    "content": {
                        "padding": 16,
                        "max_width": None,
                        "full_width": False
                    },
                    "created_at": datetime.now().isoformat()
                },
                "sidebar_right": {
                    "name": "右侧边栏布局",
                    "description": "边栏在右侧的布局",
                    "sidebar": {
                        "width": 280,
                        "collapsed_width": 80,
                        "position": "right",
                        "fixed": True,
                        "collapsible": True
                    },
                    "header": {
                        "height": 64,
                        "fixed": True,
                        "show_breadcrumb": True
                    },
                    "footer": {
                        "height": 48,
                        "fixed": False
                    },
                    "content": {
                        "padding": 24,
                        "max_width": None,
                        "full_width": False
                    },
                    "created_at": datetime.now().isoformat()
                },
                "top_nav": {
                    "name": "顶部导航布局",
                    "description": "无侧边栏，顶部导航布局",
                    "sidebar": {
                        "enabled": False
                    },
                    "header": {
                        "height": 80,
                        "fixed": True,
                        "show_breadcrumb": True,
                        "navigation_mode": "top"
                    },
                    "footer": {
                        "height": 48,
                        "fixed": False
                    },
                    "content": {
                        "padding": 24,
                        "max_width": None,
                        "full_width": True
                    },
                    "created_at": datetime.now().isoformat()
                }
            }
            self._save_layouts(default_layouts)

    def _load_layouts(self) -> Dict[str, Any]:
        """加载布局配置"""
        if self.layouts_file.exists():
            try:
                with open(self.layouts_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载布局失败: {e}")
                return {}
        return {}

    def _save_layouts(self, layouts: Dict[str, Any]) -> bool:
        """保存布局配置"""
        try:
            with open(self.layouts_file, 'w', encoding='utf-8') as f:
                json.dump(layouts, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存布局失败: {e}")
            return False

    async def create_layout(
        self,
        layout_id: str,
        name: str,
        description: str,
        sidebar: Dict[str, Any],
        header: Dict[str, Any],
        footer: Optional[Dict[str, Any]] = None,
        content: Optional[Dict[str, Any]] = None,
        base_layout: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        创建新布局

        Args:
            layout_id: 布局ID
            name: 布局名称
            description: 布局描述
            sidebar: 侧边栏配置
            header: 头部配置
            footer: 底部配置
            content: 内容区配置
            base_layout: 基础布局（继承配置）
        """
        layouts = self._load_layouts()

        if layout_id in layouts:
            return {
                "success": False,
                "error": f"布局ID已存在: {layout_id}"
            }

        # 验证配置
        validation = await self._validate_layout_config({
            "sidebar": sidebar,
            "header": header
        })
        if not validation["valid"]:
            return {
                "success": False,
                "error": "布局配置无效",
                "details": validation["errors"]
            }

        # 构建布局
        layout = {
            "name": name,
            "description": description,
            "sidebar": sidebar,
            "header": header,
            "footer": footer or {"height": 48, "fixed": False},
            "content": content or {"padding": 24, "max_width": None},
            "created_at": datetime.now().isoformat()
        }

        if base_layout and base_layout in layouts:
            layout["based_on"] = base_layout

        layouts[layout_id] = layout
        self._save_layouts(layouts)

        return {
            "success": True,
            "layout_id": layout_id,
            "layout": layout
        }

    async def _validate_layout_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """验证布局配置"""
        errors = []

        # 验证侧边栏
        if "sidebar" in config:
            sidebar = config["sidebar"]
            if "width" in sidebar:
                if not (64 <= sidebar["width"] <= 400):
                    errors.append("sidebar.width 应在 64-400 之间")
            if "collapsed_width" in sidebar:
                if not (48 <= sidebar["collapsed_width"] <= 100):
                    errors.append("sidebar.collapsed_width 应在 48-100 之间")

        # 验证头部
        if "header" in config:
            header = config["header"]
            if "height" in header:
                if not (48 <= header["height"] <= 120):
                    errors.append("header.height 应在 48-120 之间")

        # 验证内容区
        if "content" in config:
            content = config["content"]
            if "padding" in content:
                if not (0 <= content["padding"] <= 64):
                    errors.append("content.padding 应在 0-64 之间")

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }

    async def get_layout(self, layout_id: str) -> Dict[str, Any]:
        """获取布局配置"""
        layouts = self._load_layouts()

        if layout_id not in layouts:
            return {
                "success": False,
                "error": "布局不存在"
            }

        return {
            "success": True,
            "layout_id": layout_id,
            "layout": layouts[layout_id]
        }

    async def list_layouts(self) -> Dict[str, Any]:
        """列出所有布局"""
        layouts = self._load_layouts()

        layout_list = []
        for layout_id, layout in layouts.items():
            layout_list.append({
                "layout_id": layout_id,
                "name": layout.get("name"),
                "description": layout.get("description"),
                "created_at": layout.get("created_at")
            })

        return {
            "success": True,
            "total": len(layout_list),
            "layouts": layout_list
        }

    async def update_layout(
        self,
        layout_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """更新布局"""
        layouts = self._load_layouts()

        if layout_id not in layouts:
            return {
                "success": False,
                "error": "布局不存在"
            }

        # 验证更新
        validation = await self._validate_layout_config(updates)
        if not validation["valid"]:
            return {
                "success": False,
                "error": "布局配置无效",
                "details": validation["errors"]
            }

        # 更新布局
        layout = layouts[layout_id]
        for key, value in updates.items():
            layout[key] = value
        layout["updated_at"] = datetime.now().isoformat()

        self._save_layouts(layouts)

        return {
            "success": True,
            "layout_id": layout_id,
            "layout": layout
        }

    async def delete_layout(self, layout_id: str) -> Dict[str, Any]:
        """删除布局"""
        # 保护默认布局
        if layout_id in ["default", "wide", "compact"]:
            return {
                "success": False,
                "error": "无法删除默认布局"
            }

        layouts = self._load_layouts()

        if layout_id not in layouts:
            return {
                "success": False,
                "error": "布局不存在"
            }

        del layouts[layout_id]
        self._save_layouts(layouts)

        return {
            "success": True,
            "message": f"布局 {layout_id} 已删除"
        }

    async def set_current_layout(self, layout_id: str) -> Dict[str, Any]:
        """设置当前布局"""
        layouts = self._load_layouts()

        if layout_id not in layouts:
            return {
                "success": False,
                "error": "布局不存在"
            }

        # 保存当前布局配置
        config = {
            "current": layout_id,
            "updated_at": datetime.now().isoformat()
        }

        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            return {
                "success": True,
                "current_layout": layout_id,
                "layout": layouts[layout_id]
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"设置失败: {str(e)}"
            }

    async def get_current_layout(self) -> Dict[str, Any]:
        """获取当前布局"""
        config = {}
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            except:
                pass

        layout_id = config.get("current", "default")
        layouts = self._load_layouts()

        if layout_id not in layouts:
            layout_id = "default"

        return {
            "success": True,
            "current_layout": layout_id,
            "layout": layouts[layout_id]
        }

    async def duplicate_layout(
        self,
        source_layout_id: str,
        new_layout_id: str,
        new_name: str,
        new_description: Optional[str] = None
    ) -> Dict[str, Any]:
        """复制布局"""
        layouts = self._load_layouts()

        if source_layout_id not in layouts:
            return {
                "success": False,
                "error": "源布局不存在"
            }

        if new_layout_id in layouts:
            return {
                "success": False,
                "error": f"目标布局ID已存在: {new_layout_id}"
            }

        # 复制布局
        import copy
        new_layout = copy.deepcopy(layouts[source_layout_id])
        new_layout["name"] = new_name
        if new_description:
            new_layout["description"] = new_description
        new_layout["created_at"] = datetime.now().isoformat()
        new_layout["based_on"] = source_layout_id

        layouts[new_layout_id] = new_layout
        self._save_layouts(layouts)

        return {
            "success": True,
            "layout_id": new_layout_id,
            "layout": new_layout
        }

    async def preview_layout(self, layout_id: str) -> Dict[str, Any]:
        """生成布局预览数据"""
        result = await self.get_layout(layout_id)
        if not result["success"]:
            return result

        layout = result["layout"]

        # 计算可用空间
        preview = {
            "sidebar": layout.get("sidebar", {}),
            "header": layout.get("header", {}),
            "footer": layout.get("footer", {}),
            "content": layout.get("content", {}),
            "breakpoints": {
                "xs": 576,
                "sm": 768,
                "md": 992,
                "lg": 1200,
                "xl": 1600,
                "xxl": 2000
            }
        }

        return {
            "success": True,
            "layout_id": layout_id,
            "preview": preview
        }


__all__ = ["LayoutManager"]
