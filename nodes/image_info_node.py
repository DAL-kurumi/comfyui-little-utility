"""
图片信息节点 - 获取图片的长宽高信息
这是一个简单的ComfyUI自定义节点，用于显示输入图片的尺寸信息
"""

class ImageInfoNode:
    """
    图片信息节点
    输入：图片
    输出：图片（传递）、宽度、高度、批次大小
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        """
        定义节点的输入类型
        """
        return {
            "required": {
                "image": ("IMAGE",),  # 图片输入，ComfyUI中IMAGE类型是一个4维张量 [batch, height, width, channels]
            },
        }
    
    RETURN_TYPES = ("IMAGE", "INT", "INT", "INT")
    RETURN_NAMES = ("图片", "宽度", "高度", "批次数")
    FUNCTION = "get_image_info"
    CATEGORY = "utils"  # 节点在菜单中的分类
    
    def get_image_info(self, image):
        """
        获取图片信息的主函数
        
        参数:
            image: 输入的图片张量，格式为 [batch, height, width, channels]
        
        返回:
            tuple: (原图片, 宽度, 高度, 批次数)
        """
        # ComfyUI中的图片格式是 [batch, height, width, channels]
        batch_size = image.shape[0]
        height = image.shape[1]
        width = image.shape[2]
        # channels = image.shape[3]  # 通常是3（RGB）或4（RGBA）
        
        # 打印信息到控制台（用于调试）
        print(f"图片信息 - 批次: {batch_size}, 高度: {height}, 宽度: {width}")
        
        # 返回：原图片（传递给下一个节点）、宽度、高度、批次数
        return (image, width, height, batch_size)
