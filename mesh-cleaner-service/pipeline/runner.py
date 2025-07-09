import pymeshlab
import io
from contextlib import redirect_stdout
from .filters import run_all_filters


def process_mesh_and_capture_logs(input_path: str, output_path: str):
    log_output = io.StringIO()

    with redirect_stdout(log_output):
        ms = pymeshlab.MeshSet()
        ms.load_new_mesh(input_path)
        run_all_filters(ms, photogrammetry=True)
        ms.save_current_mesh(output_path)

    logs = log_output.getvalue().strip().splitlines()
    return logs
