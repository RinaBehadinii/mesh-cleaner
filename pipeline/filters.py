import pymeshlab


def run_basic_cleanup(ms: pymeshlab.MeshSet):
    print("Running basic cleanup...")
    ms.apply_filter("meshing_remove_duplicate_vertices")
    ms.apply_filter("meshing_remove_unreferenced_vertices")
    ms.apply_filter("meshing_remove_duplicate_faces")
    ms.apply_filter("meshing_repair_non_manifold_edges")
    # Optionally:
    # ms.apply_filter("meshing_remove_connected_component_by_diameter", mincomponentdiag=pymeshlab.Percentage(1.0))


def run_hole_filling(ms: pymeshlab.MeshSet):
    print("Filling holes...")
    try:
        ms.apply_filter("meshing_close_holes", maxholesize=100)
    except pymeshlab.PyMeshLabException as e:
        print(f"Hole filling skipped: {e}")


def run_smoothing(ms: pymeshlab.MeshSet):
    print("Smoothing surface...")
    try:
        ms.apply_filter("smoothing_laplacian", stepsmoothnum=3, boundary=False)
    except pymeshlab.PyMeshLabException as e:
        print(f"Smoothing skipped: {e}")


def run_simplification(ms: pymeshlab.MeshSet):
    print("Simplifying mesh...")
    try:
        ms.apply_filter(
            "simplification_quadric_edge_collapse_decimation",
            targetfacenum=1000,
            preservenormal=True
        )
    except pymeshlab.PyMeshLabException as e:
        print(f"Simplification skipped: {e}")
