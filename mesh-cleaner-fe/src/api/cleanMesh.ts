import {postForm} from "./apiClient";
import {CleanMeshResponse} from "../types";

export async function cleanMesh(file: File): Promise<CleanMeshResponse> {
    const formData = new FormData();
    formData.append("file", file);

    return postForm<CleanMeshResponse>("/clean-mesh", formData);
}
