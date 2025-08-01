import pymeshlab
from .logging_utils import StepLogger
from .utils import get_bounding_box_dimensions


def run_smoothing(ms: pymeshlab.MeshSet, photogrammetry: bool = False, logger: StepLogger = None):
    if logger is None:
        return

    try:
        v_before = ms.current_mesh().vertex_number()
        f_before = ms.current_mesh().face_number()
        dims_before = get_bounding_box_dimensions(ms)

        ms.apply_coord_hc_laplacian_smoothing()
        v_after = ms.current_mesh().vertex_number()
        f_after = ms.current_mesh().face_number()
        dims_after = get_bounding_box_dimensions(ms)

        logger.add_step(
            action="smoothing",
            step="HC Laplacian Smoothing",
            input_vertices=v_before,
            output_vertices=v_after,
            input_faces=f_before,
            output_faces=f_after,
            bounding_box_before=dims_before,
            bounding_box_after=dims_after,
            result="Applied HC Laplacian smoothing"
        )

        if photogrammetry:
            v_before = ms.current_mesh().vertex_number()
            f_before = ms.current_mesh().face_number()
            dims_before = get_bounding_box_dimensions(ms)

            ms.apply_coord_laplacian_smoothing_surface_preserving()
            v_after = ms.current_mesh().vertex_number()
            f_after = ms.current_mesh().face_number()
            dims_after = get_bounding_box_dimensions(ms)

            logger.add_step(
                action="smoothing",
                step="Surface‑Preserving Smoothing",
                input_vertices=v_before,
                output_vertices=v_after,
                input_faces=f_before,
                output_faces=f_after,
                bounding_box_before=dims_before,
                bounding_box_after=dims_after,
                result="Applied Surface‑Preserving smoothing"
            )

    except pymeshlab.PyMeshLabException as e:
        logger.add_step(
            action="smoothing",
            step="Smoothing",
            result=f"Skipped: {e}"
        )
