import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

url = os.getenv("DATABASE_URL", "sqlite:///./local.db")
for prefixo in ("postgres://", "postgresql://"):
    if url.startswith(prefixo):
        url = "postgresql+psycopg://" + url[len(prefixo):]

DATABASE_URL = url

args = {"check_same_thread": False} if url.startswith("sqlite") else {}
engine = create_engine(url, connect_args=args, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
