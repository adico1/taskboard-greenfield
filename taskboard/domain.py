import re

class TaskboardError(Exception):
    pass

def validate_title(title):
    trimmed = title.strip()
    if not trimmed:
        raise TaskboardError("Title must not be blank.")
    return trimmed

SQLITE_INT64_MIN = -(2**63)
SQLITE_INT64_MAX = 2**63 - 1

def validate_id(id_str):
    try:
        id_val = int(id_str)
    except Exception:
        raise TaskboardError("ID must be an integer.")
    if id_val < 1:
        raise TaskboardError("ID must be positive.")
    if id_val < SQLITE_INT64_MIN or id_val > SQLITE_INT64_MAX:
        raise TaskboardError("ID out of range.")
    return id_val
