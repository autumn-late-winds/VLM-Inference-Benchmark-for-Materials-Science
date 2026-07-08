from typing import Dict, Optional


def estimate_cost(elapsed_seconds: float, total_requests: int, output_tokens: int, gpu_hourly_usd: float) -> Dict[str, Optional[float]]:
    elapsed_hours = elapsed_seconds / 3600 if elapsed_seconds else 0
    total_cost = elapsed_hours * gpu_hourly_usd
    return {
        "estimated_total_cost_usd": round(total_cost, 6),
        "estimated_cost_per_1k_requests": round(total_cost / max(total_requests, 1) * 1000, 6),
        "estimated_cost_per_1M_output_tokens": round(total_cost / output_tokens * 1_000_000, 6) if output_tokens else None,
        "estimated_cost_per_image_text_request": round(total_cost / max(total_requests, 1), 8),
    }

