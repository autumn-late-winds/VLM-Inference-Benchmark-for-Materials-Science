import argparse
import asyncio
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from app.schemas.common import BenchmarkRequest, Deployment
from app.services.benchmark_runner import BenchmarkRunner
from app.services.report_service import build_report
from app.services.result_store import ResultStore


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="benchmark/configs/benchmark_small.yaml")
    args = parser.parse_args()
    config = yaml.safe_load((ROOT / args.config).read_text(encoding="utf-8"))
    request = BenchmarkRequest(
        run_name=config["run_name"],
        deployment_id=config.get("deployment_id"),
        dataset_file=config["dataset_file"],
        image_root=config["image_root"],
        input_mode=config["input_mode"],
        image_resolution=config["image_resolution_list"][0],
        number_of_images=config["num_images_list"][0],
        concurrency=config["concurrency_list"][0],
        max_output_tokens=config["max_output_tokens_list"][0],
        num_warmup_requests=config["num_warmup_requests"],
        num_measured_requests=config["num_measured_requests"],
        stream=config["stream"],
        timeout_seconds=config["timeout_seconds"],
        temperature=config["temperature"],
        save_model_responses=config["save_model_responses"],
        cost_per_gpu_hour_usd=config["cost_per_gpu_hour_usd"],
        notes=config.get("notes", ""),
    )
    deployment = Deployment(
        deployment_id=config.get("deployment_id", "cli"),
        name=config.get("backend_type", "external"),
        backend_type=config["backend_type"],
        base_url=config["base_url"],
        api_key=config.get("api_key", "EMPTY"),
        model_name=config["model_name"],
    )
    result = await BenchmarkRunner(deployment).run(request)
    store = ResultStore(ROOT / "results", ROOT / "reports")
    store.save_run(result["run_id"], result)
    store.save_report(result["run_id"], build_report(result), result)
    print(result["run_id"])
    print(result["summary"])


if __name__ == "__main__":
    asyncio.run(main())

