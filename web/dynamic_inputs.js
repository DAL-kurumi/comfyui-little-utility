import { app } from "../../scripts/app.js";

/**
 * [ComfyUI Little Utility] 
 * 動態插槽管理腳本 v4
 */

console.log("[Little Utility] 動態輸入控制腳本已啟動");

app.registerExtension({
    name: "Comfy.LittleUtility.DynamicInputs",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name === "TextCombineNode") {
            
            // 1. 監聽連接變動
            const onConnectionsChange = nodeType.prototype.onConnectionsChange;
            nodeType.prototype.onConnectionsChange = function(slotType, slotIndex, isConnected) {
                const r = onConnectionsChange ? onConnectionsChange.apply(this, arguments) : undefined;
                // 使用延時確保 LiteGraph 狀態已更新
                setTimeout(() => manageTextCombineSlots(this), 10);
                return r;
            };

            // 2. 監聽節點配置（載入工作流或重新整理時觸發）
            const onConfigure = nodeType.prototype.onConfigure;
            nodeType.prototype.onConfigure = function() {
                const r = onConfigure ? onConfigure.apply(this, arguments) : undefined;
                setTimeout(() => manageTextCombineSlots(this), 100); // 給予更長的延遲確保穩定
                return r;
            };

            // 3. 節點被添加到畫布時
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function() {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                setTimeout(() => manageTextCombineSlots(this), 100);
                return r;
            };
        }
    }
});

/**
 * 管理文字結合節點的插槽
 * 規則：
 * - 如果最後一個插槽有連線，且未滿 10 個，則增加一個新的。
 * - 如果末尾有多個未連線的插槽，則剪掉多餘的，只保留一個空的。
 */
function manageTextCombineSlots(node) {
    if (!node.inputs || !node.type.includes("TextCombineNode")) return;

    const prefix = "text_";
    const maxCount = 10;
    
    // 獲取所有 text_ 開頭的插槽並按照數字排序
    let getTextInputs = () => node.inputs.filter(i => i.name.startsWith(prefix))
        .sort((a, b) => {
            const n1 = parseInt(a.name.split("_")[1]) || 0;
            const n2 = parseInt(b.name.split("_")[1]) || 0;
            return n1 - n2;
        });

    let textInputs = getTextInputs();
    if (textInputs.length === 0) return;

    let changed = false;

    // --- A. 增加邏輯 ---
    const lastInput = textInputs[textInputs.length - 1];
    if (lastInput.link !== null && textInputs.length < maxCount) {
        const nextNum = parseInt(lastInput.name.split("_")[1]) + 1;
        node.addInput(`${prefix}${nextNum}`, "STRING");
        changed = true;
        // 遞歸檢查一次（防抖處理）
        setTimeout(() => manageTextCombineSlots(node), 20);
    }

    // --- B. 移除邏輯 ---
    // 從後往前檢查，如果最後兩個插槽都是空的，則移除最後一個
    textInputs = getTextInputs(); // 重新獲取最新的插槽列表
    if (textInputs.length > 1) {
        for (let i = textInputs.length - 1; i >= 1; i--) {
            const current = textInputs[i];
            const prev = textInputs[i-1];
            
            // 如果當前是空的，且它的前一個也是空的，則裁掉當前這個
            if (current.link === null && prev.link === null) {
                const inputIndex = node.inputs.indexOf(current);
                if (inputIndex !== -1) {
                    node.removeInput(inputIndex);
                    changed = true;
                }
            } else {
                // 一旦遇到有連現或唯一的空插槽，就停止裁剪（保持順序）
                break;
            }
        }
    }

    if (changed) {
        node.setDirtyCanvas(true, true);
    }
}
