import {BASE_URL} from "../../api/apiClient";

type ResultSectionProps = {
    downloadUrl: string | null;
    filename: string | null;
};

export function ResultSection({downloadUrl, filename}: ResultSectionProps) {
    const disabled = !downloadUrl || !filename;

    return (
        <div className="bg-white p-8 rounded-2xl shadow-lg space-y-5">
            <h2 className="text-2xl font-semibold text-purple-700">4. Result</h2>
            <p className="text-sm text-center text-gray-600">
                {disabled
                    ? "No cleaned mesh available yet."
                    : "The cleaned mesh is ready. You can:"}
            </p>
            <div className="flex justify-center mt-4 gap-4 flex-wrap">
                <a
                    href={`${BASE_URL}${downloadUrl}` ?? "#"}
                    download={filename ?? undefined}
                    className={`px-6 py-2 rounded-lg text-sm font-semibold transition
                        ${disabled
                        ? "bg-purple-300 text-white cursor-not-allowed pointer-events-none"
                        : "bg-purple-600 text-white hover:bg-purple-700 cursor-pointer"
                    }`}
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    Download Cleaned Mesh
                </a>
            </div>
        </div>
    );
}
