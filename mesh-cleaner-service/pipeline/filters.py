import pymeshlab
from .cleanup import run_advanced_cleanup
from .hole_filling import run_hole_filling
from .smoothing import run_smoothing
from .simplification import run_simplification
from .logging_utils import StepLogger  # Adjust if needed


def run_all_filters(ms: pymeshlab.MeshSet, *, photogrammetry: bool = False, logger: StepLogger):
    run_advanced_cleanup(ms, logger=logger)
    run_hole_filling(ms, logger=logger)
    run_smoothing(ms, photogrammetry=photogrammetry, logger=logger)
    run_simplification(ms, logger=logger)
