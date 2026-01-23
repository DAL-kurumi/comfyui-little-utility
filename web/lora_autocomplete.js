import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

console.log("[Little Utility] Lora 自動補全擴展已加載");

// 緩存 Lora 列表
let loraCache = null;
let loraCacheTime = 0;
const CACHE_DURATION = 5000; // 縮短緩存至 5 秒，確保及時更新

// 觸發詞緩存
let triggerWordsCache = null;

/**
 * 獲取 Lora 列表（帶緩存）
 */
async function fetchLoraList() {
  const now = Date.now();
  if (loraCache && now - loraCacheTime < CACHE_DURATION) {
    return loraCache;
  }

  try {
    const response = await api.fetchApi("/little-utility/loras");
    const data = await response.json();
    loraCache = data.loras || [];
    loraCacheTime = now;
    console.log(`[Little Utility] 已加載 ${loraCache.length} 個 Lora`);
    return loraCache;
  } catch (error) {
    console.error("[Little Utility] 獲取 Lora 列表失敗:", error);
    return [];
  }
}

/**
 * 獲取觸發詞配置
 */
async function fetchTriggerWords() {
  try {
    const response = await api.fetchApi("/little-utility/trigger-words");
    const data = await response.json();
    triggerWordsCache = data.trigger_words || {};
    return triggerWordsCache;
  } catch (error) {
    console.error("[Little Utility] 獲取觸發詞失敗:", error);
    return {};
  }
}

/**
 * 保存觸發詞
 */
async function saveTriggerWord(loraName, triggerWord) {
  try {
    const response = await api.fetchApi("/little-utility/trigger-words", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        lora_name: loraName,
        trigger_word: triggerWord,
      }),
    });
    const data = await response.json();
    if (data.success) {
      // 更新緩存
      if (!triggerWordsCache) triggerWordsCache = {};
      if (triggerWord) {
        triggerWordsCache[loraName] = triggerWord;
      } else {
        delete triggerWordsCache[loraName];
      }
    }
    return data;
  } catch (error) {
    console.error("[Little Utility] 保存觸發詞失敗:", error);
    return { success: false, error: error.message };
  }
}

// ==================== 樣式注入 ====================

