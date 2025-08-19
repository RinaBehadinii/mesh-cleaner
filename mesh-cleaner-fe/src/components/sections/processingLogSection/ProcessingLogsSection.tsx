import {StepLog, Summary} from "../../../types";
import {LogGroup} from "./LogGroup";
import {LogSummary} from "./LogSummary";
import {ProcessingHistoryModal} from "./ProcessingHistoryModal";

type ProcessingLogsSectionProps = {
    logs: StepLog[];
    isProcessing: boolean;
    summary?: Summary | null;
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
                    <LogGroup logs={logs}/>
                ) : (
                    "Nothing to show yet. Upload a file to generate logs."
                )}

                {!isProcessing && summary && <LogSummary summary={summary}/>}
            </div>

            <ProcessingHistoryModal isProcessing={isProcessing}/>
        </div>
    );
}
