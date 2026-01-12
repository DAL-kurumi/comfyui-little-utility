import os
import json
import folder_paths

class GlobalVarStorage:
    """Global storage for variable sharing between nodes"""
    _storage = {}
    _cache_dir = os.path.join(os.path.dirname(__file__), "cache")
    _cache_file = os.path.join(_cache_dir, "global_vars.json")

    @classmethod
    def _ensure_cache_dir(cls):
        if not os.path.exists(cls._cache_dir):
            os.makedirs(cls._cache_dir)

    @classmethod
    def _load_cache(cls):
        if os.path.exists(cls._cache_file):
            try:
                with open(cls._cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[GlobalVar] Error loading cache: {e}")
        return {}

    @classmethod
    def _save_cache(cls, data):
        cls._ensure_cache_dir()
        try:
            # Only save serializable data to disk
            serializable_data = {}
            # Load existing cache first to merge
            existing = cls._load_cache()
            serializable_data.update(existing)
            
            # Update with new data if serializable
            for k, v in data.items():
                try:
                    json.dumps(v)
                    serializable_data[k] = v
                except:
                    # If not serializable (like tensors/objects), skip saving to disk 
                    # but keep in memory. 
                    pass
            
            with open(cls._cache_file, 'w', encoding='utf-8') as f:
                json.dump(serializable_data, f, indent=4)
        except Exception as e:
            print(f"[GlobalVar] Error saving cache: {e}")

    @classmethod
    def set(cls, name, value, persist=False):
        cls._storage[name] = value
        if persist:
            cls._save_cache({name: value})

    @classmethod
    def get(cls, name):
        # Try memory first
        if name in cls._storage:
            return cls._storage[name]
        
        # Try loading from disk if not in memory (and if it was serializable)
        cache = cls._load_cache()
        if name in cache:
            # Restore to memory
            cls._storage[name] = cache[name]
            return cache[name]
            
        return None

class GlobalVarSetNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_data": ("*",),
                "var_name": ("STRING", {"default": "var_01", "multiline": False}),
                "is_cached": ("BOOLEAN", {"default": False, "label_on": "Cache (Disk)", "label_off": "Session Only"}),
            }
        }

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("output_data",)
    FUNCTION = "set_value"
    CATEGORY = "utils/global"
    
    def set_value(self, input_data, var_name, is_cached):
        GlobalVarStorage.set(var_name, input_data, persist=is_cached)
        # Pass through the data to allow chaining and ensure execution order
        return (input_data,)

class GlobalVarGetNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "var_name": ("STRING", {"default": "var_01", "multiline": False}),
            },
            "optional": {
                "trigger": ("*",),
            }
        }

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("value",)
    FUNCTION = "get_value"
    CATEGORY = "utils/global"

    def get_value(self, var_name, trigger=None):
        val = GlobalVarStorage.get(var_name)
        if val is None:
            # Validate or handle missing values (optional)
            print(f"Warning: Global variable '{var_name}' not found or is None.")
        return (val,)