function injectStyles() {
  if (document.getElementById("lora-autocomplete-styles")) return;

  const style = document.createElement("style");
  style.id = "lora-autocomplete-styles";
  style.textContent = `
        /* 自動補全下拉框 */
        .lora-autocomplete-dropdown {
            position: fixed;
            z-index: 99999;
            background: #252525;
            border: 1px solid #3a3a3a;
            border-radius: 4px;
            max-height: 280px;
            overflow-y: auto;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
            min-width: 200px;
        }
        .lora-autocomplete-dropdown::-webkit-scrollbar {
            width: 6px;
        }
        .lora-autocomplete-dropdown::-webkit-scrollbar-track {
            background: #1a1a1a;
        }
        .lora-autocomplete-dropdown::-webkit-scrollbar-thumb {
            background: #444;
            border-radius: 3px;
        }
        .lora-autocomplete-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 6px 10px;
            cursor: pointer;
            font-size: 13px;
            color: #ccc;
            border-left: 2px solid transparent;
        }
        .lora-autocomplete-item:hover,
        .lora-autocomplete-item.selected {
            background: #333;
            border-left-color: #4a9eff;
        }
        .lora-autocomplete-item .name {
            flex: 1;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        .lora-autocomplete-item .name .match {
            color: #ffcc00;
            font-weight: bold;
        }
        .lora-autocomplete-item .has-trigger {
            color: #4ade80;
            font-size: 10px;
            margin-left: 6px;
        }
        .lora-autocomplete-empty {
            padding: 12px;
            color: #666;
            text-align: center;
            font-size: 12px;
        }
        
        /* 管理按鈕 */
        .lora-manage-btn {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            width: 100%;
            padding: 8px 12px;
            margin-top: 4px;
            background: #2a2a2a;
            border: 1px solid #444;
            border-radius: 4px;
            color: #a78bfa;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .lora-manage-btn:hover {
            background: #333;
            border-color: #a78bfa;
        }
        .lora-manage-btn .icon {
            font-size: 14px;
        }
        
        /* 彈出對話框 */
        .lora-dialog-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.7);
            z-index: 100000;
            display: flex;
            align-items: center;
            justify-content: center;
            backdrop-filter: blur(4px);
        }
        .lora-dialog {
            background: #1e1e1e;
            border: 1px solid #444;
            border-radius: 8px;
            width: 500px;
            max-width: 90vw;
            max-height: 80vh;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        }
        .lora-dialog-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px 20px;
            background: #252525;
            border-bottom: 1px solid #333;
        }
        .lora-dialog-title {
            font-size: 16px;
            font-weight: 600;
            color: #fff;
        }
        .lora-dialog-close {
            width: 28px;
            height: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: transparent;
            border: none;
            color: #888;
            font-size: 18px;
            cursor: pointer;
            border-radius: 4px;
            transition: all 0.2s;
        }
        .lora-dialog-close:hover {
            background: #333;
            color: #fff;
        }
        .lora-dialog-body {
            padding: 20px;
            overflow-y: auto;
            max-height: calc(80vh - 140px);
        }
        .lora-dialog-footer {
            display: flex;
            justify-content: flex-end;
            gap: 10px;
            padding: 16px 20px;
            background: #252525;
            border-top: 1px solid #333;
        }
        
        /* 表單元素 */
        .lora-form-group {
            margin-bottom: 16px;
        }
        .lora-form-label {
            display: block;
            margin-bottom: 8px;
            font-size: 13px;
            color: #aaa;
        }
        .lora-form-input {
            width: 100%;
            padding: 10px 12px;
            background: #2a2a2a;
            border: 1px solid #444;
            border-radius: 4px;
            color: #fff;
            font-size: 14px;
            outline: none;
            transition: border-color 0.2s;
        }
        .lora-form-input:focus {
            border-color: #a78bfa;
        }
        .lora-form-input::placeholder {
            color: #666;
        }
        .lora-form-textarea {
            width: 100%;
            min-height: 120px;
            padding: 10px 12px;
            background: #2a2a2a;
            border: 1px solid #444;
            border-radius: 4px;
            color: #fff;
            font-size: 14px;
            resize: vertical;
            outline: none;
            font-family: inherit;
            transition: border-color 0.2s;
        }
        .lora-form-textarea:focus {
            border-color: #a78bfa;
        }
        .lora-form-textarea::placeholder {
            color: #666;
        }
        
        /* 按鈕 */
        .lora-btn {
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .lora-btn-primary {
            background: #a78bfa;
            color: #fff;
        }
        .lora-btn-primary:hover {
            background: #8b5cf6;
        }
        .lora-btn-secondary {
            background: #333;
            color: #ccc;
        }
        .lora-btn-secondary:hover {
            background: #444;
        }
        
        /* 提示訊息 */
        .lora-toast {
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 12px 20px;
            background: #333;
            border: 1px solid #444;
            border-radius: 6px;
            color: #fff;
            font-size: 13px;
            z-index: 100001;
            animation: lora-toast-in 0.3s ease;
        }
        .lora-toast.success {
            border-color: #4ade80;
        }
        .lora-toast.error {
            border-color: #f87171;
        }
        @keyframes lora-toast-in {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    `;
  document.head.appendChild(style);
}

// ==================== 自動補全下拉框 ====================

let activeDropdown = null;
let activeInput = null;

function highlightMatch(text, query) {
  if (!query) return text;

  const lowerText = text.toLowerCase();
  const lowerQuery = query.toLowerCase();
  let result = "";
  let lastIndex = 0;
  let searchIndex = 0;

  while ((searchIndex = lowerText.indexOf(lowerQuery, lastIndex)) !== -1) {
    result += text.substring(lastIndex, searchIndex);
    result += `<span class="match">${text.substring(searchIndex, searchIndex + query.length)}</span>`;
    lastIndex = searchIndex + query.length;
  }
  result += text.substring(lastIndex);

  return result;
}

function getDropdown() {
  if (activeDropdown) return activeDropdown;

  injectStyles();

  const dropdown = document.createElement("div");
  dropdown.className = "lora-autocomplete-dropdown";
  dropdown.style.display = "none";
  document.body.appendChild(dropdown);

  activeDropdown = dropdown;
  return dropdown;
}

function hideDropdown() {
  if (activeDropdown) {
    activeDropdown.style.display = "none";
  }
  activeInput = null;
}

