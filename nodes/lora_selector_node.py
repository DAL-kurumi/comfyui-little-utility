"""
Lora 選擇器節點 - 提供自動補全功能的 Lora 文件選擇器
支持在文本輸入框中自動匹配 ComfyUI lora 文件夾中的 Lora 名稱
支持管理 Lora 觸發詞並自動輸出
"""

import folder_paths
import os
import json


# 觸發詞配置文件路徑
TRIGGER_WORDS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "lora_trigger_words.json")


def load_trigger_words():
    """載入觸發詞配置"""
    if os.path.exists(TRIGGER_WORDS_FILE):
        try:
            with open(TRIGGER_WORDS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[LoraSelectorNode] 載入觸發詞配置失敗: {e}")
    return {}


def save_trigger_words(data):
    """保存觸發詞配置"""
    try:
        with open(TRIGGER_WORDS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"[LoraSelectorNode] 保存觸發詞配置失敗: {e}")
        return False


class LoraSelectorNode:
    """
    Lora 選擇器節點
    輸入：Lora 名稱文本輸入（帶自動補全功能，支持逗號分隔多個）
    輸出：選定的 Lora 名稱字符串和對應的觸發詞
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        """
        定義節點的輸入類型
        """
        return {
            "required": {
                "lora_name": ("STRING", {
                    "multiline": True,
                    "default": "",
                }),
            },
        }
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("lora_names", "trigger_words")
    FUNCTION = "select_lora"
    CATEGORY = "utils"
    
    @classmethod
    def get_lora_list(cls):
        """
        獲取所有可用的 Lora 文件列表
        
        返回:
            list: Lora 文件名列表（不含擴展名）
        """
        lora_list = []
        
        try:
            # 獲取 lora 文件夾路徑
            lora_paths = folder_paths.get_folder_paths("loras")
            
            for lora_path in lora_paths:
                if os.path.exists(lora_path):
                    # 遍歷文件夾獲取所有 lora 文件
                    for root, dirs, files in os.walk(lora_path):
                        for file in files:
                            if file.endswith(('.safetensors', '.ckpt', '.pt', '.bin')):
                                # 計算相對路徑
                                rel_path = os.path.relpath(os.path.join(root, file), lora_path)
                                # 移除擴展名
                                lora_name = os.path.splitext(rel_path)[0]
                                # 統一使用正斜線
                                lora_name = lora_name.replace('\\', '/')
                                lora_list.append(lora_name)
        except Exception as e:
            print(f"[LoraSelectorNode] 獲取 Lora 列表時出錯: {e}")
        
        # 去重並排序
        lora_list = sorted(list(set(lora_list)))
        return lora_list
    
    def select_lora(self, lora_name: str):
        """
        返回選定的 Lora 名稱和對應的觸發詞
        
        參數:
            lora_name: Lora 文件名（可用逗號分隔多個）
            
        返回:
            tuple: (lora_names, trigger_words)
        """
        # 解析逗號分隔的 Lora 名稱
        lora_names = [name.strip() for name in lora_name.split(",") if name.strip()]
        
        # 載入觸發詞配置
        trigger_words_config = load_trigger_words()
        
        # 收集所有觸發詞
        all_trigger_words = []
        for name in lora_names:
            if name in trigger_words_config:
                trigger = trigger_words_config[name].strip()
                if trigger:
                    all_trigger_words.append(trigger)
        
        # 合併觸發詞
        combined_trigger_words = ", ".join(all_trigger_words)
        
        return (lora_name, combined_trigger_words)


# ComfyUI 節點註冊
NODE_CLASS_MAPPINGS = {
    "LoraSelectorNode": LoraSelectorNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoraSelectorNode": "Lora 選擇器 (Lora Selector)"
}

