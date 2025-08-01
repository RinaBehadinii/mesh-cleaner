import pymeshlab
from .logging_utils import StepLogger
from .utils import get_bounding_box_dimensions


def run_advanced_cleanup(ms: pymeshlab.MeshSet, logger: StepLogger):
    logger.add_step(action="cleanup", step="Advanced Cleanup", result="Started")

    def log_change(name: str, before_v: int, before_f: int, before_dims: tuple[float, float, float]):
        after_v = ms.current_mesh().vertex_number()
        after_f = ms.current_mesh().face_number()
        after_dims = get_bounding_box_dimensions(ms)

        changed = (before_v != after_v or before_f != after_f)
        result = "Changes detected" if changed else "No change"

        logger.add_step(
            action="cleanup",
            step=name,
            input_vertices=before_v,
            output_vertices=after_v,
            input_faces=before_f,
            output_faces=after_f,
            bounding_box_before=before_dims,
            bounding_box_after=after_dims,
            result=result
        )

    v, f = ms.current_mesh().vertex_number(), ms.current_mesh().face_number()
    dims = get_bounding_box_dimensions(ms)
    ms.apply_filter("meshing_remove_duplicate_vertices")
    log_change("Remove Duplicate Vertices", v, f, dims)

    v, f = ms.current_mesh().vertex_number(), ms.current_mesh().face_number()
    dims = get_bounding_box_dimensions(ms)
    ms.apply_filter("meshing_remove_unreferenced_vertices")
    log_change("Remove Unreferenced Vertices", v, f, dims)

    v, f = ms.current_mesh().vertex_number(), ms.current_mesh().face_number()
    dims = get_bounding_box_dimensions(ms)
    ms.apply_filter("meshing_remove_duplicate_faces")
    log_change("Remove Duplicate Faces", v, f, dims)

    v, f = ms.current_mesh().vertex_number(), ms.current_mesh().face_number()
    dims = get_bounding_box_dimensions(ms)
    ms.apply_filter("meshing_repair_non_manifold_edges", method="Remove Faces")
    log_change("Repair Non‑Manifold Edges", v, f, dims)

    v, f = ms.current_mesh().vertex_number(), ms.current_mesh().face_number()
    dims = get_bounding_box_dimensions(ms)
    ms.apply_filter(
        "meshing_remove_connected_component_by_diameter",
        mincomponentdiag=pymeshlab.PercentageValue(1.0)
    )
    log_change("Remove Small Components by Diameter", v, f, dims)
