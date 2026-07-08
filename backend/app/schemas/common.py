from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Deployment(BaseModel):
    deployment_id: str
    name: str
    backend_type: str = "mock_multimodal"
    base_url: str = "http://localhost:8001/v1"
    api_key: str = "EMPTY"
    model_name: str = "Qwen/Qwen3-VL-8B-Instruct"
    notes: str = ""


class InferenceRequest(BaseModel):
    deployment_id: Optional[str] = None
    question: str
    image_paths: List[str] = Field(default_factory=list)
    image_base64: List[str] = Field(default_factory=list)
    max_tokens: int = 256
    temperature: float = 0.0


class InferenceResponse(BaseModel):
    response: str
    latency_ms: float
    usage: Dict[str, Any] = Field(default_factory=dict)
    model_name: str
    deployment_id: str


class BenchmarkRequest(BaseModel):
    run_name: str = "local_smoke"
    deployment_id: Optional[str] = None
    dataset_file: str = "data/demo/materials_vlm_demo.jsonl"
    image_root: str = "."
    input_mode: str = "single_image"
    image_resolution: str = "512"
    number_of_images: int = 1
    concurrency: int = 1
    max_output_tokens: int = 128
    num_warmup_requests: int = 1
    num_measured_requests: int = 5
    stream: bool = False
    timeout_seconds: int = 60
    temperature: float = 0.0
    save_model_responses: bool = True
    cost_per_gpu_hour_usd: float = 1.50
    notes: str = ""


class DatasetExample(BaseModel):
    id: str
    image_paths: List[str]
    task_type: str
    modality: str
    question: str
    reference_answer: str
    expected_keywords: List[str] = Field(default_factory=list)
    difficulty: str = "easy"
    source: str = "synthetic_demo"

