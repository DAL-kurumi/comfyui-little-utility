import { app } from "../../scripts/app.js";

console.log("[Little Utility] 動態輸入擴展已加載");

// 清理 TextCombineNode 多餘的空插槽
function cleanupEmptySlots(node) {
    if (node.type !== "TextCombineNode") return;
    
    const prefix = "text_";
    const dynamicInputs = node.inputs.filter(i => i.name.startsWith(prefix));
    
    // 找到最後一個有連接的插槽索引
    let lastConnectedIndex = -1;
    for (let i = 0; i < dynamicInputs.length; i++) {
        if (dynamicInputs[i].link !== null) {
            lastConnectedIndex = i;
        }
    }
    
    // 保留：所有已連接的插槽 + 最後一個已連接插槽後的一個空插槽
    const keepCount = lastConnectedIndex + 2; // +1 for next empty slot, +1 for 0-based index
    
    // 移除多餘的空插槽（從後往前移除）
    let removed = 0;
    for (let i = dynamicInputs.length - 1; i >= keepCount; i--) {
        const slotToRemove = dynamicInputs[i];
        const idx = node.inputs.indexOf(slotToRemove);
        if (idx !== -1) {
            node.removeInput(idx);
            removed++;
            console.log(`[Little Utility] 清理空插槽: ${slotToRemove.name}`);
        }
    }
    
    // 如果移除了插槽，重新計算節點大小
    if (removed > 0) {
        node.setSize(node.computeSize());
        console.log(`[Little Utility] 節點大小已重新計算`);
    }
}

app.registerExtension({
    name: "Comfy.LittleUtility.DynamicInputs",
    
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name === "TextCombineNode") {
            
            // 節點創建時的處理（包括加載工作流時）
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function() {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                
                // 延遲執行清理，確保節點已完全初始化
                setTimeout(() => {
                    cleanupEmptySlots(this);
                    this.setDirtyCanvas(true, true);
                }, 10);
                
                return r;
            };
            
            // 連接變化時的處理
            const onConnectionsChange = nodeType.prototype.onConnectionsChange;
            nodeType.prototype.onConnectionsChange = function(type, index, connected, link_info) {
                const r = onConnectionsChange ? onConnectionsChange.apply(this, arguments) : undefined;
                
                if (type === 1) { // INPUT
                    const prefix = "text_";
                    const maxCount = 10;
                    
                    const dynamicInputs = this.inputs.filter(i => i.name.startsWith(prefix));
                    const lastInput = dynamicInputs[dynamicInputs.length - 1];
                    const lastInputIndex = this.inputs.indexOf(lastInput);

                    // 連接時：如果是最後一個插槽被連接，增加新插槽
                    if (connected && index === lastInputIndex && dynamicInputs.length < maxCount) {
                        const newName = `${prefix}${dynamicInputs.length + 1}`;
                        console.log(`[Little Utility] 增加插槽: ${newName}`);
                        this.addInput(newName, "STRING");
                        this.setSize(this.computeSize());
                        this.setDirtyCanvas(true, true);
                    }
                    
                    // 斷開連接時：清理多餘的空插槽
                    if (!connected) {
                        setTimeout(() => {
                            cleanupEmptySlots(this);
                            this.setDirtyCanvas(true, true);
                        }, 10);
                    }
                }
                
                return r;
            };
        }
    }
});
