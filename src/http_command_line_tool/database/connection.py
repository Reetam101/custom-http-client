from sqlalchemy import create_engine
from pathlib import Path

DB_DIR = Path.home() / ".pyreq" / "data"
DB_DIR.mkdir(parents=True, exist_ok=True)

DATBASE_URL = f"sqlite:///{DB_DIR / 'pyreq.db'}"

engine = create_engine(
    url=DATBASE_URL,
    connect_args={"check_same_thread": False}
)