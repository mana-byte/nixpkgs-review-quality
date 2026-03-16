"""Example model for the review points application."""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from .base import Base


class Example(Base):
    """Represents an example associated with a review point. Each example has a name, content, and is linked to a specific review point."""

    __tablename__: str = "examples"
    id = Column(Integer, primary_key=True)
    example_name = Column(String, nullable=False, unique=True)
    example = Column(String, nullable=False)
    review_point_id = Column(Integer, ForeignKey("review_points.id"), nullable=False)

    review_point = relationship("ReviewPoint", back_populates="examples")
