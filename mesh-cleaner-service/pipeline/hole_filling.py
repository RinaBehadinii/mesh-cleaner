import pymeshlab
from .logging_utils import StepLogger
from .utils import get_bounding_box_dimensions


def run_hole_filling(ms: pymeshlab.MeshSet, max_hole_size: int = 100, logger: StepLogger = None):
    if logger is None:
        return

    logger.add_step(action="hole_filling", step="Surface Completion", result="Started")

    v_before = ms.current_mesh().vertex_number()
    f_before = ms.current_mesh().face_number()
    dims_before = get_bounding_box_dimensions(ms)

    try:
        ms.apply_filter("meshing_close_holes", maxholesize=max_hole_size)
        v_after = ms.current_mesh().vertex_number()
        f_after = ms.current_mesh().face_number()
        dims_after = get_bounding_box_dimensions(ms)

        result = "Holes filled" if f_after > f_before else "No change"

        logger.add_step(
            action="hole_filling",
            step="Close Holes",
            input_vertices=v_before,
            output_vertices=v_after,
            input_faces=f_before,
            output_faces=f_after,
            bounding_box_before=dims_before,
            bounding_box_after=dims_after,
            result=result
        )

    except pymeshlab.PyMeshLabException as e:
        logger.add_step(
            action="hole_filling",
            step="Close Holes",
            input_vertices=v_before,
            input_faces=f_before,
            bounding_box_before=dims_before,
            result=f"Skipped: {e}"
        )

    ms.compute_normal_per_vertex()
    logger.add_step(
        action="hole_filling",
        step="Recompute Vertex Normals",
        result="Completed"
    )
