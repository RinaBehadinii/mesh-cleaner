import pymeshlab
from .logging_utils import StepLogger


def get_bounding_box(ms: pymeshlab.MeshSet):
    bb = ms.current_mesh().bounding_box()
    min_coords = bb.min()
    max_coords = bb.max()
    return (
        min_coords[0], min_coords[1], min_coords[2],
        max_coords[0], max_coords[1], max_coords[2]
    )


def run_smoothing(ms: pymeshlab.MeshSet, photogrammetry: bool = False, logger: StepLogger = None):
    if logger is None:
        return

    try:
        before_bbox = get_bounding_box(ms)

        ms.apply_coord_hc_laplacian_smoothing()
        after_bbox = get_bounding_box(ms)

        logger.add_step(
            action="smoothing",
            step="HC Laplacian Smoothing",
            bounding_box_before=before_bbox,
            bounding_box_after=after_bbox,
            result="Applied HC Laplacian smoothing"
        )

        if photogrammetry:
            before_bbox = get_bounding_box(ms)
            ms.apply_coord_laplacian_smoothing_surface_preserving()
            after_bbox = get_bounding_box(ms)

            logger.add_step(
                action="smoothing",
                step="Surface-Preserving Smoothing",
                bounding_box_before=before_bbox,
                bounding_box_after=after_bbox,
                result="Applied Surface-Preserving smoothing"
            )

    except pymeshlab.PyMeshLabException as e:
        logger.add_step(
            action="smoothing",
            step="Smoothing",
            result=f"Skipped: {e}"
        )
