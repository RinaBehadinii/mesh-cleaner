from fastapi import APIRouter, File, UploadFile, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
import os
import base64
from uuid import uuid4
from pipeline.runner import process_mesh_and_capture_logs

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

    background_tasks.add_task(clean_files, [input_path, output_path])

    return JSONResponse(
        content={
            "filename": output_filename,
            "filedata": file_data,
            "logs": logs,
        }
    )


def clean_files(paths: list[str]):
    for path in paths:
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception as err:
            print(f"Warning: Failed to delete {path} — {err}")
