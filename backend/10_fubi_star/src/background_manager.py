"""
辅弼星辰（扩展层）- 背景管理器
版本: v2.0
负责人: 康辅星 (162)
功能: 背景上传、管理、预览
"""

from typing import Dict, List, Optional, Any
import asyncio
from pathlib import Path
import shutil
from datetime import datetime
from PIL import Image
import io


class BackgroundManager:
    """背景管理器"""

    def __init__(self, storage_dir: str = "storage/backgrounds", max_size_mb: int = 10):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.allowed_formats = {'.png', '.jpg', '.jpeg', '.webp'}
        self.display_modes = ['cover', 'contain', 'stretch', 'tile']

    async def upload_background(
        self,
        file_data: bytes,
        filename: str,
        page: str = "login",
        description: str = ""
    ) -> Dict[str, Any]:
        """
        上传背景图片

        Args:
            file_data: 文件二进制数据
            filename: 文件名
            page: 适用页面 (login/dashboard/...)
            description: 背景描述
        """
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
            # 验证图片
            image = Image.open(io.BytesIO(file_data))
            width, height = image.size

            # 生成唯一文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_id = f"{page}_{timestamp}{ext}"
            file_path = self.storage_dir / file_id

            # 保存图片
            image.save(file_path, format=ext[1:].upper())

            # 保存缩略图
            thumbnail_path = self.storage_dir / "thumbnails" / f"{file_id}.thumb{ext}"
            thumbnail_path.parent.mkdir(exist_ok=True)
            thumbnail = image.copy()
            thumbnail.thumbnail((300, 300), Image.Resampling.LANCZOS)
            thumbnail.save(thumbnail_path, format=ext[1:].upper())

            return {
                "success": True,
                "file_id": file_id,
                "url": f"/api/ui_templates/background/{file_id}",
                "thumbnail_url": f"/api/ui_templates/background/thumbnail/{file_id}",
                "page": page,
                "width": width,
                "height": height,
                "description": description,
                "uploaded_at": datetime.now().isoformat()
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"上传失败: {str(e)}"
            }

    async def get_background_info(self, file_id: str) -> Dict[str, Any]:
        """获取背景信息"""
        file_path = self.storage_dir / file_id
        if not file_path.exists():
            return {
                "success": False,
                "error": "文件不存在"
            }

        try:
            file_stat = file_path.stat()
            info = {
                "success": True,
                "file_id": file_id,
                "filename": file_id,
                "size": file_stat.st_size,
                "url": f"/api/ui_templates/background/{file_id}",
                "created_at": datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
                "modified_at": datetime.fromtimestamp(file_stat.st_mtime).isoformat()
            }

            # 获取图片尺寸
            with Image.open(file_path) as img:
                info["width"] = img.width
                info["height"] = img.height
                info["aspect_ratio"] = round(img.width / img.height, 2)

            return info

        except Exception as e:
            return {
                "success": False,
                "error": f"获取信息失败: {str(e)}"
            }

    async def list_backgrounds(self, page: Optional[str] = None) -> Dict[str, Any]:
        """列出所有背景"""
        backgrounds = []
        for file_path in self.storage_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.allowed_formats:
                file_page = file_path.stem.split('_')[0]
                if page is None or file_page == page:
                    backgrounds.append(await self.get_background_info(file_path.name))

        return {
            "success": True,
            "total": len(backgrounds),
            "backgrounds": backgrounds
        }

    async def delete_background(self, file_id: str) -> Dict[str, Any]:
        """删除背景"""
        file_path = self.storage_dir / file_id
        if not file_path.exists():
            return {
                "success": False,
                "error": "文件不存在"
            }

        try:
            # 删除原图
            file_path.unlink()

            # 删除缩略图
            thumbnail_path = self.storage_dir / "thumbnails" / f"{file_id}.thumb{file_path.suffix}"
            if thumbnail_path.exists():
                thumbnail_path.unlink()

            return {
                "success": True,
                "message": f"背景 {file_id} 已删除"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"删除失败: {str(e)}"
            }

    async def set_background(
        self,
        page: str,
        file_id: Optional[str] = None,
        mode: str = "cover"
    ) -> Dict[str, Any]:
        """
        设置页面背景

        Args:
            page: 页面名称
            file_id: 背景文件ID（None表示清除）
            mode: 显示模式 (cover/contain/stretch/tile)
        """
        if mode not in self.display_modes:
            return {
                "success": False,
                "error": f"无效的显示模式: {mode}"
            }

        if file_id:
            file_path = self.storage_dir / file_id
            if not file_path.exists():
                return {
                    "success": False,
                    "error": "背景文件不存在"
                }

        # 保存背景配置
        config_file = self.storage_dir / "background_config.json"
        try:
            if config_file.exists():
                import json
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                config = {}

            config[page] = {
                "file_id": file_id,
                "mode": mode,
                "updated_at": datetime.now().isoformat()
            }

            with open(config_file, 'w', encoding='utf-8') as f:
                import json
                json.dump(config, f, indent=2, ensure_ascii=False)

            return {
                "success": True,
                "message": f"背景配置已更新",
                "page": page,
                "file_id": file_id,
                "mode": mode
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"设置失败: {str(e)}"
            }

    async def get_page_background(self, page: str) -> Dict[str, Any]:
        """获取页面背景配置"""
        config_file = self.storage_dir / "background_config.json"
        if not config_file.exists():
            return {
                "success": True,
                "page": page,
                "background": None
            }

        try:
            import json
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            if page in config:
                bg_config = config[page]
                file_id = bg_config.get("file_id")
                if file_id:
                    file_path = self.storage_dir / file_id
                    if file_path.exists():
                        bg_info = await self.get_background_info(file_id)
                        bg_info.update({
                            "mode": bg_config.get("mode"),
                            "updated_at": bg_config.get("updated_at")
                        })
                        return {
                            "success": True,
                            "page": page,
                            "background": bg_info
                        }

            return {
                "success": True,
                "page": page,
                "background": None
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"获取失败: {str(e)}"
            }


__all__ = ["BackgroundManager"]
