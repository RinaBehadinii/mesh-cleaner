import {formatBoundingBox} from "../../../utils/logs.util";
import {StepLog} from "../../../types";

type LogGroupProps = {
    logs: StepLog[];
};

export function LogGroup({logs}: LogGroupProps) {
    return (
        <>
            {logs.map((log, idx) => {
                const prev = logs[idx - 1];
                const isNewSection = idx === 0 || log.action !== prev?.action;

                return (
                    <div key={idx} className="mb-2">
                        {isNewSection && (
                            <div className="mt-4 mb-1 font-bold uppercase text-purple-800">
                                {log.action}
                            </div>
                        )}

                        <div className="ml-4">
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
                    </div>
                );
            })}
        </>
    );
}
