import {StepLog} from "../../types";
import {JSX} from "react";
import {formatBoundingBox} from "./ProcessingHistorySection";

type ProcessingLogsSectionProps = {
    logs: StepLog[];
    isProcessing: boolean;
    summary?: {
        faces: { input: number; output: number; delta: number };
        vertices: { input: number; output: number; delta: number };
        bounding_box: {
            before: { width: number; height: number; depth: number };
            after: { width: number; height: number; depth: number };
        };
    } | null;
};

export function ProcessingLogsSection({
                                          logs,
                                          isProcessing,
                                          summary,
                                      }: ProcessingLogsSectionProps) {
    return (
        <div className="bg-white p-8 rounded-2xl shadow-lg space-y-5">
            <h2 className="text-2xl font-semibold text-purple-700">2. Processing Logs</h2>
            <div
                className="bg-purple-50 rounded-md p-5 h-52 overflow-y-auto text-sm font-mono whitespace-pre-wrap border border-purple-200">
                {isProcessing ? (
                    <div className="flex place-self-center items-center h-full text-purple-700">
                        Processing mesh, please wait...
                    </div>
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
                            <div key={`log-${idx}`} className="ml-4 mb-2">
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
                                        Bounding Box:
                                        <div className="ml-2">
                                            Before: {formatBoundingBox(log.bounding_box_before)}
                                        </div>
                                        <div className="ml-2">
                                            After: {formatBoundingBox(log.bounding_box_after)}
                                        </div>
                                    </div>
                                )}
                            </div>
                        );

                        return acc;
                    }, [])
                ) : (
                    "Nothing to show yet. Upload a file to generate logs."
                )}

                {!isProcessing && summary && (
                    <div className="mt-6 border-t border-purple-300 pt-4">
                        <div className="text-purple-800 font-bold uppercase mb-1">Summary</div>
                        <div className="ml-4">
                            <div>
                                Vertices: {summary.vertices.input} → {summary.vertices.output} (
                                Δ {summary.vertices.delta})
                            </div>
                            <div>
                                Faces: {summary.faces.input} → {summary.faces.output} (Δ{" "}
                                {summary.faces.delta})
                            </div>
                            <div className="mt-1">
                                Bounding Box:
                                <div className="ml-2">
                                    Before: {formatBoundingBox(summary.bounding_box.before)}
                                </div>
                                <div className="ml-2">
                                    After: {formatBoundingBox(summary.bounding_box.after)}
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
