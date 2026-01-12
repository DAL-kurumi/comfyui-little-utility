"""
文字清理節點 - 清理文字中的錯誤逗號和多餘空格
處理常見的格式問題，如連續逗號、多餘空格等
"""

import re


class TextCleanupNode:
    """
    文字清理節點
    輸入：需要清理的文字
    輸出：清理後的文字
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        """
        定義節點的輸入類型
        """
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
            },
            "optional": {
                "remove_start_end_commas": ("BOOLEAN", {
                    "default": True,
                    "label_on": "移除",
                    "label_off": "保留"
                }),
                "normalize_spaces": ("BOOLEAN", {
                    "default": True,
                    "label_on": "標準化",
                    "label_off": "保留"
                }),
            },
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("清理後文字",)
    FUNCTION = "cleanup_text"
    CATEGORY = "utils"
    
    def cleanup_text(self, text, remove_start_end_commas=True, normalize_spaces=True):
        """
        清理文字中的錯誤逗號和格式問題
        
        參數:
            text: 需要清理的原始文字
            remove_start_end_commas: 是否移除開頭和結尾的逗號
            normalize_spaces: 是否標準化空格（多個空格轉為一個）
            
        返回:
            tuple: (清理後的文字,)
        """
        if not text:
            return ("",)
        
        original_text = text
        cleaned = text
        
        print("=" * 50)
        print("開始清理文字...")
        print(f"原始文字長度: {len(text)} 字符")
        
        # 1. 處理連續的逗號（包括中間有空格的情況）
        # ", ," -> ","
        # ",  ," -> ","
        # ",," -> ","
        # ",,," -> ","
        cleaned = re.sub(r',(\s*,)+', ',', cleaned)
        print("步驟 1: 移除連續逗號")
        
        # 2. 處理逗號前的多餘空格
        # "word , word" -> "word, word"
        cleaned = re.sub(r'\s+,', ',', cleaned)
        print("步驟 2: 移除逗號前的空格")
        
        # 3. 標準化逗號後的空格（確保逗號後只有一個空格，如果有的話）
        # "word,word" -> "word, word"
        # "word,  word" -> "word, word"
        cleaned = re.sub(r',\s*', ', ', cleaned)
        print("步驟 3: 標準化逗號後的空格")
        
        # 4. 如果啟用，標準化所有多餘的空格
        if normalize_spaces:
            # 將多個空格轉為一個空格
            cleaned = re.sub(r' +', ' ', cleaned)
            print("步驟 4: 標準化多餘空格")
        
        # 5. 如果啟用，移除開頭和結尾的逗號及空格
        if remove_start_end_commas:
            # 移除開頭的逗號和空格
            cleaned = re.sub(r'^[\s,]+', '', cleaned)
            # 移除結尾的逗號和空格
            cleaned = re.sub(r'[\s,]+$', '', cleaned)
            print("步驟 5: 移除開頭和結尾的逗號")
        
        # 6. 清理行首行尾的空格
        cleaned = cleaned.strip()
        
        # 統計結果
        changes_made = original_text != cleaned
        chars_removed = len(original_text) - len(cleaned)
        
        print(f"清理完成！")
        print(f"清理後文字長度: {len(cleaned)} 字符")
        print(f"移除了 {chars_removed} 個字符")
        print(f"是否有變更: {'是' if changes_made else '否'}")
        
        if changes_made:
            print("\n清理前後對比（前100字符）:")
            print(f"清理前: {original_text[:100]}")
            print(f"清理後: {cleaned[:100]}")
        
        print("=" * 50)
        
        return (cleaned,)


class TextCleanupAdvancedNode:
    """
    進階文字清理節點
    提供更多自定義選項的文字清理功能
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        """
        定義節點的輸入類型
        """
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
            },
            "optional": {
                "clean_commas": ("BOOLEAN", {
                    "default": True,
                    "label_on": "清理",
                    "label_off": "保留"
                }),
                "clean_spaces": ("BOOLEAN", {
                    "default": True,
                    "label_on": "清理",
                    "label_off": "保留"
                }),
                "remove_empty_lines": ("BOOLEAN", {
                    "default": False,
                    "label_on": "移除",
                    "label_off": "保留"
                }),
                "trim_lines": ("BOOLEAN", {
                    "default": True,
                    "label_on": "修剪",
                    "label_off": "保留"
                }),
            },
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("清理後文字",)
    FUNCTION = "cleanup_text_advanced"
    CATEGORY = "utils"
    
    def cleanup_text_advanced(self, text, clean_commas=True, clean_spaces=True, 
                            remove_empty_lines=False, trim_lines=True):
        """
        進階文字清理，提供更多自定義選項
        
        參數:
            text: 需要清理的原始文字
            clean_commas: 是否清理錯誤的逗號
            clean_spaces: 是否清理多餘空格
            remove_empty_lines: 是否移除空行
            trim_lines: 是否修剪每行的首尾空格
            
        返回:
            tuple: (清理後的文字,)
        """
        if not text:
            return ("",)
        
        lines = text.split('\n')
        cleaned_lines = []
        
        print("=" * 50)
        print("開始進階清理...")
        print(f"原始行數: {len(lines)}")
        
        for i, line in enumerate(lines):
            cleaned_line = line
            
            # 清理逗號
            if clean_commas:
                # 移除連續逗號
                cleaned_line = re.sub(r',(\s*,)+', ',', cleaned_line)
                # 移除逗號前的空格
                cleaned_line = re.sub(r'\s+,', ',', cleaned_line)
                # 標準化逗號後的空格
                cleaned_line = re.sub(r',\s*', ', ', cleaned_line)
                # 移除行首行尾的逗號
                cleaned_line = re.sub(r'^[\s,]+', '', cleaned_line)
                cleaned_line = re.sub(r'[\s,]+$', '', cleaned_line)
            
            # 清理空格
            if clean_spaces:
                # 將多個空格轉為一個
                cleaned_line = re.sub(r' +', ' ', cleaned_line)
            
            # 修剪每行
            if trim_lines:
                cleaned_line = cleaned_line.strip()
            
            # 如果不移除空行，或者該行非空，則加入結果
            if not remove_empty_lines or cleaned_line:
                cleaned_lines.append(cleaned_line)
        
        cleaned = '\n'.join(cleaned_lines)
        
        print(f"清理後行數: {len(cleaned_lines)}")
        print(f"移除了 {len(lines) - len(cleaned_lines)} 個空行")
        print(f"清理後總字符數: {len(cleaned)}")
        print("=" * 50)
        
        return (cleaned,)


# ComfyUI節點註冊
NODE_CLASS_MAPPINGS = {
    "TextCleanupNode": TextCleanupNode,
    "TextCleanupAdvancedNode": TextCleanupAdvancedNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextCleanupNode": "Text Cleanup",
    "TextCleanupAdvancedNode": "Text Cleanup Adv",
}
