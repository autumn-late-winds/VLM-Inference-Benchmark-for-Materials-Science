import base64
from io import BytesIO
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image


def resize_image(path: Path, max_side: Optional[int]) -> Tuple[str, int]:
    with Image.open(path) as img:
        img = img.convert("RGB")
        if max_side and max(img.size) > max_side:
            img.thumbnail((max_side, max_side))
        pixels = img.width * img.height
        buffer = BytesIO()
        img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("ascii"), pixels


def parse_resolution(value: str) -> Optional[int]:
    if value in {"original", "", None}:
        return None
    text = str(value).lower().replace("px", "").strip()
    return int(text)

