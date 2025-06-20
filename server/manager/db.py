from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from server.config import DatabaseConfig
from server.utils.globalize import Globalize

_engine = create_engine(
    DatabaseConfig.url, pool_recycle=DatabaseConfig.connection_pool_recycle
)
_SqlSession = sessionmaker(bind=_engine)

# the async is needed
async def use_db():
    session = _SqlSession()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

db: Session | Globalize[Session] = Globalize[Session]("db", use_db)
