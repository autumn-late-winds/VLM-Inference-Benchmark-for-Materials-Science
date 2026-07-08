from pathlib import Path

from fastapi import APIRouter, HTTPException, Response

from app.config import get_settings

router = APIRouter()


@router.get("")
def list_reports():
    reports_dir = get_settings().reports_dir
    return [{"run_id": path.stem, "path": str(path)} for path in sorted(reports_dir.glob("*.md"))]


@router.get("/{run_id}")
def get_report(run_id: str):
    return {"markdown": get_markdown(run_id)}


@router.get("/{run_id}/markdown")
def get_markdown(run_id: str):
    path = get_settings().reports_dir / f"{run_id}.md"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    return path.read_text(encoding="utf-8")


@router.get("/{run_id}/json")
def get_json(run_id: str):
    path = get_settings().reports_dir / f"{run_id}.report.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    return Response(path.read_text(encoding="utf-8"), media_type="application/json")

