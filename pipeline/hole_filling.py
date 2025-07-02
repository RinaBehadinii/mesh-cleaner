import pymeshlab


def run_hole_filling(ms: pymeshlab.MeshSet, max_hole_size: int = 100):
    print("Running surface completion...")

    v, f = ms.current_mesh().vertex_number(), ms.current_mesh().face_number()
    try:
        ms.apply_filter("meshing_close_holes", maxholesize=max_hole_size)
        after_v = ms.current_mesh().vertex_number()
        after_f = ms.current_mesh().face_number()
        print(f"Close Holes:")
        print(f"  Vertices: {v} → {after_v}")
        print(f"  Faces:    {f} → {after_f}")
        print("   Holes filled\n" if after_f > f else "No change\n")
    except pymeshlab.PyMeshLabException as e:
        print(f"  Skipped: {e}\n")

    ms.compute_normal_per_vertex()
    print("Recomputed vertex normals\n")
