import pymeshlab
from pipeline.filters import (
    run_basic_cleanup,
    run_hole_filling,
    run_smoothing,
    run_simplification,
)

def process_mesh(input_path: str, output_path: str):
    print("Starting mesh processing...")
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(input_path)

    run_basic_cleanup(ms)
    run_hole_filling(ms)
    run_simplification(ms)
    run_smoothing(ms)

    ms.save_current_mesh(output_path)
    print("Mesh processing complete.")
