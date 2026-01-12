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
                    "default": ""
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
            # 设置更全的请求头，模仿现代浏览器
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Sec-Fetch-Dest': 'image',
                'Sec-Fetch-Mode': 'no-cors',
                'Sec-Fetch-Site': 'cross-site',
            }
            
            # 针对 Pixiv 的特殊处理：必须设置 Referer 否则会 403
            if 'pximg.net' in url:
                headers['Referer'] = 'https://www.pixiv.net/'
            
            # 针对 Twitter/X 的处理
            if 'twimg.com' in url:
                headers['Referer'] = 'https://x.com/'

            response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
            if response.status_code != 200:
                print(f"下载失败，状态码: {response.status_code}, URL: {url}")
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
    "ImageDownloadNode": "Image Download"
}
