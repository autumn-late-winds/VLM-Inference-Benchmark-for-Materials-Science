import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
IMAGE_DIR = ROOT / "data" / "demo" / "images"
DATASET = ROOT / "data" / "demo" / "materials_vlm_demo.jsonl"


def save_texture(path: Path, seed: int, title: str) -> None:
    rng = np.random.default_rng(seed)
    image = rng.normal(0.45, 0.16, (256, 256))
    for _ in range(22):
        x, y = rng.integers(0, 256, 2)
        rr = rng.integers(8, 34)
        yy, xx = np.ogrid[:256, :256]
        mask = (xx - x) ** 2 + (yy - y) ** 2 < rr**2
        image[mask] += rng.uniform(0.08, 0.25)
    plt.imsave(path, np.clip(image, 0, 1), cmap="gray")


def save_spectrum(path: Path, seed: int, title: str, xlabel: str) -> None:
    rng = np.random.default_rng(seed)
    x = np.linspace(0, 100, 500)
    y = 0.08 * rng.normal(size=x.shape)
    for center, amp, width in [(18, 1.4, 2.4), (42, 0.8, 4.5), (71, 1.0, 3.2)]:
        y += amp * np.exp(-0.5 * ((x - center) / width) ** 2)
    fig, ax = plt.subplots(figsize=(4, 3), dpi=120)
    ax.plot(x, y, color="#2563eb", linewidth=2)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Intensity")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def save_curve(path: Path, title: str, ylabel: str) -> None:
    x = np.linspace(0, 1, 200)
    y = (1 - np.exp(-6 * x)) * (1 - 0.25 * x)
    fig, ax = plt.subplots(figsize=(4, 3), dpi=120)
    ax.plot(x, y, color="#16a34a", linewidth=2)
    ax.set_title(title)
    ax.set_xlabel("Normalized axis")
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def main() -> None:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    save_texture(IMAGE_DIR / "sem_001.png", 1, "SEM")
    save_texture(IMAGE_DIR / "sem_002.png", 7, "SEM dense")
    save_texture(IMAGE_DIR / "tem_001.png", 2, "TEM")
    save_spectrum(IMAGE_DIR / "xrd_001.png", 3, "Synthetic XRD Pattern", "2 theta")
    save_spectrum(IMAGE_DIR / "raman_001.png", 4, "Synthetic Raman Spectrum", "Raman shift")
    save_spectrum(IMAGE_DIR / "ftir_001.png", 5, "Synthetic FTIR Spectrum", "Wavenumber")
    save_spectrum(IMAGE_DIR / "xps_001.png", 6, "Synthetic XPS Spectrum", "Binding energy")
    save_curve(IMAGE_DIR / "uvvis_001.png", "Synthetic UV-vis Curve", "Absorption")
    save_curve(IMAGE_DIR / "electrochem_001.png", "Synthetic Electrochemical Curve", "Capacity")
    save_curve(IMAGE_DIR / "stress_strain_001.png", "Synthetic Stress-Strain Curve", "Stress")
    examples = [
        ("sem_001", ["data/demo/images/sem_001.png"], "sem_vqa", "SEM", "What morphology is shown in this SEM image?", "The image shows a porous nanosheet-like morphology with visible aggregation.", ["porous", "nanosheet", "aggregation", "morphology"]),
        ("tem_001", ["data/demo/images/tem_001.png"], "tem_vqa", "TEM", "What structural information can be inferred from this TEM image?", "The image suggests nanoscale particles with contrast variations.", ["structure", "particle", "contrast"]),
        ("xrd_001", ["data/demo/images/xrd_001.png"], "xrd_interpretation", "XRD", "What are the main peaks in this XRD pattern?", "The plot has several peaks with varying intensity.", ["peaks", "intensity", "phase"]),
        ("raman_001", ["data/demo/images/raman_001.png"], "raman_interpretation", "Raman", "Interpret the Raman spectrum and describe peak trends.", "The Raman spectrum shows peak positions, shifts, and intensity differences.", ["spectrum", "peak", "shift", "intensity"]),
        ("ftir_001", ["data/demo/images/ftir_001.png"], "ftir_interpretation", "FTIR", "What does this FTIR spectrum show?", "The FTIR spectrum contains absorption peaks related to chemical bonds.", ["absorption", "peaks", "bonds"]),
        ("xps_001", ["data/demo/images/xps_001.png"], "xps_interpretation", "XPS", "What can be inferred from this XPS spectrum?", "The XPS spectrum shows binding energy peaks useful for surface chemistry.", ["binding energy", "peaks", "surface"]),
        ("uvvis_001", ["data/demo/images/uvvis_001.png"], "uvvis_interpretation", "UV-vis", "Describe the trend in this UV-vis plot.", "The UV-vis absorption curve changes with wavelength and shows an absorption trend.", ["absorption", "wavelength", "trend"]),
        ("electrochem_001", ["data/demo/images/electrochem_001.png"], "electrochemical_curve", "Electrochemistry", "What trend is shown in this electrochemical curve?", "The curve shows performance trend and capacity behavior.", ["trend", "capacity", "curve"]),
        ("stress_strain_001", ["data/demo/images/stress_strain_001.png"], "stress_strain_curve", "Mechanical", "Interpret this stress-strain curve.", "The curve increases to maximum stress before failure.", ["stress", "strain", "maximum"]),
        ("multi_001", ["data/demo/images/sem_001.png", "data/demo/images/sem_002.png"], "multi_image_comparison", "SEM", "Compare the morphology shown in these two SEM images.", "The first is more porous while the second has denser aggregation.", ["compare", "porous", "dense", "aggregation"]),
    ]
    with DATASET.open("w", encoding="utf-8") as f:
        for item in examples:
            row = {
                "id": item[0],
                "image_paths": item[1],
                "task_type": item[2],
                "modality": item[3],
                "question": item[4],
                "reference_answer": item[5],
                "expected_keywords": item[6],
                "difficulty": "easy",
                "source": "synthetic_demo",
            }
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Wrote {DATASET}")


if __name__ == "__main__":
    main()

