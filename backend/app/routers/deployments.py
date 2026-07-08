from fastapi import APIRouter, HTTPException

from app.config import get_settings
from app.schemas.common import Deployment
from app.services.deployments import DeploymentRegistry
from app.services.multimodal_openai_client import MultimodalOpenAIClient

router = APIRouter()


def registry() -> DeploymentRegistry:
    settings = get_settings()
    default = Deployment(
        deployment_id="local_mock",
        name="Local Mock Multimodal Server",
        backend_type="mock_multimodal",
        base_url=settings.openai_compatible_base_url,
        api_key=settings.openai_compatible_api_key,
        model_name=settings.default_model,
        notes="Local smoke testing only; no model weights are downloaded.",
    )
    return DeploymentRegistry(settings.results_dir / "deployments.json", default)


@router.get("")
def list_deployments():
    return registry().list()


@router.post("/register")
def register_deployment(deployment: Deployment):
    return registry().register(deployment)


@router.get("/{deployment_id}")
def get_deployment(deployment_id: str):
    return registry().get(deployment_id)


@router.post("/test")
async def test_deployment(deployment: Deployment):
    client = MultimodalOpenAIClient(deployment.base_url, deployment.api_key, deployment.model_name, timeout_seconds=15)
    try:
        result = await client.chat("Return a short health check for a materials VLM endpoint.", [], max_tokens=32)
        return {"ok": True, "latency_ms": result["latency_ms"], "response": result["model_response"], "usage": result["usage"]}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

