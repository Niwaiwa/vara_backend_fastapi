from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import get_settings

env = get_settings()

# Create Database Engine
Engine = create_engine(
    env.db_url, echo=env.debug, future=True
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=Engine
)


def get_db_connection():
    db = scoped_session(SessionLocal)
    try:
        yield db
    finally:
        db.close()