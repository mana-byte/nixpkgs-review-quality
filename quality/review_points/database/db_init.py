from sqlalchemy import create_engine
from quality.review_points.models.base import Base
from quality.review_points import DB_URL

# Importing models to ensure they are registered with SQLAlchemy's metadata
from quality.review_points.models.review_point import ReviewPoint
from quality.review_points.models.example import Example


def init_db():
    engine = create_engine(DB_URL)
    Base.metadata.create_all(engine)
    print("Database initialized successfully.")


if __name__ == "__main__":
    init_db()
