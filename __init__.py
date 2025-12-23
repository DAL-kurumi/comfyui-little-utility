"""
ComfyUI Little Utility - 简单实用的自定义节点集合
一个用于ComfyUI的自定义节点包，包含各种实用工具节点
"""

from .nodes.image_info_node import ImageInfoNode
from .nodes.image_download_node import ImageDownloadNode

# 节点类映射
NODE_CLASS_MAPPINGS = {
    "ImageInfoNode": ImageInfoNode,
    "ImageDownloadNode": ImageDownloadNode,
}

# 节点显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageInfoNode": "图片信息 (Image Info)",
    "ImageDownloadNode": "图片下载 (Image Download)",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

