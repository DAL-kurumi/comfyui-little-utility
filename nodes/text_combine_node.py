"""
文字結合節點 - 允許多個文字輸入並合併
支持動態添加輸入（最多10個），並可自定義分隔符
"""

class TextCombineNode:
    """
    文字結合節點
    輸入：多個文字輸入（最多10個）+ 分隔符
    輸出：合併後的文字
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        """
        定義節點的輸入類型
        """
        return {
            "required": {
                "text_1": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "separator": ("STRING", {
                    "multiline": False,
                    "default": "\n",
                    "placeholder": "輸入分隔符（例如：\\n, , 等）"
                }),
            },
            "optional": {
                "text_2": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "text_3": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "text_4": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "text_5": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "text_6": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "text_7": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "text_8": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "text_9": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "text_10": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
            },
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("合併文字",)
    FUNCTION = "combine_texts"
    CATEGORY = "utils"
    
    def combine_texts(self, separator="\n", text_1="", text_2="", text_3="", text_4="", 
                     text_5="", text_6="", text_7="", text_8="", text_9="", text_10="", **kwargs):
        """
        合併所有輸入的文字，使用指定的分隔符
        
        參數:
            separator: 分隔符字符串
            text_1 到 text_10: 最多10個文字輸入
            
        返回:
            tuple: (合併後的文字,)
        """
        # 收集所有非空的文字輸入
        texts = []
        
        # 檢查所有10個可能的輸入
        for i, text in enumerate([text_1, text_2, text_3, text_4, text_5, 
                                   text_6, text_7, text_8, text_9, text_10], 1):
            # 只添加非空的文字
            if text and text.strip():
                texts.append(text)
                print(f"文字輸入 {i}: {text[:50]}...")  # 打印前50個字符用於調試
        
        # 使用分隔符合併所有文字
        combined = separator.join(texts)
        
        print(f"總共合併了 {len(texts)} 個文字輸入")
        print(f"使用分隔符: {repr(separator)}")
        print(f"合併結果長度: {len(combined)} 字符")
        
        return (combined,)


# ComfyUI節點註冊
NODE_CLASS_MAPPINGS = {
    "TextCombineNode": TextCombineNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextCombineNode": "文字結合 (Text Combine)"
}
