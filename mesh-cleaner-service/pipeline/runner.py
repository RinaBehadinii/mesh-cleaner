import pymeshlab
from .filters import run_all_filters
from .logging_utils import StepLogger


def process_mesh_and_capture_logs(input_path: str, output_path: str):
    logger = StepLogger()

    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(input_path)

    run_all_filters(ms, photogrammetry=True, logger=logger)

    ms.save_current_mesh(output_path)

    return logger.get_logs()
