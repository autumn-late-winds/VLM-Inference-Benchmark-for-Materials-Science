from typing import Any, Dict


def build_report(run: Dict[str, Any]) -> str:
    summary = run.get("summary", {})
    deployment = run.get("deployment", {})
    config = run.get("config", {})
    return f"""# Materials VLM Inference Benchmark Report

## Configuration
- Run: {config.get("run_name")}
- Backend: {deployment.get("backend_type")}
- Model: {deployment.get("model_name")}
- Input mode: {config.get("input_mode")}
- Resolution: {config.get("image_resolution")}
- Concurrency: {config.get("concurrency")}

## Latency And Throughput
- Mean latency: {summary.get("mean_latency_ms")} ms
- P95 latency: {summary.get("p95_latency_ms")} ms
- Requests per second: {summary.get("requests_per_second")}

## Cost Estimates
- Cost per 1k requests: ${summary.get("estimated_cost_per_1k_requests")}
- Cost per 1M output tokens: ${summary.get("estimated_cost_per_1M_output_tokens")}

## Quality
- Mean keyword coverage: {summary.get("mean_keyword_coverage_score")}
- Quality scores are approximate, synthetic-demo dependent, and not proof of scientific correctness.

## Limitations
- Synthetic demo images are for engineering validation only.
- VLM outputs may hallucinate peaks, materials, or performance values.
- Remote latency includes network overhead unless benchmark runs on the cloud server.
- vLLM and Transformers support depends on installed package versions and model compatibility.
"""

