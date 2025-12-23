"""
類型切換節點 - 在文字、整數、小數之間進行轉換
支持三種輸入類型，自動選擇優先級最高的輸入並轉換為目標類型
"""


class TypeSwitchNode:
    """
    類型切換節點
    輸入：文字/整數/小數（可選，優先級：文字 > 整數 > 小數）
    輸出：根據選擇的類型輸出
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        """
        定義節點的輸入類型
        """
        return {
            "required": {
                "text_input": ("STRING", {"forceInput": True}),
            },
            "optional": {
                # int_input 和 float_input 由 JS 動態添加
                "output_type": (["STRING", "INT", "FLOAT"], {
                    "default": "STRING"
                }),
            },
        }
    
    RETURN_TYPES = ("STRING", "INT", "FLOAT")
    RETURN_NAMES = ("文字輸出", "整數輸出", "小數輸出")
    FUNCTION = "switch_type"
    CATEGORY = "utils"
    
    def switch_type(self, output_type="STRING", **kwargs):
        """
        根據優先級選擇輸入並轉換為目標類型
        """
        text_input = kwargs.get("text_input")
        int_input = kwargs.get("int_input")
        float_input = kwargs.get("float_input")
        print("=" * 50)
        print("類型切換節點執行中...")
        print(f"目標輸出類型: {output_type}")
        
        # 根據優先級選擇輸入值
        selected_value = None
        source_type = None
        
        # 優先級：文字 > 整數 > 小數
        if text_input is not None:
            selected_value = text_input
            source_type = "STRING"
            print(f"✓ 選擇文字輸入: {selected_value}")
        elif int_input is not None:
            selected_value = int_input
            source_type = "INT"
            print(f"✓ 選擇整數輸入: {selected_value}")
        elif float_input is not None:
            selected_value = float_input
            source_type = "FLOAT"
            print(f"✓ 選擇小數輸入: {selected_value}")
        else:
            print("⚠ 沒有任何輸入，使用默認值")
            # 沒有任何輸入，返回默認值
            return ("", 0, 0.0)
        
        print(f"來源類型: {source_type}")
        
        # 根據目標類型進行轉換
        try:
            if output_type == "STRING":
                result_str = self._to_string(selected_value, source_type)
                print(f"→ 轉換為文字: {result_str}")
                return (result_str, 0, 0.0)
            
            elif output_type == "INT":
                result_int = self._to_int(selected_value, source_type)
                print(f"→ 轉換為整數: {result_int}")
                return ("", result_int, 0.0)
            
            elif output_type == "FLOAT":
                result_float = self._to_float(selected_value, source_type)
                print(f"→ 轉換為小數: {result_float}")
                return ("", 0, result_float)
            
        except Exception as e:
            print(f"✗ 轉換失敗: {e}")
            # 轉換失敗時返回默認值
            return ("", 0, 0.0)
        
        finally:
            print("=" * 50)
        
        return ("", 0, 0.0)
    
    def _to_string(self, value, source_type):
        """轉換為字符串"""
        if source_type == "STRING":
            return value
        elif source_type == "INT":
            return str(value)
        elif source_type == "FLOAT":
            return str(value)
        return str(value)
    
    def _to_int(self, value, source_type):
        """轉換為整數"""
        if source_type == "INT":
            return value
        elif source_type == "FLOAT":
            return int(value)
        elif source_type == "STRING":
            # 嘗試將字符串轉換為整數
            try:
                # 如果字符串包含小數點，先轉為float再轉int
                if '.' in value:
                    return int(float(value))
                return int(value)
            except ValueError:
                print(f"⚠ 無法將 '{value}' 轉換為整數，返回 0")
                return 0
        return 0
    
    def _to_float(self, value, source_type):
        """轉換為浮點數"""
        if source_type == "FLOAT":
            return value
        elif source_type == "INT":
            return float(value)
        elif source_type == "STRING":
            # 嘗試將字符串轉換為浮點數
            try:
                return float(value)
            except ValueError:
                print(f"⚠ 無法將 '{value}' 轉換為小數，返回 0.0")
                return 0.0
        return 0.0


class TypeSwitchAutoNode:
    """
    自動類型切換節點
    根據輸入自動選擇最合適的輸出類型（無需手動選擇）
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        """
        定義節點的輸入類型
        """
        return {
            "required": {
                "text_input": ("STRING", {"forceInput": True}),
            },
            "optional": {
                # int_input 和 float_input 由 JS 動態添加
            },
        }
    
    RETURN_TYPES = ("STRING", "INT", "FLOAT")
    RETURN_NAMES = ("文字", "整數", "小數")
    FUNCTION = "auto_switch"
    CATEGORY = "utils"
    
    def auto_switch(self, **kwargs):
        """
        自動選擇輸入並輸出所有類型的轉換結果
        """
        text_input = kwargs.get("text_input")
        int_input = kwargs.get("int_input")
        float_input = kwargs.get("float_input")
        print("=" * 50)
        print("自動類型切換節點執行中...")
        
        # 根據優先級選擇輸入值
        selected_value = None
        source_type = None
        
        # 優先級：文字 > 整數 > 小數
        if text_input is not None:
            selected_value = text_input
            source_type = "STRING"
            print(f"✓ 選擇文字輸入: {selected_value}")
        elif int_input is not None:
            selected_value = int_input
            source_type = "INT"
            print(f"✓ 選擇整數輸入: {selected_value}")
        elif float_input is not None:
            selected_value = float_input
            source_type = "FLOAT"
            print(f"✓ 選擇小數輸入: {selected_value}")
        else:
            print("⚠ 沒有任何輸入，使用默認值")
            return ("", 0, 0.0)
        
        # 轉換為所有類型
        try:
            result_str = self._to_string(selected_value, source_type)
            result_int = self._to_int(selected_value, source_type)
            result_float = self._to_float(selected_value, source_type)
            
            print(f"→ 文字: {result_str}")
            print(f"→ 整數: {result_int}")
            print(f"→ 小數: {result_float}")
            print("=" * 50)
            
            return (result_str, result_int, result_float)
            
        except Exception as e:
            print(f"✗ 轉換失敗: {e}")
            print("=" * 50)
            return ("", 0, 0.0)
    
    def _to_string(self, value, source_type):
        """轉換為字符串"""
        return str(value)
    
    def _to_int(self, value, source_type):
        """轉換為整數"""
        if source_type == "INT":
            return value
        elif source_type == "FLOAT":
            return int(value)
        elif source_type == "STRING":
            try:
                if '.' in value:
                    return int(float(value))
                return int(value)
            except ValueError:
                return 0
        return 0
    
    def _to_float(self, value, source_type):
        """轉換為浮點數"""
        if source_type == "FLOAT":
            return value
        elif source_type == "INT":
            return float(value)
        elif source_type == "STRING":
            try:
                return float(value)
            except ValueError:
                return 0.0
        return 0.0


# ComfyUI節點註冊
NODE_CLASS_MAPPINGS = {
    "TypeSwitchNode": TypeSwitchNode,
    "TypeSwitchAutoNode": TypeSwitchAutoNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TypeSwitchNode": "類型切換 (Type Switch)",
    "TypeSwitchAutoNode": "類型切換自動 (Type Switch Auto)",
}
