import folder_paths
import comfy.sd
import comfy.utils

class LoraLoaderWithMetadata:
    """
    带有元数据的 LoRA 加载器
    除了加载 LoRA，还会将 LoRA 名称记录在模型对象中，方便后续读取。
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "lora_name": (folder_paths.get_filename_list("loras"), ),
                "strength_model": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
                "strength_clip": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
            }
        }
    
    RETURN_TYPES = ("MODEL", "CLIP", "STRING")
    RETURN_NAMES = ("MODEL", "CLIP", "lora_name")
    FUNCTION = "load_lora"
    CATEGORY = "little_utils"

    def load_lora(self, model, clip, lora_name, strength_model, strength_clip):
        if strength_model == 0 and strength_clip == 0:
            return (model, clip, lora_name)

        lora_path = folder_paths.get_full_path("loras", lora_name)
        lora = comfy.utils.load_torch_file(lora_path, safe_load=True)
        model_lora, clip_lora = comfy.sd.load_lora_for_models(model, clip, lora, strength_model, strength_clip)
        
        # 初始化或复制已有的 lora 列表
        current_loras = getattr(model, 'loaded_lora_names', [])
        # 为了不修改原对象（虽然 model_lora 是新对象），我们创建一个新的列表
        new_lora_list = list(current_loras)
        if lora_name not in new_lora_list:
            new_lora_list.append(lora_name)
        
        # 将列表存入新的模型对象中
        setattr(model_lora, 'loaded_lora_names', new_lora_list)
        
        return (model_lora, clip_lora, lora_name)

class GetModelLoraNames:
    """
    读取模型中已加载的 LoRA 名称
    支持读取通过 LoraLoaderWithMetadata 加载的名称，以及尝试读取一些常用第三方插件的 LoRA 堆栈信息。
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("names_string", "names_list_formatted")
    FUNCTION = "get_names"
    CATEGORY = "little_utils"

    def get_names(self, model):
        lora_list = []
        
        # 1. 尝试从我们自己的插件格式读取
        if hasattr(model, 'loaded_lora_names'):
            lora_list.extend(getattr(model, 'loaded_lora_names'))
            
        # 2. 尝试从常见的 LoRA Stack 格式读取 (例如 EasyUse, Efficiency Nodes 等)
        # 很多插件会将 LoRA 堆栈存储在 model.lora_stack 中
        if hasattr(model, 'lora_stack'):
            stack = getattr(model, 'lora_stack')
            for item in stack:
                if isinstance(item, (list, tuple)) and len(item) > 0:
                    name = item[0]
                    if isinstance(name, str) and name not in lora_list:
                        lora_list.append(name)
        
        # 去重并排序
        unique_loras = []
        for l in lora_list:
            if l not in unique_loras:
                unique_loras.append(l)
        
        names_str = ", ".join(unique_loras)
        names_list_fmt = "\n".join([f"- {name}" for name in unique_loras])
        
        return (names_str, names_list_fmt)

NODE_CLASS_MAPPINGS = {
    "LoraLoaderWithMetadata": LoraLoaderWithMetadata,
    "GetModelLoraNames": GetModelLoraNames
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoraLoaderWithMetadata": "带元数据的 LoRA 加载 (Lora Loader w/ Metadata)",
    "GetModelLoraNames": "读取模型 LoRA 名称 (Get Model LoRA Names)"
}
