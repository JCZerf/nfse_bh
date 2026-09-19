import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from classify import classify_digit_with_score, load_templates
from segment_digits import SAMPLES_DIR, segment_image

CONFIDENCE_THRESHOLD = 0.75
OUTPUT_PATH = Path(__file__).parent / "auto_labels.json"


def auto_label() -> None:
    templates = load_templates()
    sample_paths = sorted(SAMPLES_DIR.glob("*.jpg"))

    results = {}
    low_confidence_samples = []

    for sample_path in sample_paths:
        sample_name = sample_path.stem
        crops = segment_image(sample_path)
        predicted_label = ""
        min_confidence = 1.0
        for crop in crops:
            digit_char, score = classify_digit_with_score(crop, templates)
            predicted_label += digit_char
            min_confidence = min(min_confidence, score)

        results[sample_name] = {"label": predicted_label, "confidence": round(min_confidence, 3)}
        if min_confidence < CONFIDENCE_THRESHOLD:
            low_confidence_samples.append(sample_name)

    OUTPUT_PATH.write_text(json.dumps(results, indent=2))

    print(f"Total de amostras: {len(sample_paths)}")
    print(f"Baixa confianca (< {CONFIDENCE_THRESHOLD}): {len(low_confidence_samples)}")
    print(f"Resultados salvos em {OUTPUT_PATH}")


if __name__ == "__main__":
    auto_label()
