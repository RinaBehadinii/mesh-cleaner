import os
from sqlalchemy.orm import Session
from database import SessionLocal
from models import MeshLog


def clean_files(paths: list[str]) -> None:
    for path in paths:
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception as err:
            print(f"Warning: Failed to delete {path} — {err}")


def save_log_to_db(filename: str, logs: list[dict]) -> None:
    if not logs:
        return

    first = next(
        (log for log in logs
         if log.get("input_faces") is not None and log.get("input_vertices") is not None),
        logs[0]
    )
    last = next(
        (log for log in reversed(logs)
         if log.get("output_faces") is not None and log.get("output_vertices") is not None),
        logs[-1]
    )

    mesh_stats = {
        "faces": {
            "input": first.get("input_faces"),
            "output": last.get("output_faces")
        },
        "vertices": {
            "input": first.get("input_vertices"),
            "output": last.get("output_vertices")
        }
    }

    bounding_box_before = next(
        (log.get("bounding_box_before") for log in logs if log.get("bounding_box_before")),
        None
    )
    bounding_box_after = next(
        (log.get("bounding_box_after") for log in reversed(logs) if log.get("bounding_box_after")),
        None
    )

    bounding_box = None
    if isinstance(bounding_box_before, (list, tuple)) and len(bounding_box_before) == 3:
        w_before, h_before, d_before = bounding_box_before
        bounding_box = {
            "before": {"width": w_before, "height": h_before, "depth": d_before}
        }

    if isinstance(bounding_box_after, (list, tuple)) and len(bounding_box_after) == 3:
        w_after, h_after, d_after = bounding_box_after
        if bounding_box is None:
            bounding_box = {}
        bounding_box["after"] = {"width": w_after, "height": h_after, "depth": d_after}

    db: Session = SessionLocal()
    try:
        entry = MeshLog(
            filename=filename,
            mesh_stats=mesh_stats,
            bounding_box=bounding_box,
            logs=logs,
        )
        db.add(entry)
        db.commit()
    except Exception as e:
        print(f"Error saving mesh log to DB: {e}")
    finally:
        db.close()


def transform_logs(raw_logs: list[dict]) -> tuple[dict, dict]:
    first = next(
        (log for log in raw_logs
         if log.get("input_faces") is not None and log.get("input_vertices") is not None),
        raw_logs[0]
    )
    last = next(
        (log for log in reversed(raw_logs)
         if log.get("output_faces") is not None and log.get("output_vertices") is not None),
        raw_logs[-1]
    )
    summary = {
        "faces": {
            "input": first.get("input_faces"),
            "output": last.get("output_faces"),
            "delta": (last.get("output_faces") - first.get("input_faces"))
            if first.get("input_faces") is not None and last.get("output_faces") is not None else None
        },
        "vertices": {
            "input": first.get("input_vertices"),
            "output": last.get("output_vertices"),
            "delta": (last.get("output_vertices") - first.get("input_vertices"))
            if first.get("input_vertices") is not None and last.get("output_vertices") is not None else None
        }
    }

    bb_before = next((log.get("bounding_box_before") for log in raw_logs if log.get("bounding_box_before")), None)
    bb_after = next((log.get("bounding_box_after") for log in reversed(raw_logs) if log.get("bounding_box_after")),
                    None)
    if isinstance(bb_before, (list, tuple)) and len(bb_before) == 3:
        w, h, d = bb_before
        summary.setdefault("bounding_box", {})["before"] = {"width": w, "height": h, "depth": d}
    if isinstance(bb_after, (list, tuple)) and len(bb_after) == 3:
        w, h, d = bb_after
        summary.setdefault("bounding_box", {})["after"] = {"width": w, "height": h, "depth": d}

    grouped_logs: dict[str, list[dict]] = {}
    for log in raw_logs:
        action = log.get("action", "unknown")
        entry = {
            "step": log["step"],
            "result": log["result"],
            "input_vertices": log.get("input_vertices"),
            "output_vertices": log.get("output_vertices"),
            "input_faces": log.get("input_faces"),
            "output_faces": log.get("output_faces"),
            "bounding_box_before": None,
            "bounding_box_after": None,
        }
        if isinstance(log.get("bounding_box_before"), (list, tuple)) and len(log["bounding_box_before"]) == 3:
            w, h, d = log["bounding_box_before"]
            entry["bounding_box_before"] = {"width": w, "height": h, "depth": d}
        if isinstance(log.get("bounding_box_after"), (list, tuple)) and len(log["bounding_box_after"]) == 3:
            w, h, d = log["bounding_box_after"]
            entry["bounding_box_after"] = {"width": w, "height": h, "depth": d}

        grouped_logs.setdefault(action, []).append(entry)

    return summary, grouped_logs
