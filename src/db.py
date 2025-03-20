from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from server.config import DatabaseConfig

from werkzeug.local import LocalProxy
from flask import g

engine = create_engine(
    DatabaseConfig.url, pool_recycle=DatabaseConfig.connection_pool_recycle
)
SqlSession = sessionmaker(bind=engine)


def get_current_db():
    try:
        if "db" not in g:
            g.db = SqlSession()
        return g.db
    except RuntimeError:
        return SqlSession()


db: Session = LocalProxy(get_current_db)
