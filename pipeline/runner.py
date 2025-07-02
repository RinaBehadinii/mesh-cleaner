import pymeshlab

from pipeline.filters import run_all_filters

def process_mesh(input_path: str, output_path: str):
    print("Starting mesh processing...")
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(input_path)

    run_all_filters(ms, photogrammetry=True)

    ms.save_current_mesh(output_path)
    print("Mesh processing complete.")
