from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.data.db import init_db
from app.api.routers import router

app = FastAPI(title="Intake Staffing Forecasting POC")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}
