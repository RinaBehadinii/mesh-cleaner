import {getJson} from "./apiClient";
import {StructuredLog} from "../types";

export async function getProcessingHistory(): Promise<StructuredLog[]> {
    return getJson<StructuredLog[]>("/logs");
}
