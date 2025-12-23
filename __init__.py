"""
ComfyUI Little Utility - 简单实用的自定义节点集合
一个用于ComfyUI的自定义节点包，包含各种实用工具节点
"""

from .nodes.image_info_node import ImageInfoNode
from .nodes.image_download_node import ImageDownloadNode
from .nodes.text_combine_node import TextCombineNode
from .nodes.text_cleanup_node import TextCleanupNode, TextCleanupAdvancedNode
from .nodes.type_switch_node import TypeSwitchNode, TypeSwitchAutoNode

WEB_DIRECTORY = "web"
NODE_CLASS_MAPPINGS = {
    "ImageInfoNode": ImageInfoNode,
    "ImageDownloadNode": ImageDownloadNode,
    "TextCombineNode": TextCombineNode,
    "TextCleanupNode": TextCleanupNode,
    "TextCleanupAdvancedNode": TextCleanupAdvancedNode,
    "TypeSwitchNode": TypeSwitchNode,
    "TypeSwitchAutoNode": TypeSwitchAutoNode,
}

# 节点显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageInfoNode": "图片信息 (Image Info)",
    "ImageDownloadNode": "图片下载 (Image Download)",
    "TextCombineNode": "文字結合 (Text Combine)",
    "TextCleanupNode": "文字清理 (Text Cleanup)",
    "TextCleanupAdvancedNode": "文字清理進階 (Text Cleanup Advanced)",
    "TypeSwitchNode": "類型切換 (Type Switch)",
    "TypeSwitchAutoNode": "類型切換自動 (Type Switch Auto)",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

