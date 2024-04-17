import os

def make_db_uri() -> str:
    """Correctly make the database URi."""
    user = os.environ.get("POSTGRES_USER", "foo")
    password = os.environ.get("POSTGRES_PASSWORD", "bar")
    host = os.environ.get("POSTGRES_HOST", "localhost")
    port = os.environ.get("POSTGRES_PORT", "8050")

    return f"postgresql://{user}:{password}@{host}:{port}/pgstream"