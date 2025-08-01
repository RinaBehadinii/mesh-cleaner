import pymeshlab
from .logging_utils import StepLogger
from .utils import get_bounding_box_dimensions


def run_simplification(ms: pymeshlab.MeshSet, logger: StepLogger = None):
    if logger is None:
        return

    logger.add_step(action="simplification", step="Simplifying mesh", result="Started")

    initial_faces = ms.current_mesh().face_number()
    initial_vertices = ms.current_mesh().vertex_number()
    initial_dims = get_bounding_box_dimensions(ms)

    try:
        ms.apply_filter(
            "meshing_decimation_quadric_edge_collapse",
            targetfacenum=int(initial_faces * 0.5),
            preservenormal=True
        )

        final_faces = ms.current_mesh().face_number()
        final_vertices = ms.current_mesh().vertex_number()
        final_dims = get_bounding_box_dimensions(ms)

        result = (
            "Simplification successful"
            if final_faces < initial_faces
            else "Simplification had no effect (face count not reduced)"
        )

        logger.add_step(
            action="simplification",
            step="Quadric Edge Collapse",
            input_vertices=initial_vertices,
            output_vertices=final_vertices,
            input_faces=initial_faces,
            output_faces=final_faces,
            bounding_box_before=initial_dims,
            bounding_box_after=final_dims,
            result=result
        )

    except pymeshlab.PyMeshLabException as e:
        logger.add_step(
            action="simplification",
            step="Quadric Edge Collapse",
            input_vertices=initial_vertices,
            input_faces=initial_faces,
            bounding_box_before=initial_dims,
            result=f"Skipped: {e}"
        )
