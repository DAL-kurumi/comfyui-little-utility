/** 本套件所有節點：記住使用者手動調整後的尺寸 */

export const USER_SIZE_KEY = "little_utility_user_size";

export const LITTLE_UTILITY_NODES = new Set([
    "ImageInfoNode",
    "ImageDownloadNode",
    "TextCombineNode",
    "TextCleanupNode",
    "TextCleanupAdvancedNode",
    "TypeSwitchAutoNode",
    "SwitchAnyNode",
    "LoraSelectorNode",
    "EmptyLatentImageWithFlip",
    "CacheNode",
]);

/** 記錄使用者手動調整後的節點尺寸（會隨 workflow 一併保存） */
export function markUserSize(node) {
    if (!node.size) return;
    node.properties ??= {};
    node.properties[USER_SIZE_KEY] = [node.size[0], node.size[1]];
}

/** 自動調整時：至少容納內容，但不小於使用者曾設定的大小 */
export function applyNodeSize(node) {
    const computed = node.computeSize();
    const saved = node.properties?.[USER_SIZE_KEY];
    if (saved) {
        node.setSize([
            Math.max(computed[0], saved[0]),
            Math.max(computed[1], saved[1]),
        ]);
    } else {
        node.setSize(computed);
    }
}

/** 掛載 onResize / onConfigure，記住手動 resize、載入 workflow 時還原 */
export function setupRememberNodeSize(nodeType) {
    const onResize = nodeType.prototype.onResize;
    nodeType.prototype.onResize = function (size) {
        const r = onResize ? onResize.apply(this, arguments) : undefined;
        markUserSize(this);
        return r;
    };

    const onConfigure = nodeType.prototype.onConfigure;
    nodeType.prototype.onConfigure = function (info) {
        const r = onConfigure ? onConfigure.apply(this, arguments) : undefined;
        if (info?.size) {
            this.properties ??= {};
            this.properties[USER_SIZE_KEY] = [info.size[0], info.size[1]];
        }
        return r;
    };
}
