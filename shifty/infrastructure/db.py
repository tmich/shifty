from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from contextlib import contextmanager
from typing import Generator

# Configura l'engine
# engine = create_engine("sqlite:///./shifty.db", echo=True, future=True)
# create a new postgresql database
engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5431/shiftydb", echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Dipendenza FastAPI
def get_session() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
