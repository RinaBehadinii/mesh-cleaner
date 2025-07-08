type ProcessingLogsSectionProps = {
    logs: string[];
};

export function ProcessingLogsSection({logs}: ProcessingLogsSectionProps) {
    return (
        <div className="bg-white p-8 rounded-2xl shadow-lg space-y-5">
            <h2 className="text-2xl font-semibold text-purple-700">2. Processing Logs</h2>
            <div
                className="bg-purple-50 rounded-md p-5 h-52 overflow-y-auto text-sm font-mono whitespace-pre-wrap border border-purple-200">
                {logs.length > 0
                    ? logs.map((log, idx) => <div key={idx}>{log}</div>)
                    : "Waiting for file to be processed..."}
            </div>
        </div>
    );
}
