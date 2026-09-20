import os


def get_int_setting(name: str, default: int) -> int:
    value = os.environ.get(name)
    if value is None:
        return default
    try:
        parsed = int(value)
    except ValueError:
        return default
    return parsed if parsed > 0 else default


NFSE_HTTP_TIMEOUT_SECONDS = get_int_setting("NFSE_HTTP_TIMEOUT_SECONDS", 30)
