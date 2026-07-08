from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile

from app.services.dataset_service import dataset_stats, load_jsonl

router = APIRouter()


@router.post("/upload")
async def upload_dataset(file: UploadFile):
    target_dir = Path("data/uploads")
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / file.filename
    content = await file.read()
    target.write_bytes(content)
    examples = load_jsonl(target)
    return {"dataset_id": target.stem, "path": str(target), "stats": dataset_stats(examples)}


@router.get("")
def list_datasets():
    demo = Path("data/demo/materials_vlm_demo.jsonl")
    datasets = []
    if demo.exists():
        examples = load_jsonl(demo)
        datasets.append({"dataset_id": "synthetic_demo", "path": str(demo), "stats": dataset_stats(examples)})
    return datasets


@router.get("/{dataset_id}")
def get_dataset(dataset_id: str):
    if dataset_id != "synthetic_demo":
        raise HTTPException(status_code=404, detail="Only synthetic_demo is registered in the MVP. Upload support is planned next.")
    path = Path("data/demo/materials_vlm_demo.jsonl")
    examples = load_jsonl(path)
    return {"dataset_id": dataset_id, "path": str(path), "stats": dataset_stats(examples)}


@router.get("/{dataset_id}/examples")
def get_examples(dataset_id: str, limit: int = 20):
    if dataset_id != "synthetic_demo":
        raise HTTPException(status_code=404, detail="Dataset not found")
    return load_jsonl(Path("data/demo/materials_vlm_demo.jsonl"))[:limit]


@router.get("/{dataset_id}/stats")
def get_stats(dataset_id: str):
    return get_dataset(dataset_id)["stats"]
