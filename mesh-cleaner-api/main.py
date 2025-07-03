from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
import shutil
import os
import subprocess

app = FastAPI()

@app.post("/clean")
async def clean_mesh(file: UploadFile = File(...), filename: str = Form(...)):
    input_path = f"./meshes/{filename}"
    output_path = f"./meshes/cleaned_{filename}"

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = subprocess.run(
        ["python", "main.py", input_path, output_path],
        cwd="../mesh-cleaner-service"
    )

    if result.returncode != 0:
        return {"error": "Mesh cleaning failed"}

    return FileResponse(output_path, media_type="application/octet-stream", filename=f"cleaned_{filename}")
