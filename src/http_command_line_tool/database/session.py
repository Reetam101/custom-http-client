from sqlalchemy.orm import sessionmaker
from .connection import engine
from contextlib import contextmanager

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)

@contextmanager
def get_session():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()