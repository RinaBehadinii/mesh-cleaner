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

export type BoundingBox = {
    width: number;
    height: number;
    depth: number;
};

export type StepLog = {
    action?: string;
    step: string;
    result: string;
    input_vertices: number | null;
    output_vertices: number | null;
    input_faces: number | null;
    output_faces: number | null;
    bounding_box_before?: BoundingBox;
    bounding_box_after?: BoundingBox;
};

export type Summary = {
    faces: {
        input: number | null;
        output: number | null;
        delta: number | null;
    };
    vertices: {
        input: number | null;
        output: number | null;
        delta: number | null;
    };
    bounding_box?: {
        before?: BoundingBox;
        after?: BoundingBox;
    };
};

export type CleanMeshResponse = {
    filename: string;
    download_url: string;
    summary: Summary;
    logs: Record<string, StepLog[]>;
};

