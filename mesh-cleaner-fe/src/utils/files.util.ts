import {StepLog} from "../types";

export function flattenLogs(logObject: Record<string, StepLog[]>): StepLog[] {
    return Object.entries(logObject).flatMap(([action, steps]) =>
        steps.map((step) => ({action, ...step}))
    );
}

export function createClientLogEntry(step: string, result: string): StepLog {
    return {
        action: "client",
        step,
        result,
        input_vertices: null,
        output_vertices: null,
        input_faces: null,
        output_faces: null,
    };
}