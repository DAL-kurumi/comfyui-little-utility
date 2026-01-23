import torch

class EmptyLatentImageWithFlip:
    """
    空Latent圖像 (帶翻轉開關)
    建立一個指定尺寸的空Latent圖像，並提供一個開關可以快速交換寬高。
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": ("INT", {"default": 512, "min": 16, "max": 8192, "step": 8}),
                "height": ("INT", {"default": 512, "min": 16, "max": 8192, "step": 8}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 4096}),
                "flip": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "generate"
    CATEGORY = "utils"

    def generate(self, width, height, batch_size, flip):
        if flip:
            # 這裡進行寬高的交換
            active_width, active_height = height, width
        else:
            active_width, active_height = width, height
            
        # Standard ComfyUI latent creation: (batch, 4, height/8, width/8)
        latent = torch.zeros([batch_size, 4, active_height // 8, active_width // 8])
        return ({"samples": latent}, )
