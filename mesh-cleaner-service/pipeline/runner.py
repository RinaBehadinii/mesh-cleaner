import pymeshlab
from .filters import run_all_filters
from .logging_utils import StepLogger  # Adjust the import path if needed


def process_mesh_and_capture_logs(input_path: str, output_path: str):
    logger = StepLogger()
    logger.add_step(
        action="init",
        step="Start Processing",
        result="Started mesh processing"
    )

    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(input_path)

    run_all_filters(ms, photogrammetry=True, logger=logger)

    ms.save_current_mesh(output_path)

    logger.add_step(
        action="finalize",
        step="Finish Processing",
        result="Mesh processing complete"
    )

    return logger.get_logs()
