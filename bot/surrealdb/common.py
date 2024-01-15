import uuid

# ------------------------------------------------------------------------
# ID


def generate_uuid() -> str:
    """Generate a UUID.

    Returns:
        A UUID as a string.
    """
    return str(uuid.uuid4())


# ------------------------------------------------------------------------
# Exceptions
class SurrealException(Exception):
    """Base exception for SurrealDB client library."""
