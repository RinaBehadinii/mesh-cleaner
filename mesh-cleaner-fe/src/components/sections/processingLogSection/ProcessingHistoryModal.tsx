import {useState} from "react";
import {formatBoundingBox} from "../../../utils/logs.util";
import {useGetLogs} from "../../../hooks/useGetLogs";
import {Modal} from "../../../shared-components/Modal";

export function ProcessingHistoryModal() {
    const [isOpen, setIsOpen] = useState(false);
    const {logs: history, loading,} = useGetLogs(isOpen);

    return (
        <div className="flex justify-end w-full">
            <button
                onClick={() => setIsOpen(true)}
                className="px-4 py-2 rounded-lg text-sm font-semibold transition bg-purple-600 text-white hover:bg-purple-700 cursor-pointer"
            >
                View All Processing History
            </button>

            <Modal open={isOpen} onClose={() => setIsOpen(false)} title="Processing History">
                <div className="max-h-[600px] overflow-y-auto border border-purple-200 rounded-md">
                    {loading ? (
                        <div className="p-4 text-sm text-gray-500">Loading logs...</div>
                    ) : history.length === 0 ? (
                        <div className="p-4 text-sm text-gray-500">No logs available</div>
                    ) : (
                        <table
                            className="min-w-full table-fixed border-separate border-spacing-0 text-sm text-left font-mono bg-white">
                            <thead className="bg-purple-100 sticky top-0 z-20">
                            <tr>
                                <th className="px-2 py-1 border-b border-purple-300">Filename</th>
                                <th className="px-2 py-1 border-b border-purple-300">Input Faces</th>
                                <th className="px-2 py-1 border-b border-purple-300">Output Faces</th>
                                <th className="px-2 py-1 border-b border-purple-300">Δ Faces</th>
                                <th className="px-2 py-1 border-b border-purple-300">Input Vertices</th>
                                <th className="px-2 py-1 border-b border-purple-300">Output Vertices</th>
                                <th className="px-2 py-1 border-b border-purple-300">Δ Vertices</th>
                                <th className="px-2 py-1 border-b border-purple-300">BBox Before</th>
                                <th className="px-2 py-1 border-b border-purple-300">BBox After</th>
                                <th className="px-2 py-1 border-b border-purple-300">Timestamp</th>
                            </tr>
                            </thead>
                            <tbody>
                            {history.map((log, idx) => {
                                const faces = log.mesh_stats?.faces || {};
                                const vertices = log.mesh_stats?.vertices || {};
                                const deltaFaces =
                                    typeof faces.input === "number" && typeof faces.output === "number"
                                        ? faces.input - faces.output
                                        : "–";
                                const deltaVertices =
                                    typeof vertices.input === "number" && typeof vertices.output === "number"
                                        ? vertices.input - vertices.output
                                        : "–";

                                return (
                                    <tr key={idx} className="hover:bg-purple-50">
                                        <td className="px-2 py-1 border-b border-gray-200 break-words max-w-[200px]">
                                            {log.filename}
                                        </td>
                                        <td className="px-2 py-1 border-b border-gray-200">{faces.input ?? "–"}</td>
                                        <td className="px-2 py-1 border-b border-gray-200">{faces.output ?? "–"}</td>
                                        <td className="px-2 py-1 border-b border-gray-200">{deltaFaces}</td>
                                        <td className="px-2 py-1 border-b border-gray-200">{vertices.input ?? "–"}</td>
                                        <td className="px-2 py-1 border-b border-gray-200">{vertices.output ?? "–"}</td>
                                        <td className="px-2 py-1 border-b border-gray-200">{deltaVertices}</td>
                                        <td className="px-2 py-1 border-b border-gray-200 break-words max-w-[250px]">
                                            {formatBoundingBox(log.bounding_box?.before)}
                                        </td>
                                        <td className="px-2 py-1 border-b border-gray-200 break-words max-w-[250px]">
                                            {formatBoundingBox(log.bounding_box?.after)}
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
            </Modal>
        </div>
    );
}
