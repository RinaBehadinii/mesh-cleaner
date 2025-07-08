import pymeshlab
from .cleanup import run_advanced_cleanup
from .hole_filling import run_hole_filling
from .smoothing import run_smoothing
from .simplification import run_simplification


def run_all_filters(ms: pymeshlab.MeshSet, *, photogrammetry: bool = False):
    run_advanced_cleanup(ms)
    run_hole_filling(ms)
    run_smoothing(ms, photogrammetry=photogrammetry)
    run_simplification(ms)
