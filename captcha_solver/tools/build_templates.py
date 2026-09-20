import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from auto_label import CONFIDENCE_THRESHOLD
from labels import HELD_OUT_SAMPLES, SAMPLE_LABELS, TRAIN_SAMPLES, VERIFIED_CORRECTIONS
from segment_digits import SAMPLES_DIR, segment_image

TEMPLATES_PATH = Path(__file__).resolve().parent.parent / "templates.npz"
AUTO_LABELS_PATH = Path(__file__).parent / "auto_labels.json"


def build_templates() -> None:
    auto_labels = json.loads(AUTO_LABELS_PATH.read_text())

    crops_list: list[np.ndarray] = []
    labels_list: list[int] = []
    used = 0
    skipped_low_confidence = 0

    for sample_name, info in auto_labels.items():
        if sample_name in HELD_OUT_SAMPLES:
            continue
        if sample_name in VERIFIED_CORRECTIONS:
            label = VERIFIED_CORRECTIONS[sample_name]
        elif sample_name in TRAIN_SAMPLES:
            label = SAMPLE_LABELS[sample_name]
        else:
            if info["confidence"] < CONFIDENCE_THRESHOLD:
                skipped_low_confidence += 1
                continue
            label = info["label"]
        if len(label) != 5:
            continue

        crops = segment_image(SAMPLES_DIR / f"{sample_name}.jpg")
        if len(crops) != 5:
            continue
        for digit_char, crop in zip(label, crops):
            crops_list.append(crop)
            labels_list.append(int(digit_char))
        used += 1

    np.savez_compressed(
        TEMPLATES_PATH,
        crops=np.stack(crops_list),
        labels=np.array(labels_list, dtype=np.uint8),
    )

    print(
        f"Amostras usadas para templates: {used} (excluindo {len(HELD_OUT_SAMPLES)} "
        f"reservadas para teste, {skipped_low_confidence} puladas por baixa confianca)"
    )
    counts = Counter(labels_list)
    for digit in range(10):
        print(f"digito {digit}: {counts[digit]} templates")


if __name__ == "__main__":
    build_templates()
