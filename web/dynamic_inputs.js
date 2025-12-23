import { app } from "../../scripts/app.js";

// --- 顯示日誌以確認腳本已讀取 ---
console.log("[Little Utility] JS 腳本加載成功");

app.registerExtension({
    name: "Comfy.LittleUtility.DynamicInputs",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "TextCombineNode" || nodeData.name === "TypeSwitchNode" || nodeData.name === "TypeSwitchAutoNode") {
            
            // 記錄命中
            console.log(`[Little Utility] 正在處理節點原型: ${nodeData.name}`);

            // 保存原始的 onConnectionsChange
            const onConnectionsChange = nodeType.prototype.onConnectionsChange;
            nodeType.prototype.onConnectionsChange = function(type, index, connected, link_info) {
                if (onConnectionsChange) {
                    onConnectionsChange.apply(this, arguments);
                }

                // 只有輸入插槽 (type 1) 變動才觸發
                if (type === 1) {
                    console.log(`[Little Utility] ${this.type} 插槽變動:`, {index, connected});
                    
                    // 文字結合節點邏輯
                    if (this.comfyClass === "TextCombineNode") {
                        const prefix = "text_";
                        const inputs = this.inputs.filter(i => i.name.startsWith(prefix));
                        const lastInput = inputs[inputs.length - 1];
                        
                        if (connected && index === this.inputs.indexOf(lastInput) && inputs.length < 10) {
                            this.addInput(`${prefix}${inputs.length + 1}`, "STRING");
                            this.setDirtyCanvas(true, true);
                        }
                    } 
                    // 類型切換節點邏輯
                    else if (this.comfyClass === "TypeSwitchNode" || this.comfyClass === "TypeSwitchAutoNode") {
                        const hasText = this.inputs.find(i => i.name === "text_input")?.link !== null;
                        const intInput = this.inputs.find(i => i.name === "int_input");
                        const floatInput = this.inputs.find(i => i.name === "float_input");

                        if (hasText && !intInput) {
                            this.addInput("int_input", "INT");
                        }
                        if (intInput && intInput.link !== null && !floatInput) {
                            this.addInput("float_input", "FLOAT");
                        }
                        this.setDirtyCanvas(true, true);
                    }
                }
            };
        }
    },
    // 額外保險：如果節點已經在畫布上，也檢查一次
    nodeCreated(node) {
        if (["TextCombineNode", "TypeSwitchNode", "TypeSwitchAutoNode"].includes(node.comfyClass)) {
            console.log(`[Little Utility] 節點實例建立: ${node.comfyClass}`);
            // 可以在這裡做初始檢查
        }
    }
});
