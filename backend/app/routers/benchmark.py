from pathlib import Path

from fastapi import APIRouter

from app.config import get_settings
from app.routers.deployments import registry
from app.schemas.common import BenchmarkRequest
from app.services.benchmark_runner import BenchmarkRunner
from app.services.report_service import build_report
from app.services.result_store import ResultStore

router = APIRouter()


def store() -> ResultStore:
    settings = get_settings()
    return ResultStore(settings.results_dir, settings.reports_dir)


@router.post("/run")
async def run_benchmark(request: BenchmarkRequest):
    settings = get_settings()
    settings.assert_no_local_weight_download()
    deployment = registry().get(request.deployment_id)
    result = await BenchmarkRunner(deployment).run(request)
    store().save_run(result["run_id"], result)
    report = build_report(result)
    store().save_report(result["run_id"], report, result)
    return result


@router.post("/run_matrix")
async def run_matrix(request: BenchmarkRequest):
    return await run_benchmark(request)


@router.get("/runs")
def list_runs():
    return store().list_runs()


@router.get("/runs/{run_id}")
def get_run(run_id: str):
    return store().load_run(run_id)


@router.get("/runs/{run_id}/results")
def get_results(run_id: str):
    return store().load_run(run_id).get("results", [])


@router.get("/runs/{run_id}/download_json")
def download_json(run_id: str):
    return store().load_run(run_id)


@router.get("/runs/{run_id}/download_csv")
def download_csv(run_id: str):
    return {"path": str(get_settings().results_dir / f"{run_id}.csv")}

