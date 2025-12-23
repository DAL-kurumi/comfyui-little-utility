import torch
import numpy as np
import requests
from PIL import Image, ImageOps
from io import BytesIO

class ImageDownloadNode:
    """
    图片下载节点
    输入：URL (STRING)
    输出：IMAGE
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        """
        定义节点的输入类型
        """
        return {
            "required": {
                "url": ("STRING", {
                    "multiline": False,
                    "default": "URL"
                }),
            },
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "download_image"
    CATEGORY = "utils"
    
    def download_image(self, url):
        """
        从指定URL下载图片并转换为ComfyUI格式
        """
        if not url or not url.startswith('http'):
            print(f"无效的URL: {url}")
            return (torch.zeros((1, 64, 64, 3), dtype=torch.float32),)

        try:
            # 设置请求头，模仿浏览器
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # 针对 Pixiv 的特殊处理：必须设置 Referer 否则会 403
            if 'pximg.net' in url:
                headers['Referer'] = 'https://www.pixiv.net/'
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            img = Image.open(BytesIO(response.content))
            
            # 转为RGB，防止RGBA或其他格式导致问题
            img = ImageOps.exif_transpose(img)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 转换为numpy数组并归一化到 [0, 1]
            image_np = np.array(img).astype(np.float32) / 255.0
            
            # 增加batch维度 [B, H, W, C]
            image_tensor = torch.from_numpy(image_np)[None,]
            
            return (image_tensor,)
            
        except Exception as e:
            print(f"下载图片失败: {e}")
            # 返回一个黑色的默认图，以免节点崩溃
            return (torch.zeros((1, 64, 64, 3), dtype=torch.float32),)

# 某些ComfyUI版本可能需要这个
NODE_CLASS_MAPPINGS = {
    "ImageDownloadNode": ImageDownloadNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageDownloadNode": "图片下载 (Image Download)"
}
