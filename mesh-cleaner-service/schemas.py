from pydantic import BaseModel
from typing import Dict, List, Optional


class BoundingBox(BaseModel):
    width: float
    height: float
    depth: float


class StepLog(BaseModel):
    step: str
    result: str
    input_vertices: Optional[int]
    output_vertices: Optional[int]
    input_faces: Optional[int]
    output_faces: Optional[int]
    bounding_box_before: Optional[BoundingBox]
    bounding_box_after: Optional[BoundingBox]


class SummaryFacesOrVertices(BaseModel):
    input: Optional[int]
    output: Optional[int]
    delta: Optional[int]


class SummaryBoundingBox(BaseModel):
    before: Optional[BoundingBox]
    after: Optional[BoundingBox]


class Summary(BaseModel):
    faces: SummaryFacesOrVertices
    vertices: SummaryFacesOrVertices
    bounding_box: Optional[SummaryBoundingBox]


class CleanMeshResponse(BaseModel):
    filename: str
    download_url: str
    summary: Summary
    logs: Dict[str, List[StepLog]]


class MeshStatsFacesVertices(BaseModel):
    input: int
    output: int


class MeshStats(BaseModel):
    faces: MeshStatsFacesVertices
    vertices: MeshStatsFacesVertices


class BoundingBoxFull(BaseModel):
    width: float
    height: float
    depth: float


class BoundingBoxStructured(BaseModel):
    before: Optional[BoundingBoxFull]
    after: Optional[BoundingBoxFull]


class StructuredLog(BaseModel):
    id: int
    filename: str
    timestamp: str
    mesh_stats: MeshStats
    bounding_box: Optional[BoundingBoxStructured]
