import asyncio
import statistics
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List

from app.schemas.common import BenchmarkRequest, Deployment
from app.services.cost_estimator import estimate_cost
from app.services.dataset_service import load_jsonl
from app.services.multimodal_openai_client import MultimodalOpenAIClient
from app.services.quality_evaluator import evaluate_response


def percentile(values: List[float], p: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round((p / 100) * (len(ordered) - 1))))
    return ordered[index]


class BenchmarkRunner:
    def __init__(self, deployment: Deployment):
        self.deployment = deployment

    async def run(self, request: BenchmarkRequest) -> Dict[str, Any]:
        run_id = f"run_{int(time.time())}_{uuid.uuid4().hex[:8]}"
        dataset_path = Path(request.dataset_file)
        image_root = Path(request.image_root)
        examples = load_jsonl(dataset_path)[: request.num_measured_requests + request.num_warmup_requests]
        client = MultimodalOpenAIClient(
            self.deployment.base_url,
            self.deployment.api_key,
            self.deployment.model_name,
            request.timeout_seconds,
        )
        for warmup in examples[: request.num_warmup_requests]:
            await self._run_one(client, request, warmup, image_root, run_id, warmup=True)
        start = time.perf_counter()
        sem = asyncio.Semaphore(request.concurrency)
        measured = examples[request.num_warmup_requests : request.num_warmup_requests + request.num_measured_requests]

        async def guarded(example):
            async with sem:
                return await self._run_one(client, request, example, image_root, run_id, warmup=False)

        results = await asyncio.gather(*(guarded(example) for example in measured))
        elapsed = time.perf_counter() - start
        summary = self._summarize(results, elapsed, request.cost_per_gpu_hour_usd)
        return {
            "run_id": run_id,
            "config": request.model_dump(),
            "deployment": self.deployment.model_dump(),
            "summary": summary,
            "results": results,
            "limitations": [
                "Synthetic demo images validate engineering flow only.",
                "Keyword coverage is not scientific correctness.",
                "Remote API latency includes network overhead.",
            ],
        }

    async def _run_one(self, client, request, example, image_root: Path, run_id: str, warmup: bool) -> Dict[str, Any]:
        images = []
        if request.input_mode != "text_only":
            images = [str(image_root / path) for path in example.image_paths[: request.number_of_images]]
        started = time.time()
        try:
            response = await client.chat(
                example.question,
                images,
                image_resolution=request.image_resolution,
                max_tokens=request.max_output_tokens,
                temperature=request.temperature,
            )
            evaluation = evaluate_response(example.task_type, response["model_response"], example.expected_keywords)
            ended = time.time()
            return {
                "request_id": uuid.uuid4().hex,
                "run_id": run_id,
                "warmup": warmup,
                "backend_type": self.deployment.backend_type,
                "model_name": self.deployment.model_name,
                "deployment_id": self.deployment.deployment_id,
                "input_mode": request.input_mode,
                "task_type": example.task_type,
                "modality": example.modality,
                "number_of_images": len(images),
                "image_resolution": request.image_resolution,
                "image_total_pixels": response.get("image_total_pixels", 0),
                "prompt_tokens": response.get("usage", {}).get("prompt_tokens"),
                "completion_tokens": response.get("usage", {}).get("completion_tokens"),
                "total_tokens": response.get("usage", {}).get("total_tokens"),
                "start_time": started,
                "end_time": ended,
                "end_to_end_latency_ms": response["latency_ms"],
                "time_to_first_token_ms": None,
                "time_per_output_token_ms": None,
                "output_tokens_per_second": None,
                "success": True,
                "error_message": "",
                "model_response": response["model_response"] if request.save_model_responses else "",
                "reference_answer": example.reference_answer,
                "expected_keywords": example.expected_keywords,
                **evaluation,
            }
        except Exception as exc:
            ended = time.time()
            return {
                "request_id": uuid.uuid4().hex,
                "run_id": run_id,
                "warmup": warmup,
                "backend_type": self.deployment.backend_type,
                "model_name": self.deployment.model_name,
                "deployment_id": self.deployment.deployment_id,
                "input_mode": request.input_mode,
                "task_type": example.task_type,
                "modality": example.modality,
                "number_of_images": len(images),
                "image_resolution": request.image_resolution,
                "image_total_pixels": 0,
                "start_time": started,
                "end_time": ended,
                "end_to_end_latency_ms": (ended - started) * 1000,
                "success": False,
                "error_message": str(exc),
                "model_response": "",
                "reference_answer": example.reference_answer,
                "expected_keywords": example.expected_keywords,
                "keyword_coverage_score": 0.0,
                "optional_judge_score": None,
                "quality_notes": "Request failed.",
            }

    def _summarize(self, results: List[Dict[str, Any]], elapsed: float, gpu_hourly_usd: float) -> Dict[str, Any]:
        latencies = [r["end_to_end_latency_ms"] for r in results if r.get("success")]
        output_tokens = sum((r.get("completion_tokens") or 0) for r in results)
        costs = estimate_cost(elapsed, len(results), output_tokens, gpu_hourly_usd)
        return {
            "total_requests": len(results),
            "successful_requests": sum(1 for r in results if r.get("success")),
            "failed_requests": sum(1 for r in results if not r.get("success")),
            "mean_latency_ms": round(statistics.mean(latencies), 2) if latencies else 0,
            "median_latency_ms": round(statistics.median(latencies), 2) if latencies else 0,
            "p50_latency_ms": round(percentile(latencies, 50), 2),
            "p90_latency_ms": round(percentile(latencies, 90), 2),
            "p95_latency_ms": round(percentile(latencies, 95), 2),
            "p99_latency_ms": round(percentile(latencies, 99), 2),
            "requests_per_second": round(len(results) / elapsed, 4) if elapsed else 0,
            "mean_keyword_coverage_score": round(statistics.mean([r.get("keyword_coverage_score", 0) for r in results]), 4) if results else 0,
            "peak_gpu_memory_mb": None,
            "average_gpu_utilization": None,
            **costs,
        }

