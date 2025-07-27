export type StructuredLog = {
    filename?: string,
    action: string;
    step: string;
    result: string;
    input_vertices: number | null;
    output_vertices: number | null;
    input_faces: number | null;
    output_faces: number | null;
    bounding_box_before?: number[];
    bounding_box_after?: number[];
    timestamp?: string;
};
