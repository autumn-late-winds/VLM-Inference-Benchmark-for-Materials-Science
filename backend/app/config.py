from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    openai_compatible_base_url: str = "http://localhost:8001/v1"
    openai_compatible_api_key: str = "EMPTY"
    default_model: str = "Qwen/Qwen3-VL-8B-Instruct"
    local_mock_mode: bool = True
    results_dir: Path = Field(default=Path("./results"))
    reports_dir: Path = Field(default=Path("./reports"))
    data_dir: Path = Field(default=Path("./data"))
    enable_gpu_monitor: bool = False
    cloud_gpu_hourly_cost_usd: float = 1.50
    max_image_size_mb: int = 10
    backend_api_key: Optional[str] = None
    allow_local_model_download: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def assert_no_local_weight_download(self) -> None:
        if not self.allow_local_model_download:
            blocked = "Qwen3-VL local weight download is disabled. Set ALLOW_LOCAL_MODEL_DOWNLOAD=true only on a machine where downloads are intentional."
            if self.local_mock_mode is False and "localhost" in self.openai_compatible_base_url:
                raise RuntimeError(blocked)


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.results_dir.mkdir(parents=True, exist_ok=True)
    settings.reports_dir.mkdir(parents=True, exist_ok=True)
    return settings

