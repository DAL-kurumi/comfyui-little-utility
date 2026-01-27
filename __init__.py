"""
ComfyUI Little Utility - 简单实用的自定义节点集合
一个用于ComfyUI的自定义节点包，包含各种实用工具节点
"""

from .nodes.image_info_node import ImageInfoNode
from .nodes.image_download_node import ImageDownloadNode
from .nodes.text_combine_node import TextCombineNode
from .nodes.text_cleanup_node import TextCleanupNode, TextCleanupAdvancedNode
from .nodes.type_switch_node import TypeSwitchAutoNode
from .nodes.lora_selector_node import LoraSelectorNode
from .nodes.latent_utils import EmptyLatentImageWithFlip
from .nodes.cache_node import CacheNode
from .nodes.workflow_save_node import WorkflowSaveNode

# 導入 API 路由（這會自動註冊路由到服務器）
from .nodes.server import lora_api

WEB_DIRECTORY = "web"
NODE_CLASS_MAPPINGS = {
    "ImageInfoNode": ImageInfoNode,
    "ImageDownloadNode": ImageDownloadNode,
    "TextCombineNode": TextCombineNode,
    "TextCleanupNode": TextCleanupNode,
    "EmptyLatentImageWithFlip": EmptyLatentImageWithFlip,
    "TextCleanupAdvancedNode": TextCleanupAdvancedNode,
    "TypeSwitchAutoNode": TypeSwitchAutoNode,
    "LoraSelectorNode": LoraSelectorNode,
    "CacheNode": CacheNode,
    "WorkflowSaveNode": WorkflowSaveNode,
}

# 节点显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageInfoNode": "Image Info",
    "ImageDownloadNode": "Image Download",
    "TextCombineNode": "Text Combine",
    "TextCleanupNode": "Text Cleanup",
    "EmptyLatentImageWithFlip": "Empty Latent Flip",
    "TextCleanupAdvancedNode": "Text Cleanup Adv",
    "TypeSwitchAutoNode": "Type Switch",
    "LoraSelectorNode": "Lora Selector",
    "CacheNode": "Cache Node",
    "WorkflowSaveNode": "Workflow Save",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
