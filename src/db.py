from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session
from server.config import DatabaseConfig
from contextlib import contextmanager
from typing import Generator

engine = create_engine(
    DatabaseConfig.url, pool_recycle=DatabaseConfig.connection_pool_recycle
)
SessionLocal = sessionmaker(bind=engine)

@contextmanager
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()