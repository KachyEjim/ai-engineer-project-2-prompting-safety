import uuid

def new_session_id() -> str:
    """Generate a new UUIDv4 session ID."""
    return str(uuid.uuid4())

def format_session_banner(session_id: str) -> str:
    return f"Session ID: {session_id}"