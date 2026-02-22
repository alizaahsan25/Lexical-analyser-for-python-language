import re
_ID_RE = re.compile(r'^[^\W\d]\w*$', re.UNICODE)


def is_ID(token, line, col):
    """Return 'ID' if token is a valid Python identifier, else None."""
    if not token:
        return None
    if token[0] in ('"', "'"):
        return None
    if _ID_RE.match(token):
        return 'ID'
    return None