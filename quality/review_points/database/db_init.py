"""Script to initialize the database for the review points application."""

from sqlalchemy import create_engine
from quality.review_points.models.base import Base
from quality.review_points import DB_URL

# Importing models to ensure they are registered with SQLAlchemy's metadata
from quality.review_points.models.review_point import ReviewPoint
from quality.review_points.models.example import Example


def init_db():
    """Initializes the database by creating all tables defined in the models."""
    engine = create_engine(DB_URL)
    Base.metadata.create_all(engine)
    print("Database initialized successfully.")


if __name__ == "__main__":
    init_db()
