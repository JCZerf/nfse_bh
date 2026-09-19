from pathlib import Path

import cv2
import numpy as np

TEMPLATES_DIR = Path(__file__).parent / "templates"


def _flatten_and_center(image: np.ndarray) -> np.ndarray:
    flat = image.astype(np.float64).flatten()
    return flat - flat.mean()


def _unit_normalize(vector: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm


def load_templates() -> dict[str, np.ndarray]:
    templates: dict[str, np.ndarray] = {}
    for digit_dir in sorted(TEMPLATES_DIR.iterdir()):
        if not digit_dir.is_dir():
            continue
        vectors = [
            _unit_normalize(_flatten_and_center(cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)))
            for path in digit_dir.glob("*.png")
        ]
        templates[digit_dir.name] = np.stack(vectors)
    return templates


def classify_digit_with_score(crop: np.ndarray, templates: dict[str, np.ndarray]) -> tuple[str, float]:
    centered = _flatten_and_center(crop)
    norm = np.linalg.norm(centered)
    if norm == 0:
        return "", -1.0
    unit_crop = centered / norm

    best_digit = ""
    best_score = -1.0
    for digit_char, template_matrix in templates.items():
        score = float((template_matrix @ unit_crop).max())
        if score > best_score:
            best_score = score
            best_digit = digit_char
    return best_digit, best_score


def classify_digit(crop: np.ndarray, templates: dict[str, np.ndarray]) -> str:
    digit_char, _ = classify_digit_with_score(crop, templates)
    return digit_char
