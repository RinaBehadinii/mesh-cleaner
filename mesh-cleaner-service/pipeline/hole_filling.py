import pymeshlab


def run_hole_filling(ms: pymeshlab.MeshSet, max_hole_size: int = 100, logs: list[str] | None = None):
    log = logs.append if logs is not None else lambda x: None

    log("Running surface completion...")

    v, f = ms.current_mesh().vertex_number(), ms.current_mesh().face_number()
    try:
        ms.apply_filter("meshing_close_holes", maxholesize=max_hole_size)
        after_v = ms.current_mesh().vertex_number()
        after_f = ms.current_mesh().face_number()

        print("Close Holes:")
        print(f"  Vertices: {v} → {after_v}")
        print(f"  Faces:    {f} → {after_f}")
        log("Close Holes:")
        log(f"  Vertices: {v} → {after_v}")
        log(f"  Faces:    {f} → {after_f}")

        if after_f > f:
            print("   Holes filled\n")
            log("   Holes filled\n")
        else:
            print("No change\n")
            log("No change\n")
    except pymeshlab.PyMeshLabException as e:
        print(f"  Skipped: {e}\n")
        log(f"  Skipped: {e}\n")

    ms.compute_normal_per_vertex()
    print("Recomputed vertex normals\n")
    log("Recomputed vertex normals\n")
