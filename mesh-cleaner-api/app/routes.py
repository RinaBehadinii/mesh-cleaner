from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import FileResponse
import os
import shutil
from datetime import datetime
from subprocess import run

router = APIRouter()

UPLOAD_DIR = "/app/meshes/input"
OUTPUT_DIR = "/app/meshes/output"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


@router.post("/clean-mesh")
async def clean_mesh():
    # Example input/output paths (adjust as needed)
    input_path = "/app/meshes/input/test.obj"
    output_path = "/app/meshes/output/cleaned_test.obj"

    # Run the mesh-cleaner service
    result = run(["python", "main.py", input_path, output_path], cwd="/mesh-cleaner-service", capture_output=True,
                 text=True)

    if result.returncode != 0:
        return {
            "success": False,
            "error": result.stderr,
        }

    return {
        "success": True,
        "message": "Mesh cleaner script executed",
        "stdout": result.stdout.strip(),
    }
