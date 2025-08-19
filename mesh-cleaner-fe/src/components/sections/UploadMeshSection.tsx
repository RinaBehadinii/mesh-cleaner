import React, { useRef, useState } from "react";

type UploadMeshSectionProps = {
  selectedFile: File | null;
  onFileChange: (file: File | null) => void;
  onUpload: () => void;
  onDrop: (e: React.DragEvent<HTMLDivElement>) => void;
  onDragOver: (e: React.DragEvent<HTMLDivElement>) => void;
  isProcessing: boolean;
};

export function UploadMeshSection({
  selectedFile,
  onFileChange,
  onUpload,
  onDrop,
  onDragOver,
  isProcessing,
}: UploadMeshSectionProps) {
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const [dragActive, setDragActive] = useState(false);

  const handleDragEnter = () => setDragActive(true);
  const handleDragLeave = () => setDragActive(false);
  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    setDragActive(false);
    onDrop(e);
  };

  return (
    <div className="bg-white p-8 rounded-2xl shadow-lg space-y-5">
      <h2 className="text-2xl font-semibold text-purple-700">1. Upload Mesh</h2>

      <div
        onDrop={handleDrop}
        onDragOver={onDragOver}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        className={`border-2 border-dashed rounded-xl p-8 text-center transition-all duration-200 ease-in-out
                    ${
                      dragActive
                        ? "border-purple-500 bg-purple-100 text-purple-700 shadow-md"
                        : "border-purple-300 bg-purple-50 text-purple-500"
                    }`}
      >
        {selectedFile ? (
          <span className="font-medium text-purple-700">
            {selectedFile.name}
          </span>
        ) : (
          "Drag and drop your OBJ file here"
        )}
      </div>

      <div className="flex flex-wrap items-center justify-between gap-2 text-sm mt-2">
        <input
          ref={fileInputRef}
          type="file"
          accept=".obj"
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) onFileChange(file);
          }}
          className="block flex-1 text-sm file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-purple-100 file:text-purple-700 hover:file:bg-purple-200 cursor-pointer"
        />

        <div className="flex gap-2">
          <button
            disabled={!selectedFile || isProcessing}
            onClick={onUpload}
            className={`px-4 py-2 rounded-lg text-sm font-semibold transition 
                            ${
                              selectedFile && !isProcessing
                                ? "bg-purple-600 text-white hover:bg-purple-700 cursor-pointer"
                                : "bg-purple-300 text-white cursor-not-allowed"
                            }`}
          >
            Upload & Clean
          </button>
          {selectedFile && (
            <button
              disabled={isProcessing}
              onClick={() => {
                onFileChange(null);
                if (fileInputRef.current) {
                  fileInputRef.current.value = "";
                }
              }}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                isProcessing
                  ? "bg-gray-300 text-gray-400 cursor-not-allowed"
                  : "bg-gray-200 text-gray-700 hover:bg-gray-300"
              }`}
            >
              Remove
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
