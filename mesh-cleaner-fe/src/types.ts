export type StructuredLog = {
    id: number;
    filename: string;
    timestamp: string;

    mesh_stats: {
        faces: {
            input: number;
            output: number;
        };
        vertices: {
            input: number;
            output: number;
        };
    };

    bounding_box?: {
        before?: {
            width: number;
            height: number;
            depth: number;
        };
        after?: {
            width: number;
            height: number;
            depth: number;
        };
    };
};

export type StepLog = {
    filename?: string,
    action: string;
    step: string;
    result: string;
    input_vertices: number | null;
    output_vertices: number | null;
    input_faces: number | null;
    output_faces: number | null;
    bounding_box_before?: string;
    bounding_box_after?: string;
    timestamp?: string;
};
