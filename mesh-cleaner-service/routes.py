from fastapi import APIRouter, File, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
import os
from uuid import uuid4
from pipeline.runner import process_mesh

router = APIRouter()

UPLOAD_DIR = "meshes/input"
OUTPUT_DIR = "meshes/output"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


@router.post("/clean-mesh")
async def clean_mesh(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    unique_name = uuid4().hex
    input_filename = f"{unique_name}_{file.filename}"
    input_path = os.path.join(UPLOAD_DIR, input_filename)

    with open(input_path, "wb") as f:
        f.write(await file.read())

    output_filename = f"processed_{input_filename}"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    process_mesh(input_path, output_path)

    if not os.path.exists(output_path):
        raise RuntimeError(f"Processed file not found at {output_path}")

    background_tasks.add_task(clean_files, [input_path, output_path])

    return FileResponse(
        path=output_path,
        media_type="application/octet-stream",
        filename=output_filename,
        background=background_tasks
    )


def clean_files(paths: list[str]):
    for path in paths:
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception as err:
            print(f"Warning: Failed to delete {path} — {err}")
