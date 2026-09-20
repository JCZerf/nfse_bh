import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from classify import classify_digit_with_score, load_templates
from labels import HELD_OUT_SAMPLES, SAMPLE_LABELS, TRAIN_SAMPLES
from segment_digits import SAMPLES_DIR, segment_image


def build_round1_templates() -> tuple[np.ndarray, np.ndarray]:
    crops_list: list[np.ndarray] = []
    labels_list: list[int] = []
    for sample_name in sorted(TRAIN_SAMPLES):
        label = SAMPLE_LABELS[sample_name]
        crops = segment_image(SAMPLES_DIR / f"{sample_name}.jpg")
        for digit_char, crop in zip(label, crops):
            crops_list.append(crop)
            labels_list.append(int(digit_char))

    crops = np.stack(crops_list)
    matrix = crops.reshape(len(crops), -1).astype(np.float32)
    matrix -= matrix.mean(axis=1, keepdims=True)
    matrix /= np.linalg.norm(matrix, axis=1, keepdims=True)
    return matrix, np.array(labels_list, dtype=np.uint8)


def main() -> None:
    round1_templates = build_round1_templates()
    banco_templates = load_templates()

    sample_names = sorted(
        p.stem for p in SAMPLES_DIR.glob("*.jpg") if p.stem not in HELD_OUT_SAMPLES and p.stem not in TRAIN_SAMPLES
    )

    disagreements = []
    per_sample = {}
    for sample_name in sample_names:
        crops = segment_image(SAMPLES_DIR / f"{sample_name}.jpg")
        if len(crops) != 5:
            continue
        banco_label = ""
        round1_label = ""
        positions = []
        for position, crop in enumerate(crops):
            round1_digit, round1_score = classify_digit_with_score(crop, round1_templates)
            banco_digit, _ = classify_digit_with_score(crop, banco_templates)
            banco_label += banco_digit
            round1_label += round1_digit
            if round1_digit != banco_digit:
                disagreements.append(
                    {
                        "sample": sample_name,
                        "position": position,
                        "banco": banco_digit,
                        "round1": round1_digit,
                        "round1_score": round(round1_score, 3),
                    }
                )
                positions.append(position)
        if positions:
            per_sample[sample_name] = {
                "banco_label": banco_label,
                "round1_label": round1_label,
                "disagreement_positions": positions,
            }

    output_path = Path(__file__).parent / "disagreements.json"
    output_path.write_text(json.dumps({"disagreements": disagreements, "per_sample": per_sample}, indent=2))

    print(f"Amostras verificadas: {len(sample_names)}")
    print(f"Discordancias round1 vs banco atual: {len(disagreements)}")
    print(f"Resultado salvo em {output_path}")


if __name__ == "__main__":
    main()
