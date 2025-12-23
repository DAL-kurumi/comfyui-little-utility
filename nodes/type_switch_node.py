"""
類型切換節點 - 在任一輸入、整數、小數之間進行轉換
支持通配符輸入，自動選擇優先級最高的有效輸入並轉換為目標類型
"""

class TypeSwitchNode:
    """
    類型切換節點
    輸入：任何類型（通配符 *），優先級：Input 1 > Input 2 > Input 3
    輸出：根據選擇的類型輸出
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_1": ("*", {"forceInput": True}),
            },
            "optional": {
                "output_type": (["STRING", "INT", "FLOAT"], {"default": "STRING"}),
            },
        }
    
    RETURN_TYPES = ("STRING", "INT", "FLOAT")
    RETURN_NAMES = ("文字輸出", "整數輸出", "小數輸出")
    FUNCTION = "switch_type"
    CATEGORY = "utils"
    
    def switch_type(self, output_type="STRING", **kwargs):
        # 獲取所有輸入並排序
        input_keys = sorted([k for k in kwargs.keys() if k.startswith("input_")], 
                           key=lambda x: int(x.split("_")[1]) if "_" in x else 0)
        
        selected_value = None
        for key in input_keys:
            val = kwargs[key]
            if val is not None:
                selected_value = val
                break
        
        if selected_value is None:
            return ("", 0, 0.0)
            
        # 轉換邏輯
        try:
            if output_type == "STRING":
                return (str(selected_value), 0, 0.0)
            elif output_type == "INT":
                try:
                    val = int(float(str(selected_value)))
                except:
                    val = 0
                return ("", val, 0.0)
            elif output_type == "FLOAT":
                try:
                    val = float(str(selected_value))
                except:
                    val = 0.0
                return ("", 0, val)
        except:
            return ("", 0, 0.0)
        
        return ("", 0, 0.0)


class TypeSwitchAutoNode:
    """
    自動類型切換節點
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_1": ("*", {"forceInput": True}),
            },
            "optional": {},
        }
    
    RETURN_TYPES = ("STRING", "INT", "FLOAT")
    RETURN_NAMES = ("文字", "整數", "小數")
    FUNCTION = "auto_switch"
    CATEGORY = "utils"
    
    def auto_switch(self, **kwargs):
        input_keys = sorted([k for k in kwargs.keys() if k.startswith("input_")], 
                           key=lambda x: int(x.split("_")[1]) if "_" in x else 0)
        
        selected_value = None
        for key in input_keys:
            val = kwargs[key]
            if val is not None:
                selected_value = val
                break
        
        if selected_value is None:
            return ("", 0, 0.0)
            
        val_str = str(selected_value)
        try:
            val_float = float(val_str)
            val_int = int(val_float)
        except:
            val_float = 0.0
            val_int = 0
            
        return (val_str, val_int, val_float)


# ComfyUI節點註冊
NODE_CLASS_MAPPINGS = {
    "TypeSwitchNode": TypeSwitchNode,
    "TypeSwitchAutoNode": TypeSwitchAutoNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TypeSwitchNode": "類型切換 (Type Switch)",
    "TypeSwitchAutoNode": "類型切換自動 (Type Switch Auto)",
}
