export function formatBoundingBox(box?: any): string {
    if (!box) return "–";
    const {width, height, depth} = box;
    return [
        width?.toFixed(2),
        height?.toFixed(2),
        depth?.toFixed(2),
    ].join(", ");
}