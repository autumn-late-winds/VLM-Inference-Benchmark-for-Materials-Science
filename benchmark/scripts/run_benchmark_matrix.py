import argparse
import asyncio
import itertools
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

from app.schemas.common import BenchmarkRequest, Deployment
from app.services.benchmark_runner import BenchmarkRunner
from app.services.result_store import ResultStore


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="benchmark/configs/benchmark_concurrency.yaml")
    args = parser.parse_args()
    config = yaml.safe_load((ROOT / args.config).read_text(encoding="utf-8"))
    deployment = Deployment(
        deployment_id=config.get("deployment_id", "matrix"),
        name=config.get("backend_type", "external"),
        backend_type=config["backend_type"],
        base_url=config["base_url"],
        api_key=config.get("api_key", "EMPTY"),
        model_name=config["model_name"],
    )
    store = ResultStore(ROOT / "results", ROOT / "reports")
    for resolution, num_images, concurrency, max_tokens in itertools.product(
        config["image_resolution_list"],
        config["num_images_list"],
        config["concurrency_list"],
        config["max_output_tokens_list"],
    ):
        req = BenchmarkRequest(
            run_name=f"{config['run_name']}_{resolution}_{num_images}img_c{concurrency}",
            dataset_file=config["dataset_file"],
            image_root=config["image_root"],
            input_mode="text_only" if num_images == 0 else config["input_mode"],
            image_resolution=resolution,
            number_of_images=num_images,
            concurrency=concurrency,
            max_output_tokens=max_tokens,
            num_warmup_requests=config["num_warmup_requests"],
            num_measured_requests=config["num_measured_requests"],
            timeout_seconds=config["timeout_seconds"],
            cost_per_gpu_hour_usd=config["cost_per_gpu_hour_usd"],
        )
        result = await BenchmarkRunner(deployment).run(req)
        store.save_run(result["run_id"], result)
        print(result["run_id"], result["summary"])


if __name__ == "__main__":
    asyncio.run(main())

