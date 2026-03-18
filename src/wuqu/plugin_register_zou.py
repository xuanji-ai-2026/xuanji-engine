"""
Plugin Register Module
Author: 邹武全 (Employee ID: 128)
Group: XJ-05 武曲星
Task: 插件注册实现
"""

from typing import Dict, List, Any, Callable, Optional
from dataclasses import dataclass
from enum import Enum


class PluginType(Enum):
    """Plugin types."""
    ACTION = "action"
    FILTER = "filter"
    STORAGE = "storage"
    ANALYTICS = "analytics"
    CUSTOM = "custom"


@dataclass
class Plugin:
    """Plugin data class."""
    plugin_id: str
    name: str
    plugin_type: PluginType
    version: str
    author: str
    enabled: bool = True


class PluginRegistry:
    """Plugin Registry Implementation"""
    
    def __init__(self):
        """Initialize the plugin registry."""
        self.plugins: Dict[str, Plugin] = {}
        self.hooks: Dict[str, List[Callable]] = {}
        
    def register(self, plugin: Plugin) -> bool:
        """
        Register a plugin.
        
        Args:
            plugin: Plugin to register
            
        Returns:
            True if successful
        """
        if plugin.plugin_id in self.plugins:
            return False
            
        self.plugins[plugin.plugin_id] = plugin
        return True
        
    def unregister(self, plugin_id: str) -> bool:
        """
        Unregister a plugin.
        
        Args:
            plugin_id: Plugin ID
            
        Returns:
            True if successful
        """
        if plugin_id in self.plugins:
            del self.plugins[plugin_id]
            return True
        return False
        
    def get_plugin(self, plugin_id: str) -> Optional[Plugin]:
        """Get plugin by ID."""
        return self.plugins.get(plugin_id)
        
    def list_plugins(self, plugin_type: Optional[PluginType] = None) -> List[Plugin]:
        """List all plugins."""
        if plugin_type:
            return [p for p in self.plugins.values() if p.plugin_type == plugin_type]
        return list(self.plugins.values())
        
    def register_hook(self, hook_name: str, callback: Callable) -> None:
        """Register a hook callback."""
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        self.hooks[hook_name].append(callback)
        
    def get_status(self) -> Dict[str, Any]:
        """Get module status."""
        return {
            "plugins_count": len(self.plugins),
            "hooks_count": len(self.hooks)
        }
        
    def get_result(self) -> Dict[str, Any]:
        """Get module result."""
        return {
            "module": "PluginRegistry",
            "version": "1.0.0",
            "status": "ready"
        }
