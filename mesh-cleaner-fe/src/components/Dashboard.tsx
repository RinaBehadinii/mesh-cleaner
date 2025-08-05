import {useState} from "react";
import {Header} from "./sections/Header";
import {UploadMeshSection} from "./sections/UploadMeshSection";
import {ProcessingLogsSection} from "./sections/processingLogSection/ProcessingLogsSection";
import {ResultSection} from "./sections/ResultSection";
import {useCleanMesh} from "../hooks/useCleanMesh";

export function Dashboard() {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);

    const {
        isProcessing,
        logs,
        summary,
        downloadUrl,
        handleUpload,
        reset,
        filename
    } = useCleanMesh();

    const onSetSelectedFile = (file: File | null) => {
        setSelectedFile(file);
        reset();
    };

    return (
        <div className="min-h-screen bg-gray-100 px-6 py-10 text-gray-800 font-sans">
            <div className="max-w-5xl mx-auto space-y-12">
                <Header/>

                <UploadMeshSection
                    selectedFile={selectedFile}
                    onFileChange={onSetSelectedFile}
                    onUpload={() => handleUpload(selectedFile)}
                    onDrop={(e) => {
                        e.preventDefault();
                        const file = e.dataTransfer.files?.[0];
                        if (file) onSetSelectedFile(file);
                    }}
                    onDragOver={(e) => e.preventDefault()}
                />

                <ProcessingLogsSection logs={logs} isProcessing={isProcessing} summary={summary}/>
                <ResultSection downloadUrl={downloadUrl} filename={filename}/>
            </div>
        </div>
    );
}
