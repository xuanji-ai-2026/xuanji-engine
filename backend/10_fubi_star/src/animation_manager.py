"""
辅弼星辰（扩展层）- 动画管理器
版本: v2.0
负责人: 康辅星 (162)
功能: 启动动画、加载动画管理
"""

from typing import Dict, List, Optional, Any
import asyncio
from pathlib import Path
import json
from datetime import datetime


class AnimationManager:
    """动画管理器"""

    def __init__(self, storage_dir: str = "storage/animations", max_size_mb: int = 5):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.allowed_formats = {'.gif', '.lottie', '.json', '.mp4', '.webm'}
        self.animation_types = ['startup', 'loading', 'transition']

    async def upload_animation(
        self,
        file_data: bytes,
        filename: str,
        anim_type: str = "startup",
        duration: Optional[int] = None,
        description: str = ""
    ) -> Dict[str, Any]:
        """
        上传动画文件

        Args:
            file_data: 文件二进制数据
            filename: 文件名
            anim_type: 动画类型 (startup/loading/transition)
            duration: 动画时长（毫秒）
            description: 动画描述
        """
        # 验证动画类型
        if anim_type not in self.animation_types:
            return {
                "success": False,
                "error": f"无效的动画类型: {anim_type}"
            }

        # 验证文件格式
        ext = Path(filename).suffix.lower()
        if ext not in self.allowed_formats:
            return {
                "success": False,
                "error": f"不支持的文件格式: {ext}"
            }

        # 验证文件大小
        if len(file_data) > self.max_size_bytes:
            return {
                "success": False,
                "error": f"文件大小超过限制 ({self.max_size_bytes // 1024 // 1024}MB)"
            }

        try:
            # 生成唯一文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_id = f"{anim_type}_{timestamp}{ext}"
            file_path = self.storage_dir / file_id

            # 保存文件
            with open(file_path, 'wb') as f:
                f.write(file_data)

            # 解析动画信息
            anim_info = {
                "file_id": file_id,
                "url": f"/api/ui_templates/animation/{file_id}",
                "type": anim_type,
                "format": ext[1:],
                "duration": duration,
                "description": description,
                "uploaded_at": datetime.now().isoformat()
            }

            # 如果是Lottie动画，解析元数据
            if ext == '.json':
                try:
                    lottie_data = json.loads(file_data.decode('utf-8'))
                    if "w" in lottie_data and "h" in lottie_data:
                        anim_info["width"] = lottie_data["w"]
                        anim_info["height"] = lottie_data["h"]
                    if "fr" in lottie_data:
                        anim_info["frame_rate"] = lottie_data["fr"]
                        if "op" in lottie_data and "ip" in lottie_data:
                            anim_info["duration"] = int((lottie_data["op"] - lottie_data["ip"]) / lottie_data["fr"] * 1000)
                except:
                    pass

            # 保存动画元数据
            metadata_file = self.storage_dir / "metadata.json"
            if metadata_file.exists():
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
            else:
                metadata = {}

            metadata[file_id] = anim_info
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

            return {
                "success": True,
                **anim_info
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"上传失败: {str(e)}"
            }

    async def get_animation_info(self, file_id: str) -> Dict[str, Any]:
        """获取动画信息"""
        metadata_file = self.storage_dir / "metadata.json"
        if not metadata_file.exists():
            return {
                "success": False,
                "error": "元数据不存在"
            }

        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)

            if file_id in metadata:
                return {
                    "success": True,
                    **metadata[file_id]
                }
            else:
                return {
                    "success": False,
                    "error": "动画不存在"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"获取信息失败: {str(e)}"
            }

    async def list_animations(self, anim_type: Optional[str] = None) -> Dict[str, Any]:
        """列出所有动画"""
        metadata_file = self.storage_dir / "metadata.json"
        if not metadata_file.exists():
            return {
                "success": True,
                "total": 0,
                "animations": []
            }

        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)

            animations = []
            for file_id, info in metadata.items():
                if anim_type is None or info.get("type") == anim_type:
                    animations.append({
                        "success": True,
                        **info
                    })

            return {
                "success": True,
                "total": len(animations),
                "animations": animations
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"列表获取失败: {str(e)}"
            }

    async def delete_animation(self, file_id: str) -> Dict[str, Any]:
        """删除动画"""
        file_path = self.storage_dir / file_id
        if not file_path.exists():
            return {
                "success": False,
                "error": "文件不存在"
            }

        try:
            # 删除文件
            file_path.unlink()

            # 删除元数据
            metadata_file = self.storage_dir / "metadata.json"
            if metadata_file.exists():
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)

                if file_id in metadata:
                    del metadata[file_id]

                with open(metadata_file, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=2, ensure_ascii=False)

            return {
                "success": True,
                "message": f"动画 {file_id} 已删除"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"删除失败: {str(e)}"
            }

    async def set_animation(
        self,
        anim_type: str,
        file_id: Optional[str] = None,
        enabled: bool = True
    ) -> Dict[str, Any]:
        """
        设置默认动画

        Args:
            anim_type: 动画类型
            file_id: 动画文件ID（None表示清除）
            enabled: 是否启用
        """
        if anim_type not in self.animation_types:
            return {
                "success": False,
                "error": f"无效的动画类型: {anim_type}"
            }

        if file_id:
            file_path = self.storage_dir / file_id
            if not file_path.exists():
                return {
                    "success": False,
                    "error": "动画文件不存在"
                }

        # 保存动画配置
        config_file = self.storage_dir / "animation_config.json"
        try:
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                config = {}

            config[anim_type] = {
                "file_id": file_id,
                "enabled": enabled,
                "updated_at": datetime.now().isoformat()
            }

            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            return {
                "success": True,
                "message": f"动画配置已更新",
                "type": anim_type,
                "file_id": file_id,
                "enabled": enabled
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"设置失败: {str(e)}"
            }

    async def get_animation_config(self, anim_type: str) -> Dict[str, Any]:
        """获取动画配置"""
        config_file = self.storage_dir / "animation_config.json"
        if not config_file.exists():
            return {
                "success": True,
                "type": anim_type,
                "animation": None
            }

        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            if anim_type in config:
                anim_config = config[anim_type]
                file_id = anim_config.get("file_id")
                if file_id:
                    anim_info = await self.get_animation_info(file_id)
                    anim_info.update({
                        "enabled": anim_config.get("enabled"),
                        "updated_at": anim_config.get("updated_at")
                    })
                    return {
                        "success": True,
                        "type": anim_type,
                        "animation": anim_info
                    }

            return {
                "success": True,
                "type": anim_type,
                "animation": None
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"获取失败: {str(e)}"
            }

    async def create_lottie_animation(
        self,
        name: str,
        properties: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        创建Lottie动画（程序化生成）

        Args:
            name: 动画名称
            properties: 动画属性（宽度、高度、颜色、动画类型等）
        """
        try:
            # 简化的Lottie动画模板
            lottie_template = {
                "v": "5.7.0",
                "fr": properties.get("frame_rate", 60),
                "ip": 0,
                "op": properties.get("duration", 100) * properties.get("frame_rate", 60) / 1000,
                "w": properties.get("width", 500),
                "h": properties.get("height", 500),
                "nm": name,
                "ddd": 0,
                "assets": [],
                "layers": [
                    {
                        "ddd": 0,
                        "ind": 1,
                        "ty": 4,
                        "nm": "Shape Layer 1",
                        "ks": {
                            "o": {"a": 0, "k": 100},
                            "r": {"a": 0, "k": 0},
                            "p": {"a": 0, "k": [250, 250, 0]},
                            "a": {"a": 0, "k": [0, 0, 0]},
                            "s": {"a": 0, "k": [100, 100, 100]}
                        },
                        "shapes": [
                            {
                                "ty": "gr",
                                "nm": "Group 1",
                                "it": [
                                    {
                                        "ty": "el",
                                        "nm": "Ellipse Path 1",
                                        "d": 1,
                                        "p": {"a": 0, "k": [0, 0]},
                                        "s": {"a": 0, "k": [100, 100]}
                                    },
                                    {
                                        "ty": "fl",
                                        "c": {"a": 0, "k": properties.get("color", [0.07, 0.56, 1, 1])},
                                        "o": {"a": 0, "k": 100}
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }

            # 转换为JSON并保存
            file_data = json.dumps(lottie_template).encode('utf-8')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_{timestamp}.json"

            result = await self.upload_animation(
                file_data,
                filename,
                anim_type=properties.get("type", "startup"),
                duration=properties.get("duration"),
                description=f"程序生成的Lottie动画: {name}"
            )

            return result

        except Exception as e:
            return {
                "success": False,
                "error": f"创建动画失败: {str(e)}"
            }


__all__ = ["AnimationManager"]
