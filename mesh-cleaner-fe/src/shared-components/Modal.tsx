import {ReactNode} from "react";

type ModalProps = {
    open: boolean;
    onClose: () => void;
    title?: string;
    children: ReactNode;
};

export function Modal({open, onClose, title, children}: ModalProps) {
    if (!open) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
            <div className="bg-white rounded-2xl shadow-lg w-full max-w-6xl max-h-[90vh] overflow-hidden flex flex-col">
                <div className="flex justify-between items-center p-6 border-b border-gray-200">
                    <h2 className="text-xl font-semibold text-purple-700">{title}</h2>
                    <button
                        onClick={onClose}
                        className="text-purple-700 font-bold text-xl hover:text-purple-900"
                        aria-label="Close modal"
                    >
                        ×
                    </button>
                </div>
                <div className="p-6 overflow-y-auto">{children}</div>
            </div>
        </div>
    );
}
