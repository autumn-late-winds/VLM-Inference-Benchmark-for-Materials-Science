from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers import benchmark, datasets, deployments, health, inference, reports


app = FastAPI(title="Materials VLM Inference Benchmark Dashboard API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(deployments.router, prefix="/deployments", tags=["deployments"])
app.include_router(datasets.router, prefix="/datasets", tags=["datasets"])
app.include_router(inference.router, prefix="/inference", tags=["inference"])
app.include_router(benchmark.router, prefix="/benchmark", tags=["benchmark"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])
app.mount("/data", StaticFiles(directory="../data"), name="data")
