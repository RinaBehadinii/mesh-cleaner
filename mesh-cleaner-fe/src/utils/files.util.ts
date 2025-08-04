import {StepLog} from "../types";

export function base64ToBlobUrl(base64: string, mime = "application/octet-stream"): string {
    const byteCharacters = atob(base64);
    const byteNumbers = Array.from(byteCharacters).map((c) => c.charCodeAt(0));
    const byteArray = new Uint8Array(byteNumbers);
    const blob = new Blob([byteArray], {type: mime});
    return URL.createObjectURL(blob);
}

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