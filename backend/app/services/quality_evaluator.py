import re
from typing import Dict, Iterable, List


TASK_HINTS = {
    "sem": ["morphology", "porous", "particle", "nanosheet", "aggregation"],
    "tem": ["structure", "particle", "lattice", "contrast"],
    "xrd": ["peak", "pattern", "intensity", "phase"],
    "raman": ["spectrum", "peak", "shift", "intensity"],
    "ftir": ["spectrum", "absorption", "bond", "peak"],
    "xps": ["binding energy", "peak", "oxidation", "spectrum"],
    "uv": ["absorption", "wavelength", "edge", "spectrum"],
    "curve": ["trend", "maximum", "cycle", "capacity", "stress", "strain"],
    "caption": ["figure", "scientific", "modality", "sample"],
}


def keyword_coverage(response: str, expected_keywords: Iterable[str]) -> float:
    keywords = [k.lower() for k in expected_keywords if k]
    if not keywords:
        return 0.0
    text = response.lower()
    hits = sum(1 for keyword in keywords if keyword in text)
    return round(hits / len(keywords), 4)


def task_specific_notes(task_type: str, response: str) -> str:
    hints = []
    lowered = response.lower()
    for key, words in TASK_HINTS.items():
        if key in task_type.lower():
            missing = [word for word in words if word not in lowered]
            if missing:
                hints.append(f"Missing task hints: {', '.join(missing[:4])}")
            break
    return "; ".join(hints) or "Approximate keyword checks passed."


def evaluate_response(task_type: str, response: str, expected_keywords: List[str]) -> Dict[str, object]:
    return {
        "keyword_coverage_score": keyword_coverage(response, expected_keywords),
        "quality_notes": task_specific_notes(task_type, response),
        "judge_score": None,
    }

