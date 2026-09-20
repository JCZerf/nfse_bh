import json
import shutil
import sys
from pathlib import Path

import cv2

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from auto_label import CONFIDENCE_THRESHOLD
from labels import SAMPLE_LABELS
from segment_digits import SAMPLES_DIR, segment_image

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
AUTO_LABELS_PATH = Path(__file__).parent / "auto_labels.json"

HELD_OUT_TEST_SAMPLES = set(sorted(SAMPLE_LABELS.keys())[40:])
KNOWN_TRAIN_SAMPLES = set(sorted(SAMPLE_LABELS.keys())[:40])


def build_templates() -> None:
    shutil.rmtree(TEMPLATES_DIR, ignore_errors=True)
    for digit_char in "0123456789":
        (TEMPLATES_DIR / digit_char).mkdir(parents=True, exist_ok=True)

    auto_labels = json.loads(AUTO_LABELS_PATH.read_text())

    used = 0
    skipped_low_confidence = 0
    for sample_name, info in auto_labels.items():
        if sample_name in HELD_OUT_TEST_SAMPLES:
            continue
        if sample_name in KNOWN_TRAIN_SAMPLES:
            label = SAMPLE_LABELS[sample_name]
        else:
            if info["confidence"] < CONFIDENCE_THRESHOLD:
                skipped_low_confidence += 1
                continue
            label = info["label"]
        if len(label) != 5:
            continue

        sample_path = SAMPLES_DIR / f"{sample_name}.jpg"
        crops = segment_image(sample_path)
        for position, (digit_char, crop) in enumerate(zip(label, crops)):
            output_path = TEMPLATES_DIR / digit_char / f"{sample_name}_digit{position}.png"
            cv2.imwrite(str(output_path), crop)
        used += 1

    print(
        f"Amostras usadas para templates: {used} (excluindo {len(HELD_OUT_TEST_SAMPLES)} "
        f"reservadas para teste, {skipped_low_confidence} puladas por baixa confianca)"
    )
    for digit_char in "0123456789":
        count = len(list((TEMPLATES_DIR / digit_char).glob("*.png")))
        print(f"digito {digit_char}: {count} templates")


if __name__ == "__main__":
    build_templates()
