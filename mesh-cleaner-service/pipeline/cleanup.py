import pymeshlab
from .logging_utils import StepLogger


def run_advanced_cleanup(ms: pymeshlab.MeshSet, logger: StepLogger):
    logger.add_step(action="cleanup", step="Advanced Cleanup", result="Started")

    def log_change(name: str, before_v: int, before_f: int):
        after_v = ms.current_mesh().vertex_number()
        after_f = ms.current_mesh().face_number()

        changed = (before_v != after_v or before_f != after_f)
        result = "Changes detected" if changed else "No change"

        logger.add_step(
            action="cleanup",
            step=name,
            input_vertices=before_v,
            output_vertices=after_v,
            input_faces=before_f,
            output_faces=after_f,
            result=result
        )

    v, f = ms.current_mesh().vertex_number(), ms.current_mesh().face_number()
    ms.apply_filter("meshing_remove_duplicate_vertices")
    log_change("Remove Duplicate Vertices", v, f)

    v, f = ms.current_mesh().vertex_number(), ms.current_mesh().face_number()
    ms.apply_filter("meshing_remove_unreferenced_vertices")
    log_change("Remove Unreferenced Vertices", v, f)

    v, f = ms.current_mesh().vertex_number(), ms.current_mesh().face_number()
    ms.apply_filter("meshing_remove_duplicate_faces")
    log_change("Remove Duplicate Faces", v, f)

    v, f = ms.current_mesh().vertex_number(), ms.current_mesh().face_number()
    ms.apply_filter("meshing_repair_non_manifold_edges", method="Remove Faces")
    log_change("Repair Non-Manifold Edges", v, f)

    v, f = ms.current_mesh().vertex_number(), ms.current_mesh().face_number()
    ms.apply_filter(
        "meshing_remove_connected_component_by_diameter",
        mincomponentdiag=pymeshlab.PercentageValue(1.0)
    )
    log_change("Remove Small Components by Diameter", v, f)
