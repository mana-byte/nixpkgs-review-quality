from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from .base import Base

class ReviewPoint(Base):
    __tablename__ = 'review_points'
    id = Column(Integer, primary_key=True)
    review_point_name = Column(String, nullable=False)
    review_point_importance = Column(Integer, nullable=True)

    examples = relationship("Example", back_populates="review_point")