function showDropdown(inputElement, loras, query, onSelect, triggerWords) {
  const dropdown = getDropdown();
  dropdown.innerHTML = "";
  activeInput = inputElement;

  // 獲取最後一個逗號後的內容進行匹配
  const parts = query.split(",");
  const lastPart = parts[parts.length - 1].trim().toLowerCase();

  // 過濾匹配項
  let filtered = loras;
  if (lastPart) {
    filtered = loras.filter((lora) =>
      lora.name.toLowerCase().includes(lastPart),
    );
  }

  if (filtered.length === 0) {
    const empty = document.createElement("div");
    empty.className = "lora-autocomplete-empty";
    empty.textContent = lastPart ? "沒有匹配的 Lora" : "開始輸入以搜索...";
    dropdown.appendChild(empty);
  } else {
    const displayItems = filtered.slice(0, 30);

    displayItems.forEach((lora, index) => {
      const item = document.createElement("div");
      item.className = "lora-autocomplete-item";
      if (index === 0) item.classList.add("selected");

      const nameSpan = document.createElement("span");
      nameSpan.className = "name";
      nameSpan.innerHTML = highlightMatch(lora.name, lastPart);
      item.appendChild(nameSpan);

      // 顯示是否有觸發詞
      // 優先使用傳入的 triggerWords，如果沒有則使用全局緩存
      const tw = triggerWords || triggerWordsCache;
      if (tw && tw[lora.name]) {
        const hasTrigger = document.createElement("span");
        hasTrigger.className = "has-trigger";
        hasTrigger.textContent = "✓ 觸發詞";
        item.appendChild(hasTrigger);
      }

      item.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();

        // 替換最後一個部分
        parts[parts.length - 1] = lora.name;
        const newValue = parts.join(", ");
        onSelect(newValue);
        hideDropdown();
      });

      item.addEventListener("mouseenter", () => {
        dropdown.querySelectorAll(".lora-autocomplete-item").forEach((el) => {
          el.classList.remove("selected");
        });
        item.classList.add("selected");
      });

      dropdown.appendChild(item);
    });
  }

  // 定位下拉框
  const rect = inputElement.getBoundingClientRect();
  dropdown.style.left = `${rect.left}px`;
  dropdown.style.top = `${rect.bottom + 2}px`;
  dropdown.style.width = `${Math.max(rect.width, 280)}px`;
  dropdown.style.display = "block";
}

function handleKeydown(e, onSelect) {
  const dropdown = activeDropdown;
  if (!dropdown || dropdown.style.display === "none") return false;

  const items = dropdown.querySelectorAll(".lora-autocomplete-item");
  if (items.length === 0) return false;

  let selectedIndex = Array.from(items).findIndex((item) =>
    item.classList.contains("selected"),
  );

  switch (e.key) {
    case "ArrowDown":
      e.preventDefault();
      if (selectedIndex < items.length - 1) {
        items[selectedIndex]?.classList.remove("selected");
        items[selectedIndex + 1]?.classList.add("selected");
        items[selectedIndex + 1]?.scrollIntoView({ block: "nearest" });
      }
      return true;

    case "ArrowUp":
      e.preventDefault();
      if (selectedIndex > 0) {
        items[selectedIndex]?.classList.remove("selected");
        items[selectedIndex - 1]?.classList.add("selected");
        items[selectedIndex - 1]?.scrollIntoView({ block: "nearest" });
      }
      return true;

    case "Tab":
      if (selectedIndex >= 0) {
        e.preventDefault();
        items[selectedIndex]?.click();
      }
      return true;

    case "Escape":
      hideDropdown();
      return true;
  }

  return false;
}

// ==================== 觸發詞管理對話框 ====================

function showToast(message, type = "success") {
  const toast = document.createElement("div");
  toast.className = `lora-toast ${type}`;
  toast.textContent = message;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, 3000);
}

