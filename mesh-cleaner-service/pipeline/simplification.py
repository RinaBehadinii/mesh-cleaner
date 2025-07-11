import pymeshlab
from .logging_utils import StepLogger


def get_bounding_box_dimensions(ms: pymeshlab.MeshSet):
    bb = ms.current_mesh().bounding_box()
    min_coords = bb.min()
    max_coords = bb.max()
    dims = [round(max_coords[i] - min_coords[i], 6) for i in range(3)]
    return tuple(dims)


def run_simplification(ms: pymeshlab.MeshSet, logger: StepLogger = None):
    if logger is None:
        return

    logger.add_step(action="simplification", step="Simplifying mesh", result="Started")

    initial_faces = ms.current_mesh().face_number()
    initial_vertices = ms.current_mesh().vertex_number()
    initial_bbox = get_bounding_box_dimensions(ms)

    try:
        ms.apply_filter(
            "meshing_decimation_quadric_edge_collapse",
            targetfacenum=int(initial_faces * 0.5),
            preservenormal=True
        )

        final_faces = ms.current_mesh().face_number()
        final_vertices = ms.current_mesh().vertex_number()
        final_bbox = get_bounding_box_dimensions(ms)

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
            bounding_box_before=initial_bbox,
            bounding_box_after=final_bbox,
            result=result
        )

    except pymeshlab.PyMeshLabException as e:
        logger.add_step(
            action="simplification",
            step="Quadric Edge Collapse",
            input_vertices=initial_vertices,
            input_faces=initial_faces,
            bounding_box_before=initial_bbox,
            result=f"Skipped: {e}"
        )
