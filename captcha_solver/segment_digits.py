from pathlib import Path

import cv2
import numpy as np

SAMPLES_DIR = Path(__file__).parent / "samples"

BRIGHTNESS_THRESHOLD = 150
DIGIT_SIZE = (20, 30)
MIN_COMPONENT_AREA = 15
EXPECTED_DIGIT_COUNT = 5
DECORATION_MIN_HEIGHT = 30


def binarize(image: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised = cv2.medianBlur(gray, 3)
    _, binary = cv2.threshold(denoised, BRIGHTNESS_THRESHOLD, 255, cv2.THRESH_BINARY)
    return binary


def split_box_by_valley(
    closed: np.ndarray, box: tuple[int, int, int, int]
) -> list[tuple[int, int, int, int]]:
    x, y, width, height = box
    region = closed[y : y + height, x : x + width]
    column_sums = region.sum(axis=0)
    margin = max(1, width // 4)
    search_start, search_end = margin, width - margin
    if search_end <= search_start:
        return [box]
    split_col = search_start + int(np.argmin(column_sums[search_start:search_end]))
    left_box = (x, y, split_col, height)
    right_box = (x + split_col, y, width - split_col, height)
    return [left_box, right_box]


def merge_boxes(box_a: tuple[int, int, int, int], box_b: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    x = min(box_a[0], box_b[0])
    y = min(box_a[1], box_b[1])
    right = max(box_a[0] + box_a[2], box_b[0] + box_b[2])
    bottom = max(box_a[1] + box_a[3], box_b[1] + box_b[3])
    return (x, y, right - x, bottom - y)


def box_center_x(box: tuple[int, int, int, int]) -> float:
    x, _, width, _ = box
    return x + width / 2


def find_digit_boxes(binary: np.ndarray) -> list[tuple[int, int, int, int]]:
    closing_kernel = np.ones((3, 3), np.uint8)
    closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, closing_kernel)
    _image_height, image_width = binary.shape
    num_labels, _, stats, _ = cv2.connectedComponentsWithStats(closed, connectivity=8)
    boxes = []
    for label in range(1, num_labels):
        x, y, width, height, area = stats[label]
        if area < MIN_COMPONENT_AREA:
            continue
        is_decoration_bar = (
            x + width == image_width and y == 0 and height >= DECORATION_MIN_HEIGHT
        )
        if is_decoration_bar:
            continue
        boxes.append((x, y, width, height))
    boxes.sort(key=lambda box: box[0])

    while len(boxes) > EXPECTED_DIGIT_COUNT:
        distances = [
            box_center_x(boxes[i + 1]) - box_center_x(boxes[i]) for i in range(len(boxes) - 1)
        ]
        closest_index = min(range(len(distances)), key=lambda i: distances[i])
        merged = merge_boxes(boxes[closest_index], boxes[closest_index + 1])
        boxes[closest_index : closest_index + 2] = [merged]

    while len(boxes) < EXPECTED_DIGIT_COUNT:
        widest_index = max(range(len(boxes)), key=lambda i: boxes[i][2])
        split_result = split_box_by_valley(closed, boxes[widest_index])
        if len(split_result) == 1:
            break
        boxes[widest_index : widest_index + 1] = split_result

    return boxes


def crop_digits(image: np.ndarray, boxes: list[tuple[int, int, int, int]]) -> list[np.ndarray]:
    crops = []
    for x, y, width, height in boxes:
        crop = image[y : y + height, x : x + width]
        resized = cv2.resize(crop, DIGIT_SIZE, interpolation=cv2.INTER_AREA)
        crops.append(resized)
    return crops


def segment_array(image: np.ndarray) -> list[np.ndarray]:
    binary = binarize(image)
    boxes = find_digit_boxes(binary)
    return crop_digits(binary, boxes)


def segment_image(image_path: Path) -> list[np.ndarray]:
    image = cv2.imread(str(image_path))
    return segment_array(image)


def segment_image_bytes(image_bytes: bytes) -> list[np.ndarray]:
    buffer = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
    return segment_array(image)
