import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "Comfy.LittleUtility.DynamicInputs",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        
        // --- 針對文字結合節點 (TextCombineNode) ---
        if (nodeData.name === "TextCombineNode") {
            const onConnectionsChange = nodeType.prototype.onConnectionsChange;
            nodeType.prototype.onConnectionsChange = function (type, index, connected, link_info) {
                if (onConnectionsChange) onConnectionsChange.apply(this, arguments);
                
                if (type === 1) { // 1 是輸入插槽 (INPUT)
                    // 獲取所有以 text_ 開頭的輸入
                    const textInputs = this.inputs.filter(i => i.name.startsWith("text_"));
                    const lastConnectedIndex = textInputs.reduce((max, input, idx) => input.link !== null ? idx : max, -1);
                    
                    // 如果最後一個有連接的插槽是目前最後一個插槽，且未達 10 個，增加一個
                    if (lastConnectedIndex === textInputs.length - 1 && textInputs.length < 10) {
                        this.addInput(`text_${textInputs.length + 1}`, "STRING");
                    }
                    
                    // 清理多餘的未連接插槽（保留一個空插槽）
                    for (let i = textInputs.length - 1; i >= 1; i--) {
                        if (textInputs[i].link === null && textInputs[i-1].link === null) {
                            this.removeInput(this.inputs.findIndex(inp => inp.name === textInputs[i].name));
                        }
                    }
                }
            };
        }

        // --- 針對類型切換節點 (TypeSwitchNode) ---
        if (nodeData.name === "TypeSwitchNode" || nodeData.name === "TypeSwitchAutoNode") {
            const onConnectionsChange = nodeType.prototype.onConnectionsChange;
            nodeType.prototype.onConnectionsChange = function (type, index, connected, link_info) {
                if (onConnectionsChange) onConnectionsChange.apply(this, arguments);
                
                if (type === 1) {
                    // 初始只有 text_input
                    // 連接 text_input 後 出現 int_input
                    // 連接 int_input 後 出現 float_input
                    const hasText = this.inputs.find(i => i.name === "text_input")?.link !== null;
                    const hasInt = this.inputs.find(i => i.name === "int_input")?.link !== null;
                    
                    if (hasText && !this.inputs.find(i => i.name === "int_input")) {
                        this.addInput("int_input", "INT");
                    }
                    if (hasInt && !this.inputs.find(i => i.name === "float_input")) {
                        this.addInput("float_input", "FLOAT");
                    }

                    // 逆向移除
                    if (!hasInt && this.inputs.find(i => i.name === "float_input")?.link === null) {
                        this.removeInput(this.inputs.findIndex(i => i.name === "float_input"));
                    }
                    if (!hasText && this.inputs.find(i => i.name === "int_input")?.link === null) {
                        this.removeInput(this.inputs.findIndex(i => i.name === "int_input"));
                    }
                }
            };
        }
    },
});
