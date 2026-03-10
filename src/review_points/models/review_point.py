from sqlalchemy.orm import relationship
from sqlalchemy import Column, Enum, Integer, String
from src.review_points import REVIEW_POINTS_TOPIC
from .base import Base

class ReviewPoint(Base):
    __tablename__: str = 'review_points'
    id = Column(Integer, primary_key=True)
    review_point_name = Column(String, nullable=False)
    review_point_importance = Column(Integer, nullable=True)
    topic = Column(Enum(REVIEW_POINTS_TOPIC), nullable=True)

    examples = relationship("Example", back_populates="review_point")
