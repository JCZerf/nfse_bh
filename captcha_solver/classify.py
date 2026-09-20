from pathlib import Path

import numpy as np

TEMPLATES_PATH = Path(__file__).parent / "templates.npz"


def load_templates() -> tuple[np.ndarray, np.ndarray]:
    data = np.load(TEMPLATES_PATH)
    crops, labels = data["crops"], data["labels"]
    matrix = crops.reshape(len(crops), -1).astype(np.float32)
    matrix -= matrix.mean(axis=1, keepdims=True)
    matrix /= np.linalg.norm(matrix, axis=1, keepdims=True)
    return matrix, labels


def classify_digit_with_score(crop: np.ndarray, templates: tuple[np.ndarray, np.ndarray]) -> tuple[str, float]:
    matrix, labels = templates
    centered = crop.astype(np.float32).flatten()
    centered -= centered.mean()
    norm = np.linalg.norm(centered)
    if norm == 0:
        return "", -1.0
    scores = matrix @ (centered / norm)
    best = int(scores.argmax())
    return str(labels[best]), float(scores[best])


def classify_digit(crop: np.ndarray, templates: tuple[np.ndarray, np.ndarray]) -> str:
    digit_char, _ = classify_digit_with_score(crop, templates)
    return digit_char
