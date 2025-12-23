import { app } from "../../scripts/app.js";

// --- 顯示日誌以確認腳本已讀取 ---
console.log("[Little Utility] JS 腳本加載成功 v2");

app.registerExtension({
    name: "Comfy.LittleUtility.DynamicInputs",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        // 白名單節點列表
        const dynamicNodes = ["TextCombineNode", "TypeSwitchNode", "TypeSwitchAutoNode"];
        
        if (dynamicNodes.includes(nodeData.name)) {
            
            // 監聽連接變動
            const onConnectionsChange = nodeType.prototype.onConnectionsChange;
            nodeType.prototype.onConnectionsChange = function(type, index, connected, link_info) {
                if (onConnectionsChange) {
                    onConnectionsChange.apply(this, arguments);
                }

                // type 1 是輸入插槽 (INPUT)
                if (type === 1) {
                    let prefix = "";
                    let maxCount = 10;
                    let inputType = "*";

                    if (this.comfyClass === "TextCombineNode") {
                        prefix = "text_";
                        inputType = "STRING";
                    } else if (this.comfyClass === "TypeSwitchNode" || this.comfyClass === "TypeSwitchAutoNode") {
                        prefix = "input_";
                        inputType = "*";
                        maxCount = 5; // 類型切換通常不需要太多輸入，設為 5
                    }

                    if (prefix) {
                        const dynamicInputs = this.inputs.filter(i => i.name.startsWith(prefix));
                        const lastInput = dynamicInputs[dynamicInputs.length - 1];
                        const lastInputIndex = this.inputs.indexOf(lastInput);

                        // 如果最後一個插槽被連接，且未達上限，增加新插槽
                        if (connected && index === lastInputIndex && dynamicInputs.length < maxCount) {
                            const newName = `${prefix}${dynamicInputs.length + 1}`;
                            console.log(`[Little Utility] 為 ${this.type} 增加插槽: ${newName}`);
                            this.addInput(newName, inputType);
                            this.setDirtyCanvas(true, true);
                        }

                        // 自動移除多餘的空插槽（保留一個空插槽）
                        if (dynamicInputs.length > 1) {
                            for (let i = dynamicInputs.length - 1; i >= 1; i--) {
                                const current = dynamicInputs[i];
                                const prev = dynamicInputs[i-1];
                                // 如果最後兩個都是空的，則移除最後一個
                                if (current.link === null && prev.link === null) {
                                    const idx = this.inputs.indexOf(current);
                                    if (idx !== -1) {
                                        this.removeInput(idx);
                                        console.log(`[Little Utility] 移除多餘插槽: ${current.name}`);
                                    }
                                }
                            }
                        }
                    }
                }
            };
        }
    }
});
