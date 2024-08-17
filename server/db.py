from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from server.config import DatabaseConfig

engine = create_engine(DatabaseConfig.url,
                       pool_recycle=DatabaseConfig.connection_pool_recycle)
SqlSession = sessionmaker(bind=engine)
