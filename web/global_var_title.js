import { app } from "../../scripts/app.js";

console.log("[Little Utility] Global Var 標題擴展已加載");

// 定義需要處理的節點類型及其變數名稱 widget 索引
const GLOBAL_VAR_NODES = {
    "GlobalVarSetNode": { prefix: "Set_", widgetName: "var_name" },
    "GlobalVarGetNode": { prefix: "Get_", widgetName: "var_name" },
    "GlobalVarGetSelectNode": { prefix: "Get_", widgetName: "var_name" }
};

// 更新節點標題
function updateNodeTitle(node, config) {
    const widget = node.widgets?.find(w => w.name === config.widgetName);
    if (widget && widget.value) {
        const varName = widget.value;
        // 避免重複添加前綴
        if (varName && varName !== "(empty)") {
            node.title = `${config.prefix}${varName}`;
        }
    }
}

app.registerExtension({
    name: "Comfy.LittleUtility.GlobalVarTitle",
    
    async beforeRegisterNodeDef(nodeType, nodeData) {
        const config = GLOBAL_VAR_NODES[nodeData.name];
        if (!config) return;
        
        // 節點創建時
        const onNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function() {
            const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
            
            // 延遲執行以確保 widgets 已初始化
            setTimeout(() => {
                updateNodeTitle(this, config);
                
                // 監聽 widget 值變化
                const widget = this.widgets?.find(w => w.name === config.widgetName);
                if (widget) {
                    const originalCallback = widget.callback;
                    widget.callback = (value) => {
                        if (originalCallback) {
                            originalCallback.call(widget, value);
                        }
                        updateNodeTitle(this, config);
                        this.setDirtyCanvas(true, true);
                    };
                }
            }, 50);
            
            return r;
        };
        
        // 節點配置時（從工作流加載時）
        const onConfigure = nodeType.prototype.onConfigure;
        nodeType.prototype.onConfigure = function(info) {
            const r = onConfigure ? onConfigure.apply(this, arguments) : undefined;
            
            setTimeout(() => {
                updateNodeTitle(this, config);
            }, 50);
            
            return r;
        };
    }
});
