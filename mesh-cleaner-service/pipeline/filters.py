import pymeshlab
from .cleanup import run_advanced_cleanup
from .hole_filling import run_hole_filling
from .smoothing import run_smoothing
from .simplification import run_simplification


def run_all_filters(ms: pymeshlab.MeshSet, *, photogrammetry: bool = False, logs: list[str] | None = None):
    run_advanced_cleanup(ms, logs=logs)
    run_hole_filling(ms, logs=logs)
    run_smoothing(ms, photogrammetry=photogrammetry, logs=logs)
    run_simplification(ms, logs=logs)
