import json
from collections import Counter
from pathlib import Path
from typing import Dict, List

from app.schemas.common import DatasetExample


def load_jsonl(path: Path) -> List[DatasetExample]:
    examples = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            if not line.strip():
                continue
            try:
                examples.append(DatasetExample(**json.loads(line)))
            except Exception as exc:
                raise ValueError(f"Invalid JSONL at line {line_no}: {exc}") from exc
    return examples


def dataset_stats(examples: List[DatasetExample]) -> Dict[str, object]:
    return {
        "total_examples": len(examples),
        "modalities": Counter(e.modality for e in examples),
        "task_types": Counter(e.task_type for e in examples),
        "difficulties": Counter(e.difficulty for e in examples),
    }

