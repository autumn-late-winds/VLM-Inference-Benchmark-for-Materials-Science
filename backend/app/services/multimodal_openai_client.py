import asyncio
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import httpx

from app.services.image_preprocessor import parse_resolution, resize_image


class MultimodalOpenAIClient:
    def __init__(self, base_url: str, api_key: str, model_name: str, timeout_seconds: int = 60):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model_name = model_name
        self.timeout_seconds = timeout_seconds

    def build_messages(
        self,
        question: str,
        image_paths: List[str],
        image_base64: Optional[List[str]] = None,
        image_resolution: str = "original",
    ) -> Tuple[List[Dict[str, Any]], int]:
        content: List[Dict[str, Any]] = [{"type": "text", "text": question}]
        total_pixels = 0
        max_side = parse_resolution(image_resolution)
        for path_text in image_paths:
            encoded, pixels = resize_image(Path(path_text), max_side)
            total_pixels += pixels
            content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encoded}"}})
        for encoded in image_base64 or []:
            content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encoded}"}})
        return [{"role": "user", "content": content}], total_pixels

    async def chat(
        self,
        question: str,
        image_paths: List[str],
        image_base64: Optional[List[str]] = None,
        image_resolution: str = "original",
        max_tokens: int = 256,
        temperature: float = 0.0,
    ) -> Dict[str, Any]:
        messages, total_pixels = self.build_messages(question, image_paths, image_base64, image_resolution)
        payload = {
            "model": self.model_name,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        start = time.perf_counter()
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response = await client.post(f"{self.base_url}/chat/completions", json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
        latency_ms = (time.perf_counter() - start) * 1000
        text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        return {
            "model_response": text,
            "latency_ms": latency_ms,
            "usage": data.get("usage", {}),
            "image_total_pixels": total_pixels,
            "raw": data,
        }

