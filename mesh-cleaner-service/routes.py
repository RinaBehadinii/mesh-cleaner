from fastapi import APIRouter, File, UploadFile, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
import os
import base64
from uuid import uuid4
from pipeline.runner import process_mesh_and_capture_logs
from utils import save_log_to_db, clean_files, transform_logs
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
    summary, grouped_logs = transform_logs(logs)

    background_tasks.add_task(clean_files, [input_path, output_path])

    return JSONResponse(
        content={
            "filename": output_filename,
            "filedata": file_data,
            "summary": summary,
            "logs": grouped_logs,
        }
    )


@router.get("/logs")
def get_all_mesh_logs():
    db = SessionLocal()
    try:
        records = db.query(MeshLog).order_by(MeshLog.timestamp.desc()).all()
        return JSONResponse(content=[
            {
                "id": log.id,
                "filename": log.filename,
                "timestamp": log.timestamp.isoformat() if log.timestamp else None,
                "mesh_stats": log.mesh_stats,
                "bounding_box": log.bounding_box,
            }
            for log in records
        ])
    finally:
        db.close()
