import {formatBoundingBox} from "../../../utils/logs.util";
import {Summary} from "../../../types"

type LogSummaryProps = {
    summary: Summary;
};

export function LogSummary({summary}: LogSummaryProps) {
    return (
        <div className="mt-6 border-t border-purple-300 pt-4">
            <div className="text-purple-800 font-bold uppercase mb-1">Summary</div>
            <div className="ml-4">
                <div>
                    Vertices: {summary.vertices.input} → {summary.vertices.output} (Δ {summary.vertices.delta})
                </div>
                <div>
                    Faces: {summary.faces.input} → {summary.faces.output} (Δ {summary.faces.delta})
                </div>
                <div className="mt-1">
                    Bounding Box:
                    <div className="ml-2">Before: {formatBoundingBox(summary.bounding_box?.before)}</div>
                    <div className="ml-2">After: {formatBoundingBox(summary.bounding_box?.after)}</div>
                </div>
            </div>
        </div>
    );
}
