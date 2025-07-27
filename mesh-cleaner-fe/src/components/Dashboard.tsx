import {useState} from "react";
import {Header} from "./Sections/Header";
import {UploadMeshSection} from "./Sections/UploadMeshSection";
import {ProcessingLogsSection} from "./Sections/ProcessingLogsSection";
import {ResultSection} from "./Sections/ResultSection";
import {StructuredLog} from "../types";
import {ProcessingHistorySection} from "./Sections/ProcessingHistorySection";

export function Dashboard() {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [logs, setLogs] = useState<StructuredLog[]>([]);
    const [downloadUrl, setDownloadUrl] = useState<string | null>(null);
    const [isProcessing, setIsProcessing] = useState(false);

    const handleUpload = async () => {
        if (!selectedFile) return;

        setIsProcessing(true);
        setLogs([]);

        const formData = new FormData();
        formData.append("file", selectedFile);

        try {
            const res = await fetch("http://localhost:8000/clean-mesh", {
                method: "POST",
                body: formData,
            });

            if (!res.ok) {
                const err = await res.json();
                setIsProcessing(false);
                setLogs((prev) => [
                    ...prev,
                    {
                        action: "client",
                        step: "Upload",
                        result: `Error: ${err.error || res.statusText}`,
                        input_vertices: null,
                        output_vertices: null,
                        input_faces: null,
                        output_faces: null,
                    },
                ]);
                return;
            }

            const result = await res.json();
            setIsProcessing(false);

            if (Array.isArray(result.logs)) {
                setLogs(result.logs);
            }

            const byteCharacters = atob(result.filedata);
            const byteNumbers = Array.from(byteCharacters).map((char) =>
                char.charCodeAt(0)
            );
            const byteArray = new Uint8Array(byteNumbers);
            const blob = new Blob([byteArray], {type: "application/octet-stream"});

            const url = window.URL.createObjectURL(blob);
            setDownloadUrl(url);
            setLogs((prev) => [
                ...prev,
                {
                    action: "client",
                    step: "Download",
                    result: "Cleaned mesh received successfully",
                    input_vertices: null,
                    output_vertices: null,
                    input_faces: null,
                    output_faces: null,
                },
            ]);
        } catch (error) {
            setIsProcessing(false);
            setLogs((prev) => [
                ...prev,
                {
                    action: "client",
                    step: "Upload",
                    result: `Error: ${String(error)}`,
                    input_vertices: null,
                    output_vertices: null,
                    input_faces: null,
                    output_faces: null,
                },
            ]);
        }
    };

    return (
        <div className="min-h-screen bg-gray-100 px-6 py-10 text-gray-800 font-sans">
            <div className="max-w-5xl mx-auto space-y-12">
                <Header/>

                <UploadMeshSection
                    selectedFile={selectedFile}
                    onFileChange={setSelectedFile}
                    onUpload={handleUpload}
                    onDrop={(e) => {
                        e.preventDefault();
                        const file = e.dataTransfer.files?.[0];
                        if (file) setSelectedFile(file);
                    }}
                    onDragOver={(e) => e.preventDefault()}
                />

                <ProcessingLogsSection logs={logs} isProcessing={isProcessing}/>
                <ProcessingHistorySection/>

                <ResultSection downloadUrl={downloadUrl} selectedFile={selectedFile}/>
            </div>
        </div>
    );
}
