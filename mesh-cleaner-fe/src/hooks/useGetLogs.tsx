import {useEffect, useState} from "react";
import {StructuredLog} from "../types";
import {getProcessingHistory} from "../api/getProcessingHistory";

export function useGetLogs(isOpen: boolean) {
    const [logs, setLogs] = useState<StructuredLog[]>([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (isOpen && logs.length === 0) {
            setLoading(true);
            getProcessingHistory()
                .then(setLogs)
                .catch((err) => console.error("Error fetching logs:", err))
                .finally(() => setLoading(false));
        }
    }, [isOpen, logs.length]);

    return {logs, loading};
}
