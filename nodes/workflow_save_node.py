import os
import json
from datetime import datetime
import folder_paths


class AnyType(str):
    """一個能與任何類型匹配的偽裝類型，解決 ComfyUI 的類型校驗問題"""
    def __ne__(self, __value: object) -> bool:
        return False
    def __eq__(self, __value: object) -> bool:
        return True


any_type = AnyType("*")


class WorkflowSaveNode:
    """
    工作流保存節點
    接受任何輸入並原樣輸出，同時將當前工作流保存到指定目錄
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "filename_prefix": ("STRING", {"default": "workflow"}),
            },
            "optional": {
                "any_input": (any_type,),
            },
            "hidden": {
                "extra_pnginfo": "EXTRA_PNGINFO",
                "prompt": "PROMPT",
            }
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("output",)
    FUNCTION = "execute"
    CATEGORY = "utils"
    OUTPUT_NODE = True

    def execute(self, filename_prefix, any_input=None, extra_pnginfo=None, prompt=None):
        # 獲取 ComfyUI 用戶目錄下的 workflows 目錄
        # folder_paths.get_user_directory() 返回 ComfyUI/user/default
        user_dir = folder_paths.get_user_directory()
        workflows_dir = os.path.join(user_dir, "workflows")
        
        # 確保目錄存在
        os.makedirs(workflows_dir, exist_ok=True)
        
        # 生成帶時間戳的檔案名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.json"
        filepath = os.path.join(workflows_dir, filename)
        
        # 準備要保存的工作流數據
        workflow_data = {}
        
        if extra_pnginfo is not None and "workflow" in extra_pnginfo:
            # extra_pnginfo 包含完整的工作流數據
            workflow_data = extra_pnginfo["workflow"]
        elif prompt is not None:
            # 如果沒有 workflow，至少保存 prompt 數據
            workflow_data = {"prompt": prompt}
        
        if workflow_data:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(workflow_data, f, indent=2, ensure_ascii=False)
            except Exception as e:
                print(f"[WorkflowSaveNode] 保存工作流時發生錯誤: {e}")
        
        # 原樣輸出輸入
        if any_input is not None:
            return (any_input,)
        return ("",)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        # 始終執行以確保每次運行都保存工作流
        return float("nan")


NODE_CLASS_MAPPINGS = {
    "WorkflowSaveNode": WorkflowSaveNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WorkflowSaveNode": "Workflow Save",
}
