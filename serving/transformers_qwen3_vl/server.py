import os

from fastapi import FastAPI, HTTPException

app = FastAPI(title="Cloud-only Transformers Qwen3-VL Baseline")


def guard_download_permission() -> None:
    if os.getenv("ALLOW_LOCAL_MODEL_DOWNLOAD", "false").lower() != "true":
        raise HTTPException(
            status_code=403,
            detail="Transformers Qwen3-VL baseline is cloud-only. Set ALLOW_LOCAL_MODEL_DOWNLOAD=true only when intentional.",
        )


@app.get("/health")
def health():
    return {"status": "configured", "cloud_only": True, "downloads_allowed": os.getenv("ALLOW_LOCAL_MODEL_DOWNLOAD") == "true"}


@app.post("/v1/chat/completions")
def chat_completions():
    guard_download_permission()
    raise HTTPException(status_code=501, detail="Baseline stub. Implement model loading here on the cloud server only.")

