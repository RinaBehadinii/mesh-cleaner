import {useState} from "react";
import {StepLog, Summary} from "../types";
import {cleanMesh} from "../api/cleanMesh";
import {base64ToBlobUrl, createClientLogEntry, flattenLogs} from "../utils/files.util";

type UseCleanMeshResult = {
    isProcessing: boolean;
    logs: StepLog[];
    summary: Summary | null;
    downloadUrl: string | null;
    handleUpload: (file: File | null) => Promise<void>;
    reset: () => void;
};

export function useCleanMesh(): UseCleanMeshResult {
    const [logs, setLogs] = useState<StepLog[]>([]);
    const [summary, setSummary] = useState<Summary | null>(null);
    const [downloadUrl, setDownloadUrl] = useState<string | null>(null);
    const [isProcessing, setIsProcessing] = useState(false);

    const reset = () => {
        setLogs([]);
        setSummary(null);
        setDownloadUrl(null);
    };

    const handleUpload = async (file: File | null) => {
        if (!file) return;

        setIsProcessing(true);
        reset();

        try {
            const result = await cleanMesh(file);

            console.log({result})

            if (result.summary) setSummary(result.summary);
            if (result.logs) setLogs(flattenLogs(result.logs));

            if (result.filedata) {
                const url = base64ToBlobUrl(result.filedata);
                setDownloadUrl(url);
                setLogs((prev) => [...prev, createClientLogEntry("Download", "Cleaned mesh received successfully")]);
            }
        } catch (error) {
            console.log({error})
            setLogs((prev) => [...prev, createClientLogEntry("Upload", `Error: ${String(error)}`)]);
        } finally {
            setIsProcessing(false);
        }
    };

    return {
        isProcessing,
        logs,
        summary,
        downloadUrl,
        handleUpload,
        reset,
    };
}
