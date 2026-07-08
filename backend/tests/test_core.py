import json
from pathlib import Path

from app.schemas.common import DatasetExample
from app.services.cost_estimator import estimate_cost
from app.services.dataset_service import dataset_stats
from app.services.image_preprocessor import parse_resolution
from app.services.multimodal_openai_client import MultimodalOpenAIClient
from app.services.quality_evaluator import keyword_coverage
from app.services.report_service import build_report
from app.services.result_store import ResultStore


def test_parse_resolution():
    assert parse_resolution("512px") == 512
    assert parse_resolution("original") is None


def test_keyword_coverage():
    assert keyword_coverage("porous nanosheet morphology", ["porous", "nanosheet", "dense"]) == 0.6667


def test_cost_estimator():
    cost = estimate_cost(3600, 1000, 1_000_000, 2.0)
    assert cost["estimated_total_cost_usd"] == 2.0
    assert cost["estimated_cost_per_1k_requests"] == 2.0


def test_request_construction_without_images():
    client = MultimodalOpenAIClient("http://localhost:8001/v1", "EMPTY", "mock")
    messages, pixels = client.build_messages("hello", [])
    assert pixels == 0
    assert messages[0]["content"][0]["type"] == "text"


def test_dataset_stats():
    item = DatasetExample(
        id="x",
        image_paths=[],
        task_type="sem_vqa",
        modality="SEM",
        question="q",
        reference_answer="a",
        expected_keywords=[],
    )
    stats = dataset_stats([item])
    assert stats["total_examples"] == 1
    assert stats["modalities"]["SEM"] == 1


def test_result_and_report(tmp_path: Path):
    store = ResultStore(tmp_path / "results", tmp_path / "reports")
    run = {"run_id": "run_test", "summary": {"mean_latency_ms": 10}, "config": {"run_name": "x"}, "deployment": {}, "results": []}
    store.save_run("run_test", run)
    store.save_report("run_test", build_report(run), run)
    assert store.load_run("run_test")["run_id"] == "run_test"
    assert (tmp_path / "reports" / "run_test.md").exists()

