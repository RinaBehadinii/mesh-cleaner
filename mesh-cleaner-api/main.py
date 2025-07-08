from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router  # adjust to your actual routes module

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or ["*"] for all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
