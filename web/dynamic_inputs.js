import { app } from "../../scripts/app.js";
import {
    applyNodeSize,
    setupRememberNodeSize,
    LITTLE_UTILITY_NODES,
} from "./node_size.js";

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
    
    // 如果移除了插槽，重新計算節點大小（保留使用者手動調整的尺寸）
    if (removed > 0) {
        applyNodeSize(node);
        console.log(`[Little Utility] 節點大小已重新計算`);
    }
}

function setupSwitchAnyNode(nodeType) {
    const inputPrefix = "input";
    const maxCount = 32;

    function getDynamicInputs(node) {
        return node.inputs.filter((i) => i.name.startsWith(inputPrefix));
    }

    function hasAnyInputConnection(node) {
        return getDynamicInputs(node).some((i) => i.link !== null);
    }

    /** 未連線時只保留 input1；有連線時保留「已連線 + 最後一個空槽」 */
    function syncInputSlots(node) {
        const dynamicInputs = getDynamicInputs(node);

        if (!hasAnyInputConnection(node)) {
            while (getDynamicInputs(node).length > 1) {
                const extra = getDynamicInputs(node);
                node.removeInput(node.inputs.indexOf(extra[extra.length - 1]));
            }
            if (getDynamicInputs(node).length === 0) {
                node.addInput(`${inputPrefix}1`, node.outputs[0]?.type || "*");
            } else {
                getDynamicInputs(node)[0].name = `${inputPrefix}1`;
            }
            return;
        }

        let lastConnectedIndex = -1;
        for (let i = 0; i < dynamicInputs.length; i++) {
            if (dynamicInputs[i].link !== null) {
                lastConnectedIndex = i;
            }
        }
        const keepCount = lastConnectedIndex + 2;
        const current = getDynamicInputs(node);
        for (let i = current.length - 1; i >= keepCount; i--) {
            node.removeInput(node.inputs.indexOf(current[i]));
        }

        let slot = 1;
        for (const input of node.inputs) {
            if (input.name.startsWith(inputPrefix)) {
                input.name = `${inputPrefix}${slot}`;
                slot++;
            }
        }
    }

    function updateSelectWidget(node) {
        if (!node.widgets?.[0]) return;
        const count = getDynamicInputs(node).length;
        node.widgets[0].options.max = Math.max(1, count);
        node.widgets[0].value = Math.min(
            Math.max(1, node.widgets[0].value),
            node.widgets[0].options.max
        );
    }

    function lockTypes(node, type) {
        if (!type || type === "*") return;
        for (const input of node.inputs) {
            if (input.name.startsWith(inputPrefix)) {
                input.type = type;
            }
        }
        if (node.outputs?.[0]) {
            node.outputs[0].type = type;
            node.outputs[0].label = type;
            node.outputs[0].name = type;
        }
    }

    const onNodeCreated = nodeType.prototype.onNodeCreated;
    nodeType.prototype.onNodeCreated = function () {
        const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
        setTimeout(() => {
            syncInputSlots(this);
            updateSelectWidget(this);
            applyNodeSize(this);
            this.setDirtyCanvas(true, true);
        }, 10);
        return r;
    };

    const onConnectionsChange = nodeType.prototype.onConnectionsChange;
    nodeType.prototype.onConnectionsChange = function (type, index, connected, link_info) {
        const r = onConnectionsChange
            ? onConnectionsChange.apply(this, arguments)
            : undefined;

        if (!link_info) return r;

        const stackTrace = new Error().stack;
        const isLoading =
            stackTrace.includes("convertToSubgraph") ||
            stackTrace.includes("Subgraph.configure") ||
            stackTrace.includes("loadGraphData") ||
            stackTrace.includes("pasteFromClipboard");

        if (isLoading) {
            updateSelectWidget(this);
            return r;
        }

        // 輸出連線：由下游類型鎖定本節點（不新增輸入槽）
        if (type === 2 && connected && index === 0 && this.outputs[0]?.type === "*") {
            const targetNode = app.graph.getNodeById(link_info.target_id);
            const targetType = targetNode?.inputs?.[link_info.target_slot]?.type;
            if (targetType && targetType !== "*") {
                lockTypes(this, targetType);
            }
            return r;
        }

        if (type !== 1) return r;

        const input = this.inputs[index];
        if (!input?.name.startsWith(inputPrefix)) return r;

        if (connected && this.outputs[0]?.type === "*") {
            const originNode = app.graph.getNodeById(link_info.origin_id);
            const originType = originNode?.outputs?.[link_info.origin_slot]?.type;
            if (originType && originType !== "*") {
                lockTypes(this, originType);
            }
        }

        if (!connected) {
            setTimeout(() => {
                syncInputSlots(this);
                updateSelectWidget(this);
                applyNodeSize(this);
                this.setDirtyCanvas(true, true);
            }, 10);
            return r;
        }

        // 僅當「最後一個」輸入槽被連線時，才新增下一個空槽
        const dynamicInputs = getDynamicInputs(this);
        const lastInput = dynamicInputs[dynamicInputs.length - 1];
        const lastInputIndex = this.inputs.indexOf(lastInput);

        if (
            index === lastInputIndex &&
            lastInput.link !== null &&
            dynamicInputs.length < maxCount
        ) {
            const nextType = this.outputs[0]?.type || "*";
            this.addInput(`${inputPrefix}${dynamicInputs.length + 1}`, nextType);
            applyNodeSize(this);
        }

        updateSelectWidget(this);
        this.setDirtyCanvas(true, true);
        return r;
    };
}

app.registerExtension({
    name: "Comfy.LittleUtility.DynamicInputs",
    
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (LITTLE_UTILITY_NODES.has(nodeData.name)) {
            setupRememberNodeSize(nodeType);
        }

        if (nodeData.name === "SwitchAnyNode") {
            setupSwitchAnyNode(nodeType);
        }

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
                        applyNodeSize(this);
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
