import {StructuredLog} from "../../types";
import {JSX} from "react";

type ProcessingLogsSectionProps = {
    logs: StructuredLog[];
    isProcessing: boolean;
};

export function ProcessingLogsSection({logs, isProcessing}: ProcessingLogsSectionProps) {
    return (
        <div className="bg-white p-8 rounded-2xl shadow-lg space-y-5">
            <h2 className="text-2xl font-semibold text-purple-700">2. Processing Logs</h2>
            <div
                className="bg-purple-50 rounded-md p-5 h-52 overflow-y-auto text-sm font-mono whitespace-pre-wrap border border-purple-200">
                {isProcessing ? (
                    <div className="flex text-purple-700">Processing mesh, please
                        wait...</div>
                ) : logs.length > 0 ? (
                    logs.reduce<JSX.Element[]>((acc, log, idx) => {
                        const prev = logs[idx - 1];
                        const isNewSection = idx === 0 || log.action !== prev?.action;

                        if (isNewSection) {
                            acc.push(
                                <div
                                    key={`section-${log.action}`}
                                    className="mt-4 mb-1 font-bold uppercase text-purple-800"
                                >
                                    {log.action}
                                </div>
                            );
                        }

                        acc.push(
                            <div key={`log-${idx}`} className="ml-4">
                                <span className="font-semibold">{log.step}</span>: {log.result}

                                {(log.input_vertices !== null || log.output_vertices !== null) && (
                                    <div className="ml-2">
                                        Vertices: {log.input_vertices} → {log.output_vertices}
                                    </div>
                                )}

                                {(log.input_faces !== null || log.output_faces !== null) && (
                                    <div className="ml-2">
                                        Faces: {log.input_faces} → {log.output_faces}
                                    </div>
                                )}

                                {log.bounding_box_before && log.bounding_box_after && (
                                    <div className="ml-2">
                                        Bounding box changed:
                                        <div className="ml-2">Before: {JSON.stringify(log.bounding_box_before)}</div>
                                        <div className="ml-2">After: {JSON.stringify(log.bounding_box_after)}</div>
                                    </div>
                                )}
                            </div>
                        );

                        return acc;
                    }, [])
                ) : (
                    "Waiting for file to be processed..."
                )}
            </div>
        </div>
    );
}
