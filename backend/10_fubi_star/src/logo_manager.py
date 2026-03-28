"""
辅弼星辰（扩展层）- LOGO管理器
版本: v2.0
负责人: 康辅星 (162)
功能: LOGO上传、管理、预览
"""

from typing import Dict, List, Optional, Any
import asyncio
from pathlib import Path
import shutil
from datetime import datetime
from PIL import Image
import io


class LogoManager:
    """LOGO管理器"""

    def __init__(self, storage_dir: str = "storage/logos", max_size_mb: int = 5):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.allowed_formats = {'.png', '.jpg', '.jpeg', '.svg', '.webp'}

    async def upload_logo(
        self,
        file_data: bytes,
        filename: str,
        theme: str = "light",
        resize: Optional[Dict[str, int]] = None
    ) -> Dict[str, Any]:
        """
        上传LOGO

        Args:
            file_data: 文件二进制数据
            filename: 文件名
            theme: 主题类型 (light/dark)
            resize: 调整尺寸 {"width": 200, "height": 80}
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
            # 处理图片
            if ext in {'.png', '.jpg', '.jpeg', '.webp'}:
                image = Image.open(io.BytesIO(file_data))

                # 调整尺寸
                if resize:
                    image = image.resize(
                        (resize['width'], resize['height']),
                        Image.Resampling.LANCZOS
                    )

                # 生成唯一文件名
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_id = f"{theme}_{timestamp}{ext}"
                file_path = self.storage_dir / file_id

                # 保存图片
                image.save(file_path, format=ext[1:].upper())

            # SVG文件直接保存
            elif ext == '.svg':
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_id = f"{theme}_{timestamp}{ext}"
                file_path = self.storage_dir / file_id
                with open(file_path, 'wb') as f:
                    f.write(file_data)

            return {
                "success": True,
                "file_id": file_id,
                "url": f"/api/ui_templates/logo/{file_id}",
                "theme": theme,
                "uploaded_at": datetime.now().isoformat()
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"上传失败: {str(e)}"
            }

    async def get_logo_info(self, file_id: str) -> Dict[str, Any]:
        """获取LOGO信息"""
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
                "url": f"/api/ui_templates/logo/{file_id}",
                "created_at": datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
                "modified_at": datetime.fromtimestamp(file_stat.st_mtime).isoformat()
            }

            # 如果是图片，获取尺寸
            if file_path.suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp'}:
                with Image.open(file_path) as img:
                    info["width"] = img.width
                    info["height"] = img.height

            return info

        except Exception as e:
            return {
                "success": False,
                "error": f"获取信息失败: {str(e)}"
            }

    async def list_logos(self, theme: Optional[str] = None) -> Dict[str, Any]:
        """列出所有LOGOLOGO"""
        logos = []
        for file_path in self.storage_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.allowed_formats:
                file_theme = file_path.stem.split('_')[0]
                if theme is None or file_theme == theme:
                    logos.append(await self.get_logo_info(file_path.name))

        return {
            "success": True,
            "total": len(logos),
            "logos": logos
        }

    async def delete_logo(self, file_id: str) -> Dict[str, Any]:
        """删除LOGO"""
        file_path = self.storage_dir / file_id
        if not file_path.exists():
            return {
                "success": False,
                "error": "文件不存在"
            }

        try:
            # 删除原文件
            file_path.unlink()
            return {
                "success": True,
                "message": f"LOGO {file_id} 已删除"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"删除失败: {str(e)}"
            }

    async def set_default_logo(self, theme: str, file_id: str) -> Dict[str, Any]:
        """设置默认LOGO"""
        file_path = self.storage_dir / file_id
        if not file_path.exists():
            return {
                "success": False,
                "error": "文件不存在"
            }

        try:
            # 复制为默认LOGO
            default_name = f"default_{theme}{file_path.suffix}"
            default_path = self.storage_dir / default_name
            shutil.copy2(file_path, default_path)

            return {
                "success": True,
                "message": f"默认LOGO已设置为 {file_id}",
                "default_file": default_name
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"设置失败: {str(e)}"
            }

    async def get_default_logo(self, theme: str) -> Optional[str]:
        """获取默认LOGO"""
        for ext in self.allowed_formats:
            default_name = f"default_{theme}{ext}"
            if (self.storage_dir / default_name).exists():
                return default_name
        return None


__all__ = ["LogoManager"]
