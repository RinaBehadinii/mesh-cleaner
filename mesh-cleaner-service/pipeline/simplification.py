import pymeshlab


def get_bounding_box_dimensions(ms: pymeshlab.MeshSet):
    bb = ms.current_mesh().bounding_box()
    min_coords = bb.min()
    max_coords = bb.max()
    dims = [round(max_coords[i] - min_coords[i], 6) for i in range(3)]
    return tuple(dims)


def run_simplification(ms: pymeshlab.MeshSet, logs: list[str] = None):
    if logs is None:
        logs = []

    print("Simplifying mesh...")
    logs.append("Simplifying mesh...")

    initial_faces = ms.current_mesh().face_number()
    initial_vertices = ms.current_mesh().vertex_number()
    initial_bbox = get_bounding_box_dimensions(ms)

    print(f"Faces before:   {initial_faces}")
    print(f"Vertices before: {initial_vertices}")
    print(f"Bounding box (x, y, z): {initial_bbox}")
    logs.append(f"Faces before:   {initial_faces}")
    logs.append(f"Vertices before: {initial_vertices}")
    logs.append(f"Bounding box (x, y, z): {initial_bbox}")

    try:
        ms.apply_filter(
            "meshing_decimation_quadric_edge_collapse",
            targetfacenum=int(initial_faces * 0.5),
            preservenormal=True
        )

        final_faces = ms.current_mesh().face_number()
        final_vertices = ms.current_mesh().vertex_number()
        final_bbox = get_bounding_box_dimensions(ms)

        print(f"Faces after:    {final_faces}")
        print(f"Vertices after: {final_vertices}")
        print(f"Bounding box (x, y, z): {final_bbox}")
        logs.append(f"Faces after:    {final_faces}")
        logs.append(f"Vertices after: {final_vertices}")
        logs.append(f"Bounding box (x, y, z): {final_bbox}")

        if final_faces < initial_faces:
            msg = "Simplification successful\n"
        else:
            msg = "Simplification had no effect (face count not reduced)\n"

        print(msg)
        logs.append(msg.strip())

    except pymeshlab.PyMeshLabException as e:
        err_msg = f"Simplification skipped: {e}\n"
        print(err_msg)
        logs.append(err_msg.strip())
