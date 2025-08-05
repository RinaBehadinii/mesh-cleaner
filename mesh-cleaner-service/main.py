from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from database import Base, engine
import threading
import time
import os

OUTPUT_DIR = "meshes/output"
MAX_FILE_AGE_SECONDS = 120


def cleanup_output_dir(output_dir, max_age_seconds=MAX_FILE_AGE_SECONDS):
    while True:
        now = time.time()
        for filename in os.listdir(output_dir):
            file_path = os.path.join(output_dir, filename)
            if os.path.isfile(file_path):
                if now - os.path.getmtime(file_path) > max_age_seconds:
                    try:
                        os.remove(file_path)
                        print(f"Deleted old mesh file: {file_path}")
                    except Exception as e:
                        print(f"Error deleting {file_path}: {e}")
        time.sleep(30)


threading.Thread(target=cleanup_output_dir, args=(OUTPUT_DIR,), daemon=True).start()

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
