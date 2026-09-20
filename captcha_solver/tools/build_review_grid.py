import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from segment_digits import SAMPLES_DIR, segment_image

REVIEW_DIR = Path(__file__).parent / "review"

SCALE = 4
ORIGINAL_SCALE = 1.5
CELL_PADDING = 10
SAMPLES_PER_GRID = 10
DIGITS_PER_SAMPLE = 5


def load_samples() -> dict[str, tuple[np.ndarray, list[np.ndarray]]]:
    samples: dict[str, tuple[np.ndarray, list[np.ndarray]]] = {}
    for sample_path in sorted(SAMPLES_DIR.glob("*.jpg")):
        original = cv2.imread(str(sample_path))
        samples[sample_path.stem] = (original, segment_image(sample_path))
    return samples


def build_grid(
    samples: dict[str, tuple[np.ndarray, list[np.ndarray]]], sample_names: list[str], output_path: Path
) -> None:
    digit_height, digit_width = next(iter(samples.values()))[1][0].shape
    original_height, original_width = next(iter(samples.values()))[0].shape[:2]

    digit_cell_width = digit_width * SCALE + CELL_PADDING * 2
    original_cell_width = int(original_width * ORIGINAL_SCALE) + CELL_PADDING * 2
    cell_height = max(digit_height * SCALE, int(original_height * ORIGINAL_SCALE)) + CELL_PADDING * 2
    label_width = 160

    grid_width = label_width + original_cell_width + digit_cell_width * DIGITS_PER_SAMPLE
    grid_height = cell_height * len(sample_names)

    grid = np.full((grid_height, grid_width, 3), 40, dtype=np.uint8)

    for row, sample_name in enumerate(sample_names):
        original, digit_crops = samples[sample_name]
        y_top = row * cell_height

        cv2.putText(
            grid,
            sample_name.replace("captcha_", ""),
            (10, y_top + cell_height // 2 + 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (0, 255, 0),
            1,
            cv2.LINE_AA,
        )

        original_resized = cv2.resize(
            original,
            (int(original_width * ORIGINAL_SCALE), int(original_height * ORIGINAL_SCALE)),
            interpolation=cv2.INTER_NEAREST,
        )
        x_left = label_width + CELL_PADDING
        y_start = y_top + CELL_PADDING
        grid[y_start : y_start + original_resized.shape[0], x_left : x_left + original_resized.shape[1]] = (
            original_resized
        )

        for col, digit_crop in enumerate(digit_crops):
            digit_bgr = cv2.cvtColor(digit_crop, cv2.COLOR_GRAY2BGR)
            resized = cv2.resize(
                digit_bgr,
                (digit_width * SCALE, digit_height * SCALE),
                interpolation=cv2.INTER_NEAREST,
            )
            x_left = label_width + original_cell_width + col * digit_cell_width + CELL_PADDING
            y_start = y_top + CELL_PADDING
            grid[y_start : y_start + resized.shape[0], x_left : x_left + resized.shape[1]] = resized

        cv2.line(grid, (0, y_top), (grid_width, y_top), (90, 90, 90), 1)

    cv2.imwrite(str(output_path), grid)


def main() -> None:
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    samples = load_samples()
    sample_names = sorted(samples.keys())

    for chunk_index in range(0, len(sample_names), SAMPLES_PER_GRID):
        chunk = sample_names[chunk_index : chunk_index + SAMPLES_PER_GRID]
        output_path = REVIEW_DIR / f"grid_{chunk_index // SAMPLES_PER_GRID:03d}.png"
        build_grid(samples, chunk, output_path)
        print(f"gerado {output_path}")


if __name__ == "__main__":
    main()
