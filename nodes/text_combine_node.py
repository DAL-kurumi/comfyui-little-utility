"""
文字結合節點 - 允許多個文字輸入並合併
支持動態添加輸入（最多10個），並可自定義分隔符
"""

class TextCombineNode:
    """
    文字結合節點
    輸入：多個文字連接輸入（最多10個）+ 分隔符
    輸出：合併後的文字
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        """
        定義節點的輸入類型
        """
        return {
            "required": {
                "text_1": ("STRING", {"forceInput": True}),
            },
            "optional": {
                # 其他 text_n 由 JS 動態添加，這裡不再列出 2-10
                "separator": ("STRING", {
                    "multiline": False,
                    "default": "\n",
                }),
            },
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("合併文字",)
    FUNCTION = "combine_texts"
    CATEGORY = "utils"
    
    def combine_texts(self, separator="\n", **kwargs):
        """
        合併所有輸入的文字，使用指定的分隔符
        
        參數:
            separator: 分隔符字符串
            **kwargs: 所有動態輸入的文字 (text_1, text_2, ...)
            
        返回:
            tuple: (合併後的文字,)
        """
        # 收集所有輸入（從 text_1, text_2, ...）
        texts = []
        
        # 獲取所有以 text_ 開頭的參數並按數字序號排序
        text_keys = sorted([k for k in kwargs.keys() if k.startswith("text_")], 
                          key=lambda x: int(x.split("_")[1]) if "_" in x else 0)
        
        for key in text_keys:
            val = kwargs[key]
            if val and isinstance(val, str) and val.strip():
                texts.append(val)
        
        # 使用分隔符合併文字
        combined = separator.join(texts)
        return (combined,)


# ComfyUI節點註冊
NODE_CLASS_MAPPINGS = {
    "TextCombineNode": TextCombineNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextCombineNode": "文字結合 (Text Combine)"
}
