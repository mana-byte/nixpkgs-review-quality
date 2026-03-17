"""ReviewPoint model definition for the quality review points system."""

from sqlalchemy.orm import relationship, validates
from sqlalchemy import CheckConstraint, Column, Enum, Integer, String
from quality.data import REVIEW_POINTS_TOPIC
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from quality.data.models.example import Example


class ReviewPoint(Base):
    """Represents a review point in the quality review points system. Each review point has a name, optional instructions, an importance level, and a topic. Review points can have multiple examples associated with them."""

    __tablename__: str = "review_points"
    id = Column(Integer, primary_key=True)
    review_point_name = Column(String, nullable=False, unique=True)
    instructions = Column(String, nullable=True, default=None)
    review_point_importance = Column(
        Integer,
        CheckConstraint(
            "review_point_importance >= 1 AND review_point_importance <= 5"
        ),
        nullable=True,
        default=5,
    )
    topic = Column(Enum(REVIEW_POINTS_TOPIC), nullable=True)

    examples = relationship("Example", back_populates="review_point")

    @validates("review_point_importance")
    def validate_importance(self, key, value):
        """Validates that the review_point_importance is between 1 and 5 if it is not None."""
        if value is not None and (value < 1 or value > 5):
            raise ValueError("review_point_importance must be between 1 and 5")
        return value
