from fastapi import APIRouter

from app.config import get_settings

router = APIRouter()


@router.get("/health")
def health():
    settings = get_settings()
    return {
        "status": "ok",
        "local_mock_mode": settings.local_mock_mode,
        "default_model": settings.default_model,
        "local_model_download_allowed": settings.allow_local_model_download,
    }

