from typing import Optional


class StepLogger:
    def __init__(self):
        self.steps = []

    def add_step(
            self,
            *,
            action: str,
            step: str,
            result: str,
            input_vertices: Optional[int] = None,
            output_vertices: Optional[int] = None,
            input_faces: Optional[int] = None,
            output_faces: Optional[int] = None,
            bounding_box_before: Optional[tuple] = None,
            bounding_box_after: Optional[tuple] = None,
    ):
        log = {
            "action": action,
            "step": step,
            "result": result,
            "input_vertices": input_vertices,
            "output_vertices": output_vertices,
            "input_faces": input_faces,
            "output_faces": output_faces,
        }

        if bounding_box_before is not None:
            log["bounding_box_before"] = tuple(float(round(x, 6)) for x in bounding_box_before)

        if bounding_box_after is not None:
            log["bounding_box_after"] = tuple(float(round(x, 6)) for x in bounding_box_after)

        self.steps.append(log)

    def get_logs(self):
        return self.steps
