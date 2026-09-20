import json
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from segment_digits import SAMPLES_DIR, segment_image

REVIEW_DIR = Path(__file__).parent / "review"

SCALE = 6
ORIGINAL_SCALE = 2
CELL_PADDING = 10
LABEL_WIDTH = 320


def load_disagreements() -> list[dict]:
    data = json.loads((Path(__file__).parent / "disagreements.json").read_text())
    return data["disagreements"]


def main() -> None:
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    disagreements = load_disagreements()

    crops_by_sample: dict[str, list[np.ndarray]] = {}
    originals_by_sample: dict[str, np.ndarray] = {}
    for entry in disagreements:
        sample_name = entry["sample"]
        if sample_name not in crops_by_sample:
            crops_by_sample[sample_name] = segment_image(SAMPLES_DIR / f"{sample_name}.jpg")
            originals_by_sample[sample_name] = cv2.imread(str(SAMPLES_DIR / f"{sample_name}.jpg"))

    digit_height, digit_width = next(iter(crops_by_sample.values()))[0].shape
    original_height, original_width = next(iter(originals_by_sample.values())).shape[:2]
    cell_width = digit_width * SCALE + CELL_PADDING * 2
    original_cell_width = int(original_width * ORIGINAL_SCALE) + CELL_PADDING * 2
    cell_height = max(digit_height * SCALE, int(original_height * ORIGINAL_SCALE)) + CELL_PADDING * 2

    chunk_size = 10
    for chunk_index in range(0, len(disagreements), chunk_size):
        chunk = disagreements[chunk_index : chunk_index + chunk_size]
        grid_width = LABEL_WIDTH + original_cell_width + cell_width
        grid = np.full((cell_height * len(chunk), grid_width, 3), 40, dtype=np.uint8)

        for row, entry in enumerate(chunk):
            crop = crops_by_sample[entry["sample"]][entry["position"]]
            crop_bgr = cv2.cvtColor(crop, cv2.COLOR_GRAY2BGR)
            resized = cv2.resize(
                crop_bgr, (digit_width * SCALE, digit_height * SCALE), interpolation=cv2.INTER_NEAREST
            )
            original_resized = cv2.resize(
                originals_by_sample[entry["sample"]],
                (int(original_width * ORIGINAL_SCALE), int(original_height * ORIGINAL_SCALE)),
                interpolation=cv2.INTER_NEAREST,
            )

            y_top = row * cell_height
            label = f"{chunk_index + row} {entry['sample'].replace('captcha_', '')}_p{entry['position']} banco={entry['banco']} r1={entry['round1']}"
            cv2.putText(
                grid,
                label,
                (10, y_top + cell_height // 2 + 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.42,
                (0, 255, 0),
                1,
                cv2.LINE_AA,
            )
            x_left = LABEL_WIDTH + CELL_PADDING
            y_start = y_top + CELL_PADDING
            grid[y_start : y_start + original_resized.shape[0], x_left : x_left + original_resized.shape[1]] = (
                original_resized
            )
            x_left = LABEL_WIDTH + original_cell_width + CELL_PADDING
            grid[y_start : y_start + resized.shape[0], x_left : x_left + resized.shape[1]] = resized
            cv2.line(grid, (0, y_top), (grid.shape[1], y_top), (90, 90, 90), 1)

        output_path = REVIEW_DIR / f"disagreements_{chunk_index // chunk_size:02d}.png"
        cv2.imwrite(str(output_path), grid)
        print(f"gerado {output_path}")


if __name__ == "__main__":
    main()
