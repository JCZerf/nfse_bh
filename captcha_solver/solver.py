import logging
import time

from .classify import classify_digit, load_templates
from .segment_digits import segment_image_bytes

logger = logging.getLogger(__name__)

_templates = None


def _get_templates():
    global _templates
    if _templates is None:
        _templates = load_templates()
    return _templates


def solve(image_bytes: bytes, request_id: str) -> tuple[str, float]:
    templates = _get_templates()

    started_at = time.perf_counter()
    crops = segment_image_bytes(image_bytes)
    result = "".join(classify_digit(crop, templates) for crop in crops)
    duration_seconds = time.perf_counter() - started_at
    logger.info("[%s] captcha resolvido: %s", request_id, result)
    return result, duration_seconds
