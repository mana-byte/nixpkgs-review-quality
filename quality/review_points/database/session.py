from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from quality.review_points import DB_URL


@contextmanager
def get_db(expire_on_commit: bool = True):
    engine = create_engine(DB_URL)
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        expire_on_commit=expire_on_commit,
        bind=engine,
    )
    db = SessionLocal()
    try:
        yield db
    finally:
        db.commit()
        db.close()
