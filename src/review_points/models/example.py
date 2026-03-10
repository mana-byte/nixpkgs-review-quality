from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from .base import Base

class Example(Base):
    __tablename__ = 'examples'
    id = Column(Integer, primary_key=True)
    example = Column(String, nullable=False)
    review_point_id = Column(Integer, ForeignKey('review_points.id'), nullable=False)

    review_point = relationship("ReviewPoint", back_populates="examples")
