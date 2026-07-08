import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    rows = []
    for path in sorted((ROOT / "results").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        rows.append({"run_id": data["run_id"], **data.get("summary", {})})
    print(json.dumps(rows, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

