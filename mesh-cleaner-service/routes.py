from fastapi import APIRouter, File, UploadFile, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
import os
import base64
from uuid import uuid4
from pipeline.runner import process_mesh_and_capture_logs
from database import SessionLocal
from models import MeshLog

router = APIRouter()

UPLOAD_DIR = "meshes/input"
OUTPUT_DIR = "meshes/output"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


@router.post("/clean-mesh")
async def clean_mesh(
        file: UploadFile = File(...),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    unique_name = uuid4().hex
    input_filename = f"{unique_name}_{file.filename}"
    input_path = os.path.join(UPLOAD_DIR, input_filename)

    try:
        with open(input_path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save input file: {e}")

    output_filename = f"processed_{input_filename}"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    try:
        logs = process_mesh_and_capture_logs(input_path, output_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Mesh processing failed: {e}")

    if not os.path.exists(output_path):
        raise HTTPException(status_code=500, detail=f"Processed file not found at {output_path}")

    try:
        with open(output_path, "rb") as f:
            file_data = base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read output file: {e}")

    save_log_to_db(output_filename, logs)

    background_tasks.add_task(clean_files, [input_path, output_path])

    return JSONResponse(
        content={
            "filename": output_filename,
            "filedata": file_data,
            "logs": logs,
        }
    )


@router.get("/logs")
def get_all_mesh_logs():
    db = SessionLocal()
    logs = db.query(MeshLog).order_by(MeshLog.timestamp.desc()).all()
    db.close()

    return [
        {
            "id": log.id,
            "filename": log.filename,
            "input_faces": log.input_faces,
            "output_faces": log.output_faces,
            "input_vertices": log.input_vertices,
            "output_vertices": log.output_vertices,
            "timestamp": log.timestamp.isoformat(),
        }
        for log in logs
    ]


def clean_files(paths: list[str]):
    for path in paths:
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception as err:
            print(f"Warning: Failed to delete {path} — {err}")


def save_log_to_db(filename: str, logs: list[dict]):
    if not logs:
        return

    first = next(
        (log for log in logs if log.get("input_faces") is not None and log.get("input_vertices") is not None),
        logs[0]
    )

    last = next(
        (log for log in reversed(logs) if
         log.get("output_faces") is not None and log.get("output_vertices") is not None),
        logs[-1]
    )

    db = SessionLocal()
    entry = MeshLog(
        filename=filename,
        input_vertices=first["input_vertices"],
        output_vertices=last["output_vertices"],
        input_faces=first["input_faces"],
        output_faces=last["output_faces"],
        bounding_box_before=str(first.get("bounding_box_before")),
        bounding_box_after=str(last.get("bounding_box_after")),
        logs=logs,
    )
    db.add(entry)
    db.commit()
    db.close()
