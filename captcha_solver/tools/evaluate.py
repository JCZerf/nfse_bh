import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from classify import classify_digit, load_templates
from labels import HELD_OUT_SAMPLES, SAMPLE_LABELS
from segment_digits import SAMPLES_DIR, segment_image


def evaluate() -> None:
    test_samples = sorted(HELD_OUT_SAMPLES)
    templates = load_templates()

    correct_digits = 0
    total_digits = 0
    correct_captchas = 0

    for sample_name in test_samples:
        true_label = SAMPLE_LABELS[sample_name]
        sample_path = SAMPLES_DIR / f"{sample_name}.jpg"
        crops = segment_image(sample_path)
        predicted_label = "".join(classify_digit(crop, templates) for crop in crops)

        digit_matches = sum(1 for a, b in zip(true_label, predicted_label) if a == b)
        correct_digits += digit_matches
        total_digits += len(true_label)
        if predicted_label == true_label:
            correct_captchas += 1

        status = "OK" if predicted_label == true_label else "ERRO"
        print(f"{sample_name}: real={true_label} previsto={predicted_label} [{status}]")

    print()
    print(f"Acuracia por digito: {correct_digits}/{total_digits} ({100 * correct_digits / total_digits:.1f}%)")
    print(f"Acuracia por captcha completo: {correct_captchas}/{len(test_samples)} ({100 * correct_captchas / len(test_samples):.1f}%)")


if __name__ == "__main__":
    evaluate()
