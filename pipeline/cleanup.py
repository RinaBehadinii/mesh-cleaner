import pymeshlab


def run_advanced_cleanup(ms: pymeshlab.MeshSet):
    print("Running advanced cleanup...")

    def log_change(name: str, before_v: int, before_f: int):
        after_v = ms.current_mesh().vertex_number()
        after_f = ms.current_mesh().face_number()
        print(f"{name}:")
        print(f"  Vertices: {before_v} → {after_v}")
        print(f"  Faces:    {before_f} → {after_f}")
        if before_v == after_v and before_f == after_f:
            print("No change\n")
        else:
            print("Changes detected\n")

    v, f = ms.current_mesh().vertex_number(), ms.current_mesh().face_number()
    ms.apply_filter("meshing_remove_duplicate_vertices")
    log_change("1. Remove Duplicate Vertices", v, f)

    v, f = ms.current_mesh().vertex_number(), ms.current_mesh().face_number()
    ms.apply_filter("meshing_remove_unreferenced_vertices")
    log_change("2. Remove Unreferenced Vertices", v, f)

    v, f = ms.current_mesh().vertex_number(), ms.current_mesh().face_number()
    ms.apply_filter("meshing_remove_duplicate_faces")
    log_change("3. Remove Duplicate Faces", v, f)

    v, f = ms.current_mesh().vertex_number(), ms.current_mesh().face_number()
    ms.apply_filter("meshing_repair_non_manifold_edges", method="Remove Faces")
    log_change("4. Repair Non-Manifold Edges", v, f)

    v, f = ms.current_mesh().vertex_number(), ms.current_mesh().face_number()
    ms.apply_filter(
        "meshing_remove_connected_component_by_diameter",
        mincomponentdiag=pymeshlab.PercentageValue(1.0)
    )
    log_change("5. Remove Small Components by Diameter", v, f)
