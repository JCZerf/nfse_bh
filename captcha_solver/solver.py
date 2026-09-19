import logging

from .classify import classify_digit, load_templates
from .segment_digits import segment_image_bytes

logger = logging.getLogger(__name__)

_templates = None


def _get_templates():
    global _templates
    if _templates is None:
        _templates = load_templates()
    return _templates


def solve(image_bytes: bytes, request_id: str) -> str:
    crops = segment_image_bytes(image_bytes)
    templates = _get_templates()
    result = "".join(classify_digit(crop, templates) for crop in crops)
    logger.info("[%s] captcha resolvido: %s", request_id, result)
    return result
