class AnyType(str):
    """一個能與任何類型匹配的偽裝類型，解決 ComfyUI 的類型校驗問題"""
    def __ne__(self, __value: object) -> bool:
        return False
    def __eq__(self, __value: object) -> bool:
        return True

any_type = AnyType("*")

class CacheNode:
    """
    緩存節點
    輸入：任何類型 (可選)
    輸出：輸入的內容或緩存的內容
    """
    
    _cache = {}

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "cache_name": ("STRING", {"default": "default_cache"}),
            },
            "optional": {
                "any_input": (any_type,),
            }
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("output",)
    FUNCTION = "execute"
    CATEGORY = "utils"

    def execute(self, cache_name, any_input=None):
        if any_input is not None:
            # 更新緩存
            CacheNode._cache[cache_name] = any_input
            return (any_input,)
        
        # 如果輸入為空，嘗試讀取緩存
        if cache_name in CacheNode._cache:
            return (CacheNode._cache[cache_name],)
        
        # 如果連緩存都沒有，返回一個空字串避開某些節點的 None 報錯
        print(f"[CacheNode] 警告: 緩存 '{cache_name}' 為空且無輸入")
        return ("",)

    @classmethod
    def IS_CHANGED(cls, cache_name, any_input=None):
        # 始終返回 nan 確保節點每次都會執行，以便讀取最新緩存
        return float("nan")

NODE_CLASS_MAPPINGS = {
    "CacheNode": CacheNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CacheNode": "Cache Node",
}
