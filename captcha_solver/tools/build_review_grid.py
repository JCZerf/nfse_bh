import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from segment_digits import SAMPLES_DIR, segment_image

REVIEW_DIR = Path(__file__).parent / "review"

SCALE = 4
CELL_PADDING = 10
SAMPLES_PER_GRID = 10
DIGITS_PER_SAMPLE = 5
MAX_SAMPLES = 50


def load_samples(limit: int) -> dict[str, list[np.ndarray]]:
    samples: dict[str, list[np.ndarray]] = {}
    for sample_path in sorted(SAMPLES_DIR.glob("*.jpg"))[:limit]:
        samples[sample_path.stem] = segment_image(sample_path)
    return samples


def build_grid(samples: dict[str, list[np.ndarray]], sample_names: list[str], output_path: Path) -> None:
    digit_height, digit_width = next(iter(samples.values()))[0].shape
    cell_width = digit_width * SCALE + CELL_PADDING * 2
    cell_height = digit_height * SCALE + CELL_PADDING * 2
    label_width = 220

    grid_width = label_width + cell_width * DIGITS_PER_SAMPLE
    grid_height = cell_height * len(sample_names)

    grid = np.full((grid_height, grid_width, 3), 40, dtype=np.uint8)

    for row, sample_name in enumerate(sample_names):
        digit_crops = samples[sample_name]
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

        for col, digit_crop in enumerate(digit_crops):
            digit_bgr = cv2.cvtColor(digit_crop, cv2.COLOR_GRAY2BGR)
            resized = cv2.resize(
                digit_bgr,
                (digit_width * SCALE, digit_height * SCALE),
                interpolation=cv2.INTER_NEAREST,
            )
            x_left = label_width + col * cell_width + CELL_PADDING
            y_start = y_top + CELL_PADDING
            grid[y_start : y_start + resized.shape[0], x_left : x_left + resized.shape[1]] = resized

        cv2.line(grid, (0, y_top), (grid_width, y_top), (90, 90, 90), 1)

    cv2.imwrite(str(output_path), grid)


def main() -> None:
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    samples = load_samples(limit=MAX_SAMPLES)
    sample_names = sorted(samples.keys())

    for chunk_index in range(0, len(sample_names), SAMPLES_PER_GRID):
        chunk = sample_names[chunk_index : chunk_index + SAMPLES_PER_GRID]
        output_path = REVIEW_DIR / f"grid_{chunk_index // SAMPLES_PER_GRID:02d}.png"
        build_grid(samples, chunk, output_path)
        print(f"gerado {output_path}")


if __name__ == "__main__":
    main()
