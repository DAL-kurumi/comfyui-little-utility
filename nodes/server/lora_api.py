"""
Lora API 路由 - 提供 Lora 列表和觸發詞管理的 REST API 端點
"""

from aiohttp import web
import folder_paths
import os
import json
import server


# 觸發詞配置文件路徑
TRIGGER_WORDS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "lora_trigger_words.json")


def get_lora_list():
    """
    獲取所有可用的 Lora 文件列表
    
    返回:
        list: Lora 文件信息列表
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
                            # 取得完整文件名（含擴展名）
                            full_name = rel_path.replace('\\', '/')
                            
                            lora_list.append({
                                "name": lora_name,
                                "filename": full_name,
                                "folder": os.path.dirname(lora_name) if '/' in lora_name else ""
                            })
    except Exception as e:
        print(f"[LoraAPI] 獲取 Lora 列表時出錯: {e}")
    
    # 根據名稱排序
    lora_list.sort(key=lambda x: x["name"].lower())
    return lora_list


def load_trigger_words():
    """載入觸發詞配置"""
    if os.path.exists(TRIGGER_WORDS_FILE):
        try:
            with open(TRIGGER_WORDS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[LoraAPI] 載入觸發詞配置失敗: {e}")
    return {}


def save_trigger_words(data):
    """保存觸發詞配置"""
    try:
        with open(TRIGGER_WORDS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"[LoraAPI] 保存觸發詞配置失敗: {e}")
        return False


@server.PromptServer.instance.routes.get("/little-utility/loras")
async def get_loras(request):
    """
    API 端點：獲取所有 Lora 文件列表
    
    返回:
        JSON: Lora 列表
    """
    loras = get_lora_list()
    return web.json_response({"loras": loras})


@server.PromptServer.instance.routes.get("/little-utility/loras/search")
async def search_loras(request):
    """
    API 端點：搜索 Lora 文件
    
    查詢參數:
        q: 搜索關鍵字
        
    返回:
        JSON: 匹配的 Lora 列表
    """
    query = request.query.get("q", "").lower().strip()
    loras = get_lora_list()
    
    if query:
        # 過濾匹配的 Lora
        filtered = [
            lora for lora in loras 
            if query in lora["name"].lower()
        ]
        return web.json_response({"loras": filtered, "query": query})
    
    return web.json_response({"loras": loras, "query": ""})


@server.PromptServer.instance.routes.get("/little-utility/trigger-words")
async def get_trigger_words(request):
    """
    API 端點：獲取所有觸發詞配置
    
    返回:
        JSON: 觸發詞配置
    """
    trigger_words = load_trigger_words()
    return web.json_response({"trigger_words": trigger_words})


@server.PromptServer.instance.routes.get("/little-utility/trigger-words/{lora_name:.*}")
async def get_trigger_word(request):
    """
    API 端點：獲取指定 Lora 的觸發詞
    
    返回:
        JSON: 觸發詞
    """
    lora_name = request.match_info.get("lora_name", "")
    trigger_words = load_trigger_words()
    trigger_word = trigger_words.get(lora_name, "")
    return web.json_response({
        "lora_name": lora_name,
        "trigger_word": trigger_word
    })


@server.PromptServer.instance.routes.post("/little-utility/trigger-words")
async def save_trigger_word(request):
    """
    API 端點：保存觸發詞
    
    請求體:
        lora_name: Lora 名稱
        trigger_word: 觸發詞
        
    返回:
        JSON: 保存結果
    """
    try:
        data = await request.json()
        lora_name = data.get("lora_name", "").strip()
        trigger_word = data.get("trigger_word", "").strip()
        
        if not lora_name:
            return web.json_response({"success": False, "error": "Lora 名稱不能為空"}, status=400)
        
        # 載入現有配置
        trigger_words = load_trigger_words()
        
        # 更新或刪除
        if trigger_word:
            trigger_words[lora_name] = trigger_word
        elif lora_name in trigger_words:
            del trigger_words[lora_name]
        
        # 保存
        if save_trigger_words(trigger_words):
            return web.json_response({
                "success": True,
                "lora_name": lora_name,
                "trigger_word": trigger_word
            })
        else:
            return web.json_response({"success": False, "error": "保存失敗"}, status=500)
            
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)


@server.PromptServer.instance.routes.delete("/little-utility/trigger-words/{lora_name:.*}")
async def delete_trigger_word(request):
    """
    API 端點：刪除觸發詞
    
    返回:
        JSON: 刪除結果
    """
    lora_name = request.match_info.get("lora_name", "")
    
    if not lora_name:
        return web.json_response({"success": False, "error": "Lora 名稱不能為空"}, status=400)
    
    # 載入現有配置
    trigger_words = load_trigger_words()
    
    # 刪除
    if lora_name in trigger_words:
        del trigger_words[lora_name]
        if save_trigger_words(trigger_words):
            return web.json_response({"success": True, "lora_name": lora_name})
        else:
            return web.json_response({"success": False, "error": "保存失敗"}, status=500)
    
    return web.json_response({"success": True, "lora_name": lora_name})
