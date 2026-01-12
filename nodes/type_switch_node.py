"""
類型切換節點 - 將輸入轉換為文字、整數、小數三種格式
支持通配符輸入，自動輸出所有格式的轉換結果
"""

class TypeSwitchAutoNode:
    """
    類型切換自動節點
    將輸入的數據同時轉換為文字、整數、小數輸出
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": ("*", {"forceInput": True}),
            },
        }
    
    RETURN_TYPES = ("STRING", "INT", "FLOAT")
    RETURN_NAMES = ("文字", "整數", "小數")
    FUNCTION = "auto_switch"
    CATEGORY = "utils"
    
    def auto_switch(self, input=None):
        if input is None:
            return ("", 0, 0.0)
            
        val_str = str(input)
        try:
            # 優先嘗試轉換為 float 以處理包含小數點Type Switch Auto的字串
            val_float = float(val_str)
            val_int = int(val_float)
        except:
            val_float = 0.0
            val_int = 0
            
        return (val_str, val_int, val_float)


# ComfyUI節點註冊
NODE_CLASS_MAPPINGS = {
    "TypeSwitchAutoNode": TypeSwitchAutoNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TypeSwitchAutoNode": "Type Switch",
}
