import csv
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


class ResultStore:
    def __init__(self, results_dir: Path, reports_dir: Path):
        self.results_dir = results_dir
        self.reports_dir = reports_dir
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def save_run(self, run_id: str, payload: Dict[str, Any]) -> None:
        path = self.results_dir / f"{run_id}.json"
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        rows = payload.get("results", [])
        if rows:
            self.save_csv(run_id, rows)

    def save_csv(self, run_id: str, rows: List[Dict[str, Any]]) -> None:
        path = self.results_dir / f"{run_id}.csv"
        fields = sorted({key for row in rows for key in row.keys()})
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def list_runs(self) -> List[Dict[str, Any]]:
        runs = []
        for path in sorted(self.results_dir.glob("*.json")):
            payload = json.loads(path.read_text(encoding="utf-8"))
            runs.append({"run_id": path.stem, "summary": payload.get("summary", {}), "config": payload.get("config", {})})
        return runs

    def load_run(self, run_id: str) -> Dict[str, Any]:
        return json.loads((self.results_dir / f"{run_id}.json").read_text(encoding="utf-8"))

    def save_report(self, run_id: str, markdown: str, payload: Dict[str, Any]) -> None:
        (self.reports_dir / f"{run_id}.md").write_text(markdown, encoding="utf-8")
        (self.reports_dir / f"{run_id}.report.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

