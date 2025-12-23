import { app } from "../../scripts/app.js";

/**
 * [ComfyUI Little Utility] 
 * 動態插槽管理腳本
 */

console.log("[Little Utility] JS 動態輸入擴展已加載成功");

app.registerExtension({
    name: "Comfy.LittleUtility.DynamicInputs",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name === "TextCombineNode") {
            // 監聽連接變動
            const onConnectionsChange = nodeType.prototype.onConnectionsChange;
            nodeType.prototype.onConnectionsChange = function(type, index, connected, link_info) {
                if (onConnectionsChange) {
                    onConnectionsChange.apply(this, arguments);
                }
                manageTextCombineSlots(this);
            };

            // 節點創建時進行清理
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function() {
                if (onNodeCreated) {
                    onNodeCreated.apply(this, arguments);
                }
                manageTextCombineSlots(this);
            };

            // 載入工作流配置時進行清理
            const onConfigure = nodeType.prototype.onConfigure;
            nodeType.prototype.onConfigure = function() {
                if (onConfigure) {
                    onConfigure.apply(this, arguments);
                }
                manageTextCombineSlots(this);
            };
        }
    }
});

/**
 * 管理文字結合節點的插槽
 * 確保始終有一個空插槽在最後，且不超過最大數量 (10)
 * 同時清理重新整理瀏覽器後可能出現的多餘空插槽
 */
function manageTextCombineSlots(node) {
    if (!node.inputs) return;

    const prefix = "text_";
    const maxCount = 10;
    
    // 獲取所有匹配前綴的輸入插槽
    let textInputs = node.inputs.filter(i => i.name.startsWith(prefix));
    
    // 按數字序號排序（處理 text_1, text_2, ...）
    textInputs.sort((a, b) => {
        const n1 = parseInt(a.name.split("_")[1] || "0");
        const n2 = parseInt(b.name.split("_")[1] || "0");
        return n1 - n2;
    });

    // 1. 檢查是否需要增加插槽
    const lastSlot = textInputs[textInputs.length - 1];
    if (lastSlot && lastSlot.link !== null && textInputs.length < maxCount) {
        const nextNum = textInputs.length + 1;
        node.addInput(`${prefix}${nextNum}`, "STRING");
        node.setDirtyCanvas(true, true);
        // 遞歸檢查，確保連鎖連接時能一次補齊
        setTimeout(() => manageTextCombineSlots(node), 1);
        return;
    }

    // 2. 檢查是否需要移除多餘插槽（從後往前檢查）
    let changed = false;
    // 重點：從最後一個插槽開始檢查
    for (let i = node.inputs.length - 1; i >= 0; i--) {
        const input = node.inputs[i];
        if (input.name.startsWith(prefix)) {
            const num = parseInt(input.name.split("_")[1] || "0");
            // 保留 text_1，其餘空插槽如果前一個也是空的，則移除當前這個
            if (num > 1 && input.link === null) {
                const prevName = `${prefix}${num - 1}`;
                const prevInput = node.inputs.find(inp => inp.name === prevName);
                if (prevInput && prevInput.link === null) {
                    node.removeInput(i);
                    changed = true;
                }
            }
        }
    }

    if (changed) {
        node.setDirtyCanvas(true, true);
    }
}
