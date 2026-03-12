from sqlalchemy import create_engine
from src.review_points.models.base import Base
from src.review_points import DB_URL

# Importing models to ensure they are registered with SQLAlchemy's metadata
from src.review_points.models.review_point import ReviewPoint
from src.review_points.models.example import Example


def init_db():
    engine = create_engine(DB_URL)
    Base.metadata.create_all(engine)
    print("Database initialized successfully.")


if __name__ == "__main__":
    init_db()
