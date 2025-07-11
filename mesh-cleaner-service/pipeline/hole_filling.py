import pymeshlab
from .logging_utils import StepLogger


def run_hole_filling(ms: pymeshlab.MeshSet, max_hole_size: int = 100, logger: StepLogger = None):
    if logger is None:
        return

    logger.add_step(action="hole_filling", step="Surface Completion", result="Started")

    v = ms.current_mesh().vertex_number()
    f = ms.current_mesh().face_number()

    try:
        ms.apply_filter("meshing_close_holes", maxholesize=max_hole_size)
        after_v = ms.current_mesh().vertex_number()
        after_f = ms.current_mesh().face_number()

        result = "Holes filled" if after_f > f else "No change"

        logger.add_step(
            action="hole_filling",
            step="Close Holes",
            input_vertices=v,
            output_vertices=after_v,
            input_faces=f,
            output_faces=after_f,
            result=result
        )

    except pymeshlab.PyMeshLabException as e:
        logger.add_step(
            action="hole_filling",
            step="Close Holes",
            input_vertices=v,
            input_faces=f,
            result=f"Skipped: {e}"
        )

    ms.compute_normal_per_vertex()
    logger.add_step(action="hole_filling", step="Recompute Vertex Normals", result="Completed")
