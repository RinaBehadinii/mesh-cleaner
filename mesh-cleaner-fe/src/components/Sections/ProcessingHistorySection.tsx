import {useEffect, useState} from "react";
import {StructuredLog} from "../../types";

function formatBoundingBoxBefore(before?: any): string {
    if (!before) return "–";

    const {min_x, min_y, min_z, max_x, max_y, max_z} = before;
    return [
        min_x?.toFixed(2),
        min_y?.toFixed(2),
        min_z?.toFixed(2),
        max_x?.toFixed(2),
        max_y?.toFixed(2),
        max_z?.toFixed(2),
    ].join(", ");
}

function formatBoundingBoxAfter(after?: any): string {
    if (!after) return "–";

    const {width, height, depth} = after;
    return [
        width?.toFixed(2),
        height?.toFixed(2),
        depth?.toFixed(2),
    ].join(", ");
}

export function ProcessingHistorySection() {
    const [isOpen, setIsOpen] = useState(false);
    const [history, setHistory] = useState<StructuredLog[]>([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (isOpen && history.length === 0) {
            setLoading(true);
            fetch("http://localhost:8000/logs")
                .then((res) => res.json())
                .then((data) => setHistory(data))
                .catch((err) => console.error("Error fetching logs:", err))
                .finally(() => setLoading(false));
        }
    }, [isOpen, history.length]);

    return (
        <div className="bg-white p-8 rounded-2xl shadow-lg space-y-5">
            <div className="flex justify-between items-center">
                <h2 className="text-2xl font-semibold text-purple-700">3. Processing History</h2>
                <button
                    onClick={() => setIsOpen(!isOpen)}
                    className="text-lg font-bold text-purple-700 hover:underline"
                >
                    {isOpen ? "-" : "+"}
                </button>
            </div>

            {isOpen && (
                <div className="max-h-96 overflow-y-auto border border-purple-200 rounded-md">
                    {loading ? (
                        <div className="p-4 text-sm text-gray-500">Loading logs...</div>
                    ) : history.length === 0 ? (
                        <div className="p-4 text-sm text-gray-500">No logs available</div>
                    ) : (
                        <table
                            className="min-w-full table-fixed border-separate border-spacing-0 text-sm text-left font-mono bg-white">
                            <thead className="bg-purple-100 sticky top-0 z-20">
                            <tr>
                                <th className="px-2 py-1 border-b border-purple-300 bg-purple-100">Filename</th>
                                <th className="px-2 py-1 border-b border-purple-300 bg-purple-100">Input Faces</th>
                                <th className="px-2 py-1 border-b border-purple-300 bg-purple-100">Output Faces</th>
                                <th className="px-2 py-1 border-b border-purple-300 bg-purple-100">Δ Faces</th>
                                <th className="px-2 py-1 border-b border-purple-300 bg-purple-100">Input Vertices</th>
                                <th className="px-2 py-1 border-b border-purple-300 bg-purple-100">Output Vertices</th>
                                <th className="px-2 py-1 border-b border-purple-300 bg-purple-100">Δ Vertices</th>
                                <th className="px-2 py-1 border-b border-purple-300 bg-purple-100">BBox Before</th>
                                <th className="px-2 py-1 border-b border-purple-300 bg-purple-100">BBox After</th>
                                <th className="px-2 py-1 border-b border-purple-300 bg-purple-100">Timestamp</th>
                            </tr>
                            </thead>
                            <tbody>
                            {history.map((log, idx) => {
                                const faces = log.mesh_stats?.faces || {};
                                const vertices = log.mesh_stats?.vertices || {};

                                const deltaFaces = typeof faces.input === "number" && typeof faces.output === "number"
                                    ? faces.input - faces.output
                                    : "–";

                                const deltaVertices = typeof vertices.input === "number" && typeof vertices.output === "number"
                                    ? vertices.input - vertices.output
                                    : "–";

                                return (
                                    <tr key={idx} className="hover:bg-purple-50">
                                        <td className="px-2 py-1 border-b border-gray-200 break-words whitespace-normal max-w-[200px]">
                                            {log.filename}
                                        </td>
                                        <td className="px-2 py-1 border-b border-gray-200">{faces.input ?? "–"}</td>
                                        <td className="px-2 py-1 border-b border-gray-200">{faces.output ?? "–"}</td>
                                        <td className="px-2 py-1 border-b border-gray-200">{deltaFaces}</td>
                                        <td className="px-2 py-1 border-b border-gray-200">{vertices.input ?? "–"}</td>
                                        <td className="px-2 py-1 border-b border-gray-200">{vertices.output ?? "–"}</td>
                                        <td className="px-2 py-1 border-b border-gray-200">{deltaVertices}</td>
                                        <td className="px-2 py-1 border-b border-gray-200 break-words whitespace-normal max-w-[250px]">
                                            {formatBoundingBoxBefore(log.bounding_box?.before)}
                                        </td>
                                        <td className="px-2 py-1 border-b border-gray-200 break-words whitespace-normal max-w-[250px]">
                                            {formatBoundingBoxAfter(log.bounding_box?.after)}
                                        </td>
                                        <td className="px-2 py-1 border-b border-gray-200">
                                            {new Date(log.timestamp || "").toLocaleString("en-GB", {
                                                day: "2-digit",
                                                month: "2-digit",
                                                year: "numeric",
                                                hour: "2-digit",
                                                minute: "2-digit",
                                                hour12: false,
                                            })}
                                        </td>
                                    </tr>
                                );
                            })}
                            </tbody>
                        </table>
                    )}
                </div>
            )}
        </div>
    );
}
