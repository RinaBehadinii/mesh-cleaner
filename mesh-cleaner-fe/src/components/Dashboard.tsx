import {useState} from "react";

export function Dashboard() {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [logs, setLogs] = useState<string[]>([]);
    const [downloadUrl, setDownloadUrl] = useState<string | null>(null);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) setSelectedFile(file);
    };

    const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        const file = e.dataTransfer.files?.[0];
        if (file) setSelectedFile(file);
    };

    const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
        e.preventDefault();
    };

    const handleUpload = async () => {
        if (!selectedFile) return;

        setLogs((prev) => [...prev, "Uploading file..."]);

        const formData = new FormData();
        formData.append("file", selectedFile);

        try {
            const res = await fetch("http://localhost:8000/clean-mesh", {
                method: "POST",
                body: formData,
            });

            if (!res.ok) {
                const err = await res.json();
                setLogs((prev) => [...prev, `Error: ${err.error || res.statusText}`]);
                return;
            }

            const blob = await res.blob();
            const url = window.URL.createObjectURL(blob);
            setDownloadUrl(url);
            setLogs((prev) => [...prev, "Cleaned mesh received successfully"]);
        } catch (error) {
            setLogs((prev) => [...prev, `Error: ${String(error)}`]);
        }
    };

    return (
        <div className="min-h-screen bg-gray-100 px-6 py-10 text-gray-800 font-sans">
            <div className="max-w-5xl mx-auto space-y-12">
                <header className="text-center">
                    <h1 className="text-4xl font-extrabold text-purple-800 tracking-tight">
                        Mesh Cleaner Dashboard
                    </h1>
                    <p className="mt-2 text-base text-gray-600">
                        Upload, clean, and download your 3D mesh with ease
                    </p>
                </header>

                <section className="bg-white p-8 rounded-2xl shadow-lg space-y-5">
                    <h2 className="text-2xl font-semibold text-purple-700">1. Upload Mesh</h2>
                    <div
                        onDrop={handleDrop}
                        onDragOver={handleDragOver}
                        className="border-2 border-dashed border-purple-300 rounded-xl p-8 text-center text-purple-500 bg-purple-50 hover:bg-purple-100 transition"
                    >
                        Drag and drop your OBJ file here
                    </div>
                    <div className="text-center text-sm text-gray-500">or</div>
                    <input
                        type="file"
                        accept=".obj"
                        onChange={handleFileChange}
                        className="block w-full text-sm file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-purple-100 file:text-purple-700 hover:file:bg-purple-200"
                    />
                    {selectedFile && (
                        <div className="text-sm text-purple-600 mt-2 font-medium flex items-center justify-between">
                            <span>Selected: {selectedFile.name}</span>
                            <button
                                onClick={handleUpload}
                                className="ml-4 px-4 py-2 bg-purple-600 text-white rounded-lg text-sm font-semibold hover:bg-purple-700 transition"
                            >
                                Upload & Clean
                            </button>
                        </div>
                    )}
                </section>

                <section className="bg-white p-8 rounded-2xl shadow-lg space-y-5">
                    <h2 className="text-2xl font-semibold text-purple-700">2. Processing Logs</h2>
                    <div
                        className="bg-purple-50 rounded-md p-5 h-52 overflow-y-auto text-sm font-mono whitespace-pre-wrap border border-purple-200">
                        {logs.length > 0
                            ? logs.map((log, idx) => <div key={idx}>{log}</div>)
                            : "Waiting for file to be processed..."}
                    </div>
                </section>

                <section className="bg-white p-8 rounded-2xl shadow-lg space-y-5">
                    <h2 className="text-2xl font-semibold text-purple-700">3. Result</h2>
                    <p className="text-sm text-center text-gray-600">
                        The cleaned mesh is ready. You can:
                    </p>
                    <div className="flex justify-center mt-4 gap-4 flex-wrap">
                        {downloadUrl && (
                            <a
                                href={downloadUrl}
                                download={selectedFile?.name.replace(".obj", "_cleaned.obj")}
                                className="bg-purple-600 text-white hover:bg-purple-700 px-6 py-2 rounded-lg text-sm font-semibold transition"
                            >
                                Download Cleaned Mesh
                            </a>
                        )}
                        {/* MeshLab opening is out of scope unless you have local integrations */}
                    </div>
                </section>
            </div>
        </div>
    );
}