function createManageDialog(onClose) {
  injectStyles();

  const overlay = document.createElement("div");
  overlay.className = "lora-dialog-overlay";

  const dialog = document.createElement("div");
  dialog.className = "lora-dialog";

  dialog.innerHTML = `
        <div class="lora-dialog-header">
            <span class="lora-dialog-title">管理 Lora 觸發詞</span>
            <button class="lora-dialog-close">×</button>
        </div>
        <div class="lora-dialog-body">
            <div class="lora-form-group">
                <label class="lora-form-label">Lora 名稱</label>
                <input type="text" class="lora-form-input" id="lora-dialog-name" placeholder="輸入或選擇 Lora 名稱...">
                <div class="lora-autocomplete-dropdown" id="lora-dialog-dropdown" style="display:none; position:absolute;"></div>
            </div>
            <div class="lora-form-group">
                <label class="lora-form-label">觸發詞</label>
                <textarea class="lora-form-textarea" id="lora-dialog-trigger" placeholder="輸入此 Lora 的觸發詞..."></textarea>
            </div>
        </div>
        <div class="lora-dialog-footer">
            <button class="lora-btn lora-btn-secondary" id="lora-dialog-cancel">取消</button>
            <button class="lora-btn lora-btn-primary" id="lora-dialog-save">保存</button>
        </div>
    `;

  overlay.appendChild(dialog);
  document.body.appendChild(overlay);

  // 元素引用
  const nameInput = dialog.querySelector("#lora-dialog-name");
  const triggerInput = dialog.querySelector("#lora-dialog-trigger");
  const dropdown = dialog.querySelector("#lora-dialog-dropdown");
  const closeBtn = dialog.querySelector(".lora-dialog-close");
  const cancelBtn = dialog.querySelector("#lora-dialog-cancel");
  const saveBtn = dialog.querySelector("#lora-dialog-save");

  // 關閉對話框
  const close = () => {
    overlay.remove();
    if (onClose) onClose();
  };

  closeBtn.addEventListener("click", close);
  cancelBtn.addEventListener("click", close);
  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) close();
  });

  // Lora 名稱自動補全
  let loras = [];

  async function initData() {
    loras = await fetchLoraList();
    // 確保觸發詞是最新的
    if (!triggerWordsCache) {
      await fetchTriggerWords();
    }
  }

  initData();

  function showDialogDropdown(query) {
    dropdown.innerHTML = "";

    const lowerQuery = query.toLowerCase();
    const filtered = loras
      .filter((lora) => lora.name.toLowerCase().includes(lowerQuery))
      .slice(0, 20);

    if (filtered.length === 0) {
      dropdown.style.display = "none";
      return;
    }

    filtered.forEach((lora, index) => {
      const item = document.createElement("div");
      item.className = "lora-autocomplete-item";
      if (index === 0) item.classList.add("selected");

      const nameSpan = document.createElement("span");
      nameSpan.className = "name";
      nameSpan.innerHTML = highlightMatch(lora.name, query);
      item.appendChild(nameSpan);

      // 直接使用全局緩存
      if (triggerWordsCache && triggerWordsCache[lora.name]) {
        const hasTrigger = document.createElement("span");
        hasTrigger.className = "has-trigger";
        hasTrigger.textContent = "✓";
        item.appendChild(hasTrigger);
      }

      item.addEventListener("click", () => {
        nameInput.value = lora.name;
        triggerInput.value =
          (triggerWordsCache && triggerWordsCache[lora.name]) || "";
        dropdown.style.display = "none";
      });

      item.addEventListener("mouseenter", () => {
        dropdown
          .querySelectorAll(".lora-autocomplete-item")
          .forEach((el) => el.classList.remove("selected"));
        item.classList.add("selected");
      });

      dropdown.appendChild(item);
    });

    const rect = nameInput.getBoundingClientRect();
    dropdown.style.position = "fixed";
    dropdown.style.left = `${rect.left}px`;
    dropdown.style.top = `${rect.bottom + 2}px`;
    dropdown.style.width = `${rect.width}px`;
    dropdown.style.display = "block";
  }

  nameInput.addEventListener("input", () => {
    showDialogDropdown(nameInput.value);
  });

  nameInput.addEventListener("focus", () => {
    if (nameInput.value) {
      showDialogDropdown(nameInput.value);
    }
  });

  nameInput.addEventListener("keydown", (e) => {
    if (dropdown.style.display === "none") return;

    const items = dropdown.querySelectorAll(".lora-autocomplete-item");
    let selectedIndex = Array.from(items).findIndex((item) =>
      item.classList.contains("selected"),
    );

    if (e.key === "ArrowDown") {
      e.preventDefault();
      if (selectedIndex < items.length - 1) {
        items[selectedIndex]?.classList.remove("selected");
        items[selectedIndex + 1]?.classList.add("selected");
      }
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      if (selectedIndex > 0) {
        items[selectedIndex]?.classList.remove("selected");
        items[selectedIndex - 1]?.classList.add("selected");
      }
    } else if (e.key === "Enter" || e.key === "Tab") {
      e.preventDefault();
      items[selectedIndex]?.click();
    } else if (e.key === "Escape") {
      dropdown.style.display = "none";
    }
  });

  // 點擊外部關閉下拉框
  dialog.addEventListener("click", (e) => {
    if (!nameInput.contains(e.target) && !dropdown.contains(e.target)) {
      dropdown.style.display = "none";
    }
  });

  // 保存
  saveBtn.addEventListener("click", async () => {
    const loraName = nameInput.value.trim();
    const triggerWord = triggerInput.value.trim();

    if (!loraName) {
      showToast("請輸入 Lora 名稱", "error");
      return;
    }

    const result = await saveTriggerWord(loraName, triggerWord);

    if (result.success) {
      showToast(triggerWord ? "觸發詞已保存" : "觸發詞已刪除", "success");
      // 這裡不需要手動更新緩存，saveTriggerWord 已經做了
      nameInput.value = "";
      triggerInput.value = "";
    } else {
      showToast(result.error || "保存失敗", "error");
    }
  });

  // 聚焦輸入框
  setTimeout(() => nameInput.focus(), 100);

  return { overlay, close };
}

