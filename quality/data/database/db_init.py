"""Script to initialize the database for the review points application."""

from sqlalchemy import create_engine
from quality.data.models.base import Base
from quality.data import DB_URL

# Importing models to ensure they are registered with SQLAlchemy's metadata
from quality.data.models.review_point import ReviewPoint
from quality.data.models.example import Example


def init_db():
    """Initializes the database by creating all tables defined in the models."""
    engine = create_engine(DB_URL)
    Base.metadata.create_all(engine)
    print("Database initialized successfully.")


if __name__ == "__main__":
    init_db()
