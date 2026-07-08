from fastapi import APIRouter

from app.config import get_settings
from app.routers.deployments import registry
from app.schemas.common import InferenceRequest, InferenceResponse
from app.services.multimodal_openai_client import MultimodalOpenAIClient

router = APIRouter()


@router.post("/query", response_model=InferenceResponse)
async def query(request: InferenceRequest):
    settings = get_settings()
    settings.assert_no_local_weight_download()
    deployment = registry().get(request.deployment_id)
    client = MultimodalOpenAIClient(deployment.base_url, deployment.api_key, deployment.model_name)
    result = await client.chat(
        request.question,
        request.image_paths,
        request.image_base64,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
    )
    return InferenceResponse(
        response=result["model_response"],
        latency_ms=result["latency_ms"],
        usage=result["usage"],
        model_name=deployment.model_name,
        deployment_id=deployment.deployment_id,
    )


@router.post("/query_multi_image", response_model=InferenceResponse)
async def query_multi_image(request: InferenceRequest):
    return await query(request)

