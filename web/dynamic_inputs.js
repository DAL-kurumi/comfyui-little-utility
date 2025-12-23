import { app } from "../../scripts/app.js";

console.log("[Little Utility] JS 腳本加載成功 v3");

app.registerExtension({
    name: "Comfy.LittleUtility.DynamicInputs",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        
        // --- 針對文字結合節點 (TextCombineNode) 使用動態插槽 ---
        if (nodeData.name === "TextCombineNode") {
            const onConnectionsChange = nodeType.prototype.onConnectionsChange;
            nodeType.prototype.onConnectionsChange = function(type, index, connected, link_info) {
                if (onConnectionsChange) {
                    onConnectionsChange.apply(this, arguments);
                }

                // type 1 是輸入插槽 (INPUT)
                if (type === 1) {
                    const prefix = "text_";
                    const maxCount = 10;
                    
                    const dynamicInputs = this.inputs.filter(i => i.name.startsWith(prefix));
                    const lastInput = dynamicInputs[dynamicInputs.length - 1];
                    const lastInputIndex = this.inputs.indexOf(lastInput);

                    // 如果最後一個插槽被連接，且未達上限，增加新插槽
                    if (connected && index === lastInputIndex && dynamicInputs.length < maxCount) {
                        const newName = `${prefix}${dynamicInputs.length + 1}`;
                        console.log(`[Little Utility] 為文字結合增加插槽: ${newName}`);
                        this.addInput(newName, "STRING");
                        this.setDirtyCanvas(true, true);
                    }

                    // 自動移除多餘的空插槽（保留一個空插槽）
                    if (dynamicInputs.length > 1) {
                        for (let i = dynamicInputs.length - 1; i >= 1; i--) {
                            const current = dynamicInputs[i];
                            const prev = dynamicInputs[i-1];
                            if (current.link === null && prev.link === null) {
                                const idx = this.inputs.indexOf(current);
                                if (idx !== -1) {
                                    this.removeInput(idx);
                                }
                            }
                        }
                    }
                }
            };
        }
    }
});
