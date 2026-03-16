"""Database session management"""

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from quality.review_points import DB_URL


@contextmanager
def get_db(expire_on_commit: bool = True):
    """Context manager for database sessions. Yields a database session that can be used within a with statement. The session is committed and closed automatically when the block is exited."""
    engine = create_engine(DB_URL)
    session_local = sessionmaker(
        autocommit=False,
        autoflush=False,
        expire_on_commit=expire_on_commit,
        bind=engine,
    )
    db = session_local()
    try:
        yield db
    finally:
        db.commit()
        db.close()
