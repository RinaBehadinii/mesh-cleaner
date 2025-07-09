import pymeshlab


def get_bounding_box(ms: pymeshlab.MeshSet):
    bb = ms.current_mesh().bounding_box()
    min_coords = bb.min()
    max_coords = bb.max()
    return (
        min_coords[0], min_coords[1], min_coords[2],
        max_coords[0], max_coords[1], max_coords[2]
    )


def run_smoothing(ms: pymeshlab.MeshSet, photogrammetry: bool = False, logs: list[str] = None):
    if logs is None:
        logs = []

    logs.append("Smoothing surface...")
    print("Smoothing surface...")

    try:
        before = get_bounding_box(ms)

        ms.apply_coord_hc_laplacian_smoothing()
        logs.append("Applied HC Laplacian smoothing")
        print("Applied HC Laplacian smoothing")

        if photogrammetry:
            ms.apply_coord_laplacian_smoothing_surface_preserving()
            logs.append("Applied Surface-Preserving smoothing")
            print("Applied Surface-Preserving smoothing")

        after = get_bounding_box(ms)

        if before != after:
            logs.append("Smoothing changed the geometry (bounding box updated)\n")
            print("Smoothing changed the geometry (bounding box updated)\n")
        else:
            logs.append("No geometric change detected after smoothing\n")
            print("No geometric change detected after smoothing\n")

    except pymeshlab.PyMeshLabException as e:
        logs.append(f"Smoothing skipped: {e}\n")
        print(f"Smoothing skipped: {e}\n")
