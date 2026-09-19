from pathlib import Path

from captcha_solver.segment_digits import segment_image
from captcha_solver.solver import solve
from captcha_solver.tools.labels import SAMPLE_LABELS

SAMPLES_DIR = Path(__file__).resolve().parent.parent / "captcha_solver" / "samples"

# amostras reservadas fora do treino dos templates (ver tools/build_templates.py)
HELD_OUT_SAMPLES = sorted(SAMPLE_LABELS.keys())[40:]


def test_segment_image_returns_five_digit_crops():
    sample_name = HELD_OUT_SAMPLES[0]
    crops = segment_image(SAMPLES_DIR / f"{sample_name}.jpg")
    assert len(crops) == 5


def test_solve_matches_label_for_all_held_out_samples():
    for sample_name in HELD_OUT_SAMPLES:
        image_bytes = (SAMPLES_DIR / f"{sample_name}.jpg").read_bytes()
        result = solve(image_bytes, request_id="test")
        assert result == SAMPLE_LABELS[sample_name], f"falhou em {sample_name}"