// ==================== 註冊擴展 ====================

document.addEventListener("click", (e) => {
  if (
    activeInput &&
    !activeInput.contains(e.target) &&
    activeDropdown &&
    !activeDropdown.contains(e.target)
  ) {
    hideDropdown();
  }
});

app.registerExtension({
  name: "Comfy.LittleUtility.LoraAutocomplete",

  async beforeRegisterNodeDef(nodeType, nodeData) {
    if (nodeData.name === "LoraSelectorNode") {
      const onNodeCreated = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = function () {
        const r = onNodeCreated
          ? onNodeCreated.apply(this, arguments)
          : undefined;
        const node = this;

        setTimeout(async () => {
          const loraWidget = this.widgets?.find((w) => w.name === "lora_name");
          if (!loraWidget) {
            console.warn("[Little Utility] 找不到 lora_name widget");
            return;
          }

          const inputEl = loraWidget.inputEl;
          if (!inputEl) {
            console.warn("[Little Utility] 找不到 lora_name 輸入元素");
            return;
          }

          let loras = await fetchLoraList();
          // 初始化觸發詞緩存
          if (!triggerWordsCache) {
            await fetchTriggerWords();
          }

          const onSelect = (value) => {
            loraWidget.value = value;
            inputEl.value = value;
            if (node.onWidgetChanged) {
              node.onWidgetChanged(loraWidget.name, value, value, loraWidget);
            }
            node.setDirtyCanvas(true, true);
          };

          inputEl.addEventListener("input", () => {
            const query = inputEl.value;
            // 直接傳遞 null 作為 triggerWords 參數，讓 showDropdown 使用全局緩存
            showDropdown(inputEl, loras, query, onSelect, null);
          });

          inputEl.addEventListener("focus", async () => {
            loras = await fetchLoraList();
            // 確保緩存存在
            if (!triggerWordsCache) {
              await fetchTriggerWords();
            }
            const query = inputEl.value;
            showDropdown(inputEl, loras, query, onSelect, null);
          });

          inputEl.addEventListener("keydown", (e) => {
            handleKeydown(e, onSelect);
          });

          // 添加管理按鈕
          const btnContainer = document.createElement("div");
          btnContainer.style.cssText = "position: relative;";

          const manageBtn = document.createElement("button");
          manageBtn.className = "lora-manage-btn";
          manageBtn.innerHTML = '<span class="icon">+</span> 管理觸發詞';

          manageBtn.addEventListener("click", (e) => {
            e.preventDefault();
            e.stopPropagation();
            createManageDialog(() => {
              // 關閉回調，不需要做什麼，因為緩存已經是全局的並已更新
            });
          });

          // 添加按鈕 widget
          const buttonWidget = node.addDOMWidget(
            "manage_btn",
            "button",
            manageBtn,
            {
              serialize: false,
            },
          );

          console.log("[Little Utility] Lora 自動補全和管理按鈕已啟用");
        }, 100);

        return r;
      };
    }
  },
});

// 預加載
setTimeout(() => {
  fetchLoraList();
  fetchTriggerWords();
}, 1000);
