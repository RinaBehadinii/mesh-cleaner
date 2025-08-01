import pymeshlab


def get_bounding_box_dimensions(ms: pymeshlab.MeshSet) -> tuple[float, float, float]:
    bb = ms.current_mesh().bounding_box()
    min_coords = bb.min()
    max_coords = bb.max()
    dims = [round(max_coords[i] - min_coords[i], 6) for i in range(3)]
    return tuple(dims)
