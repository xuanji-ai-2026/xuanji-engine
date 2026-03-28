"""
辅弼星辰（扩展层）- UI模板配置RESTful API
版本: v2.0
负责人: 康辅星 (162)
功能: 提供UI模板配置的RESTful API接口
"""

from typing import Dict, List, Optional, Any
import asyncio
from datetime import datetime
from .ui_template_config import UITemplateConfig
from .logo_manager import LogoManager
from .background_manager import BackgroundManager
from .animation_manager import AnimationManager
from .theme_manager import ThemeManager
from .layout_manager import LayoutManager


class UITemplateAPI:
    """UI模板配置RESTful API"""

    def __init__(self, config_dir: str = "configs/ui_templates"):
        self.config = UITemplateConfig(config_dir)
        self.logo_manager = LogoManager()
        self.background_manager = BackgroundManager()
        self.animation_manager = AnimationManager()
        self.theme_manager = ThemeManager()
        self.layout_manager = LayoutManager()

    # ========== 核心配置API ==========

    async def api_get_config(self, key: str = None) -> Dict[str, Any]:
        """GET /api/ui_templates/config - 获取配置"""
        if key:
            value = await self.config.get_config(key)
            return {
                "success": True,
                "key": key,
                "value": value
            }
        else:
            return {
                "success": True,
                "config": await self.config.export_config()
            }

    async def api_set_config(self, key: str, value: Any) -> Dict[str, Any]:
        """PUT /api/ui_templates/config - 设置配置"""
        success = await self.config.set_config(key, value)
        return {
            "success": success,
            "key": key,
            "message": "配置已更新" if success else "配置更新失败"
        }

    async def api_update_config(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        """PATCH /api/ui_templates/config - 批量更新配置"""
        success = await self.config.update_config(updates)
        return {
            "success": success,
            "message": "配置已更新" if success else "配置更新失败"
        }

    async def api_reset_config(self, key: str) -> Dict[str, Any]:
        """POST /api/ui_templates/config/reset - 重置配置"""
        success = await self.config.reset_config(key)
        return {
            "success": success,
            "key": key,
            "message": "配置已重置" if success else "配置重置失败"
        }

    async def api_validate_config(self) -> Dict[str, Any]:
        """GET /api/ui_templates/config/validate - 验证配置"""
        return await self.config.validate_config()

    async def api_export_config(self) -> Dict[str, Any]:
        """GET /api/ui_templates/config/export - 导出配置"""
        return await self.config.export_config()

    async def api_import_config(self, config_data: Dict[str, Any]) -> Dict[str, Any]:
        """POST /api/ui_templates/config/import - 导入配置"""
        success = await self.config.import_config(config_data)
        return {
            "success": success,
            "message": "配置已导入" if success else "配置导入失败"
        }

    # ========== LOGO管理API ==========

    async def api_upload_logo(
        self,
        file_data: bytes,
        filename: str,
        theme: str = "light",
        resize: Optional[Dict[str, int]] = None
    ) -> Dict[str, Any]:
        """POST /api/ui_templates/logo/upload - 上传LOGO"""
        return await self.logo_manager.upload_logo(file_data, filename, theme, resize)

    async def api_get_logo(self, file_id: str) -> Dict[str, Any]:
        """GET /api/ui_templates/logo/:id - 获取LOGO信息"""
        return await self.logo_manager.get_logo_info(file_id)

    async def api_list_logos(self, theme: Optional[str] = None) -> Dict[str, Any]:
        """GET /api/ui_templates/logo - 列出所有LOGO"""
        return await self.logo_manager.list_logos(theme)

    async def api_delete_logo(self, file_id: str) -> Dict[str, Any]:
        """DELETE /api/ui_templates/logo/:id - 删除LOGO"""
        return await self.logo_manager.delete_logo(file_id)

    async def api_set_default_logo(self, theme: str, file_id: str) -> Dict[str, Any]:
        """POST /api/ui_templates/logo/default - 设置默认LOGO"""
        return await self.logo_manager.set_default_logo(theme, file_id)

    async def api_get_default_logo(self, theme: str) -> Dict[str, Any]:
        """GET /api/ui_templates/logo/default/:theme - 获取默认LOGO"""
        file_id = await self.logo_manager.get_default_logo(theme)
        return {
            "success": file_id is not None,
            "theme": theme,
            "file_id": file_id
        }

    # ========== 背景管理API ==========

    async def api_upload_background(
        self,
        file_data: bytes,
        filename: str,
        page: str = "login",
        description: str = ""
    ) -> Dict[str, Any]:
        """POST /api/ui_templates/background/upload - 上传背景"""
        return await self.background_manager.upload_background(file_data, filename, page, description)

    async def api_get_background(self, file_id: str) -> Dict[str, Any]:
        """GET /api/ui_templates/background/:id - 获取背景信息"""
        return await self.background_manager.get_background_info(file_id)

    async def api_list_backgrounds(self, page: Optional[str] = None) -> Dict[str, Any]:
        """GET /api/ui_templates/background - 列出所有背景"""
        return await self.background_manager.list_backgrounds(page)

    async def api_delete_background(self, file_id: str) -> Dict[str, Any]:
        """DELETE /api/ui_templates/background/:id - 删除背景"""
        return await self.background_manager.delete_background(file_id)

    async def api_set_background(
        self,
        page: str,
        file_id: Optional[str] = None,
        mode: str = "cover"
    ) -> Dict[str, Any]:
        """POST /api/ui_templates/background/set - - 设置页面背景"""
        return await self.background_manager.set_background(page, file_id, mode)

    async def api_get_page_background(self, page: str) -> Dict[str, Any]:
        """GET /api/ui_templates/background/page/:page - 获取页面背景"""
        return await self.background_manager.get_page_background(page)

    # ========== 动画管理API ==========

    async def api_upload_animation(
        self,
        file_data: bytes,
        filename: str,
        anim_type: str = "startup",
        duration: Optional[int] = None,
        description: str = ""
    ) -> Dict[str, Any]:
        """POST /api/ui_templates/animation/upload - 上传动画"""
        return await self.animation_manager.upload_animation(file_data, filename, anim_type, duration, description)

    async def api_get_animation(self, file_id: str) -> Dict[str, Any]:
        """GET /api/ui_templates/animation/:id - 获取动画信息"""
        return await self.animation_manager.get_animation_info(file_id)

    async def api_list_animations(self, anim_type: Optional[str] = None) -> Dict[str, Any]:
        """GET /api/ui_templates/animation - 列出所有动画"""
        return await self.animation_manager.list_animations(anim_type)

    async def api_delete_animation(self, file_id: str) -> Dict[str, Any]:
        """DELETE /api/ui_templates/animation/:id - 删除动画"""
        return await self.animation_manager.delete_animation(file_id)

    async def api_set_animation(
        self,
        anim_type: str,
        file_id: Optional[str] = None,
        enabled: bool = True
    ) -> Dict[str, Any]:
        """POST /api/ui_templates/animation/set - 设置动画"""
        return await self.animation_manager.set_animation(anim_type, file_id, enabled)

    async def api_get_animation_config(self, anim_type: str) -> Dict[str, Any]:
        """GET /api/ui_templates/animation/config/:type - 获取动画配置"""
        return await self.animation_manager.get_animation_config(anim_type)

    async def api_create_lottie_animation(
        self,
        name: str,
        properties: Dict[str, Any]
    ) -> Dict[str, Any]:
        """POST /api/ui_templates/animation/lottie - 创建Lottie动画"""
        return await self.animation_manager.create_lottie_animation(name, properties)

    # ========== 主题管理API ==========

    async def api_create_theme(
        self,
        theme_id: str,
        name: str,
        description: str,
        colors: Dict[str, Any],
        fonts: Optional[Dict[str, Any]] = None,
        base_theme: Optional[str] = None
    ) -> Dict[str, Any]:
        """POST /api/ui_templates/theme - 创建主题"""
        return await self.theme_manager.create_theme(theme_id, name, description, colors, fonts, base_theme)

    async def api_get_theme(self, theme_id: str) -> Dict[str, Any]:
        """GET /api/ui_templates/theme/:id - 获取主题"""
        return await self.theme_manager.get_theme(theme_id)

    async def api_list_themes(self) -> Dict[str, Any]:
        """GET /api/ui_templates/theme - 列出所有主题"""
        return await self.theme_manager.list_themes()

    async def api_update_theme(
        self,
        theme_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """PUT /api/ui_templates/theme/:id - 更新主题"""
        return await self.theme_manager.update_theme(theme_id, updates)

    async def api_delete_theme(self, theme_id: str) -> Dict[str, Any]:
        """DELETE /api/ui_templates/theme/:id - 删除主题"""
        return await self.theme_manager.delete_theme(theme_id)

    async def api_set_current_theme(self, theme_id: str) -> Dict[str, Any]:
        """POST /api/ui_templates/theme/current - 设置当前主题"""
        return await self.theme_manager.set_current_theme(theme_id)

    async def api_get_current_theme(self) -> Dict[str, Any]:
        """GET /api/ui_templates/theme/current - 获取当前主题"""
        return await self.theme_manager.get_current_theme()

    async def api_get_theme_css_variables(self, theme_id: str) -> Dict[str, Any]:
        """GET /api/ui_templates/theme/:id/css - 获取主题CSS变量"""
        return await self.theme_manager.generate_css_variables(theme_id)

    async def api_duplicate_theme(
        self,
        source_theme_id: str,
        new_theme_id: str,
        new_name: str,
        new_description: Optional[str] = None
    ) -> Dict[str, Any]:
        """POST /api/ui_templates/theme/duplicate - 复制主题"""
        return await self.theme_manager.duplicate_theme(source_theme_id, new_theme_id, new_name, new_description)

    async def api_get_theme_preview(self, theme_id: str) -> Dict[str, Any]:
        """GET /api/ui_templates/theme/:id/preview - 获取主题预览"""
        return await self.theme_manager.generate_css_variables(theme_id)

    # ========== 布局管理API ==========

    async def api_create_layout(
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
        """POST /api/ui_templates/layout - 创建布局"""
        return await self.layout_manager.create_layout(
            layout_id, name, description, sidebar, header, footer, content, base_layout
        )

    async def api_get_layout(self, layout_id: str) -> Dict[str, Any]:
        """GET /api/ui_templates/layout/:id - 获取布局"""
        return await self.layout_manager.get_layout(layout_id)

    async def api_list_layouts(self) -> Dict[str, Any]:
        """GET /api/ui_templates/layout - 列出所有布局"""
        return await self.layout_manager.list_layouts()

    async def api_update_layout(
        self,
        layout_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """PUT /api/ui_templates/layout/:id - 更新布局"""
        return await self.layout_manager.update_layout(layout_id, updates)

    async def api_delete_layout(self, layout_id: str) -> Dict[str, Any]:
        """DELETE /api/ui_templates/layout/:id - 删除布局"""
        return await self.layout_manager.delete_layout(layout_id)

    async def api_set_current_layout(self, layout_id: str) -> Dict[str, Any]:
        """POST /api/ui_templates/layout/current - 设置当前布局"""
        return await self.layout_manager.set_current_layout(layout_id)

    async def api_get_current_layout(self) -> Dict[str, Any]:
        """GET /api/ui_templates/layout/current - 获取当前布局"""
        return await self.layout_manager.get_current_layout()

    async def api_duplicate_layout(
        self,
        source_layout_id: str,
        new_layout_id: str,
        new_name: str,
        new_description: new_description[str] = None
    ) -> Dict[str, Any]:
        """POST /api/ui_templates/layout/duplicate - 复制布局"""
        return await self.layout_manager.duplicate_layout(source_layout_id, new_layout_id, new_name, new_description)

    async def api_preview_layout(self, layout_id: str) -> Dict[str, Any]:
        """GET /api/ui_templates/layout/:id/preview - 预览布局"""
        return await self.layout_manager.preview_layout(layout_id)

    # ========== 综合API ==========

    async def api_get_all_configs(self) -> Dict[str, Any]:
        """GET /api/ui_templates/all - 获取所有配置"""
        return {
            "success": True,
            "config": await self.config.export_config(),
            "current_theme": await self.theme_manager.get_current_theme(),
            "current_layout": await self.get_current_layout()
        }

    async def api_get_status(self) -> Dict[str, Any]:
        """GET /api/ui_templates/status - 获取系统状态"""
        logos = await self.logo_manager.list_logos()
        backgrounds = await self.background_manager.list_backgrounds()
        animations = await self.animation_manager.list_animations()
        themes = await self.theme_manager.list_themes()
        layouts = await self.layout_manager.list_layouts()

        return {
            "success": True,
            "status": {
                "logos": logos.get("total", 0),
                "backgrounds": backgrounds.get("total", 0),
                "animations": animations.get("total", 0),
                "themes": themes.get("total", 0),
                "layouts": layouts.get("total", 0)
            },
            "config_version": await self.config.get_config("version"),
            "updated_at": await self.config.get_config("updated_at")
        }


# ========== API路由定义 ==========

def get_api_routes() -> List[Dict[str, Any]]:
    """获取所有API路由定义"""
    return [
        # 核心配置
        {"method": "GET", "path": "/api/ui_templates/config", "handler": "api_get_config"},
        {"method": "PUT", "path": "/api/ui_templates/config", "handler": "api_set_config"},
        {"method": "PATCH", "path": "/api/ui_templates/config", "handler": "api_update_config"},
        {"method": "POST", "path": "/api/ui_templates/config/reset", "handler": "api_reset_config"},
        {"method": "GET", "path": "/api/ui_templates/config/validate", "handler": "api_validate_config"},
        {"method": "GET", "path": "/api/ui_templates/config/export", "handler": "api_export_config"},
        {"method": "POST", "path": "/api/ui_templates/config/import", "handler": "api_import_config"},

        # LOGO管理
        {"method": "POST", "path": "/api/ui_templates/logo/upload", "handler": "api_upload_logo"},
        {"method": "GET", "path": "/api/ui_templates/logo", "handler": "api_list_logos"},
        {"method": "GET", "path": "/api/ui_templates/logo/{id}", "handler": "api_get_logo"},
        {"method": "DELETE", "path": "/api/ui_templates/logo/{id}", "handler": "api_delete_logo"},
        {"method": "POST", "path": "/api/ui_templates/logo/default", "handler": "api_set_default_logo"},
        {"method": "GET", "path": "/api/ui_templates/logo/default/{theme}", "handler": "api_get_default_logo"},

        # 背景管理
        {"method": "POST", "path": "/api/ui_templates/background/upload", "handler": "api_upload_background"},
        {"method": "GET", "path": "/api/ui_templates/background", "handler": "api_list_backgrounds"},
        {"method": "GET", "path": "/api/ui_templates/background/{id}", "handler": "api_get_background"},
        {"method": "DELETE", "path": "/api/ui_templates/background/{id}", "handler": "api_delete_background"},
        {"method": "POST", "path": "/api/ui_templates/background/set", "handler": "api_set_background"},
        {"method": "GET", "path": "/api/ui_templates/background/page/{page}", "handler": "api_get_page_background"},

        # 动画管理
        {"method": "POST", "path": "/api/ui_templates/animation/upload", "handler": "api_upload_animation"},
        {"method": "GET", "path": "/api/ui_templates/animation", "handler": "api_list_animations"},
        {"method": "GET", "path": "/api/ui_templates/animation/{id}", "handler": "api_get_animation"},
        {"method": "DELETE", "path": "/api/ui_templates/animation/{id}", "handler": "api_delete_animation"},
        {"method": "POST", "path": "/api/ui_templates/animation/set", "handler": "api_set_animation"},
        {"method": "GET", "path": "/api/ui_templates/animation/config/{type}", "handler": "api_get_animation_config"},
        {"method": "POST", "path": "/api/ui_templates/animation/lottie", "handler": "api_create_lottie_animation"},

        # 主题管理
        {"method": "POST", "path": "/api/ui_templates/theme", "handler": "api_create_theme"},
        {"method": "GET", "path": "/api/ui_templates/theme", "handler": "api_list_themes"},
        {"method": "GET", "path": "/api/ui_templates/theme/{id}", "handler": "api_get_theme"},
        {"method": "PUT", "path": "/api/ui_templates/theme/{id}", "handler": "api_update_theme"},
        {"method": "DELETE", "path": "/api/ui_templates/theme/{id}", "handler": "api_delete_theme"},
        {"method": "POST", "path": "/api/ui_templates/theme/current", "handler": "api_set_current_theme"},
        {"method": "GET", "path": "/api/ui_templates/theme/current", "handler": "api_get_current_theme"},
        {"method": "GET", "path": "/api/ui_templates/theme/{id}/css", "handler": "api_get_theme_css_variables"},
        {"method": "GET", "path": "/api/ui_templates/theme/{id}/preview", "handler": "api_get_theme_preview"},
        {"method": "POST", "path": "/api/ui_templates/theme/duplicate", "handler": "api_duplicate_theme"},

        # 布局管理
        {"method": "POST", "path": "/api/ui_templates/layout", "handler": "api_create_layout"},
        {"method": "GET", "path": "/api/ui_templates/layout", "handler": "api_list_layouts"},
        {"method": "GET", "path": "/api/ui_templates/layout/{id}", "handler": "api_get_layout"},
        {"method": "PUT", "path": "/api/ui_templates/layout/{id}", "handler": "api_update_layout"},
        {"method": "DELETE", "path": "/api/ui_templates/layout/{id}", "handler": "api_delete_layout"},
        {"method": "POST", "path": "/api/ui_templates/layout/current", "handler": "api_set_current_layout"},
        {"method": "GET", "path": "/api/ui_templates/layout/current", "handler": "api_get_current_layout"},
        {"method": "GET", "path": "/api/ui_templates/layout/{id}/preview", "handler": "api_preview_layout"},
        {"method": "POST", "path": "/api/ui_templates/layout/duplicate", "handler": "api_duplicate_layout"},

        # 综合API
        {"method": "GET", "path": "/api/ui_templates/all", "handler": "api_get_all_configs"},
        {"method": "GET", "path": "/api/ui_templates/status", "handler": "api_get_status"},
    ]


__all__ = ["UITemplateAPI", "get_api_routes"]
