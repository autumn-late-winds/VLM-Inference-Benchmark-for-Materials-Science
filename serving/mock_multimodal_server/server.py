import asyncio
import os
import time
from typing import Any, Dict, List

from fastapi import FastAPI, Header, HTTPException

app = FastAPI(title="Mock OpenAI-Compatible Multimodal Server")

MOCK_API_KEY = os.getenv("MOCK_API_KEY", "EMPTY")


def require_key(authorization: str | None) -> None:
    if MOCK_API_KEY in {"", "EMPTY"}:
        return
    if authorization != f"Bearer {MOCK_API_KEY}":
        raise HTTPException(status_code=401, detail="Invalid API key")


def extract_text(messages: List[Dict[str, Any]]) -> str:
    parts = messages[-1].get("content", []) if messages else []
    texts = [part.get("text", "") for part in parts if part.get("type") == "text"]
    return " ".join(texts)


def count_images(messages: List[Dict[str, Any]]) -> int:
    parts = messages[-1].get("content", []) if messages else []
    return sum(1 for part in parts if part.get("type") == "image_url")


def deterministic_answer(question: str, images: int) -> str:
    q = question.lower()
    if "sem" in q or "morphology" in q:
        return "The SEM-like image shows porous nanosheet morphology with particle aggregation and rough surface texture."
    if "tem" in q or "structural" in q:
        return "The TEM-like image suggests nanoscale particles with contrast variations and possible lattice-related structure."
    if "xrd" in q or "peaks" in q:
        return "The XRD pattern contains several sharp peaks with different intensity, indicating crystalline phase information."
    if "raman" in q:
        return "The Raman spectrum shows peak shifts and intensity changes that can be compared across samples."
    if "ftir" in q:
        return "The FTIR spectrum contains absorption peaks associated with chemical bonds and functional groups."
    if "xps" in q:
        return "The XPS spectrum shows binding energy peaks useful for oxidation-state and surface chemistry analysis."
    if "uv" in q or "absorption" in q:
        return "The UV-vis curve shows an absorption edge and wavelength-dependent intensity trend."
    if "stress" in q or "strain" in q:
        return "The stress-strain curve rises to a maximum stress before failure, showing mechanical trend information."
    if "compare" in q or images > 1:
        return "The images can be compared by morphology, density, aggregation, and feature scale; one appears more porous while another is denser."
    if "caption" in q:
        return "Scientific caption: Synthetic materials characterization figure showing modality-specific features and sample trends."
    return "Mock multimodal response: this local server accepted the image-text request without downloading model weights."


@app.get("/health")
def health():
    return {"status": "ok", "downloads_model_weights": False}


@app.post("/v1/chat/completions")
async def chat_completions(payload: Dict[str, Any], authorization: str | None = Header(default=None)):
    require_key(authorization)
    messages = payload.get("messages", [])
    question = extract_text(messages)
    images = count_images(messages)
    await asyncio.sleep(float(os.getenv("MOCK_LATENCY_SECONDS", "0.15")) + images * 0.04)
    answer = deterministic_answer(question, images)
    completion_tokens = max(12, len(answer.split()))
    prompt_tokens = max(8, len(question.split()) + images * 80)
    return {
        "id": f"mock-{int(time.time() * 1000)}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": payload.get("model", "mock-materials-vlm"),
        "choices": [{"index": 0, "message": {"role": "assistant", "content": answer}, "finish_reason": "stop"}],
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
        },
    }

