from sqlalchemy import Column
from sqlalchemy.orm import Session
from quality.review_points.models.review_point import ReviewPoint
from quality.review_points import REVIEW_POINTS_TOPIC
from typing import final


@final
class ReviewPointRepo:
    def __init__(self, session: Session):
        self.session = session

    def create_review_point(
        self,
        review_point_name: str,
        review_point_importance: int,
        topic: REVIEW_POINTS_TOPIC | None = None,
    ) -> ReviewPoint:
        new_review_point = ReviewPoint(
            review_point_name=review_point_name,
            review_point_importance=review_point_importance,
            topic=topic,
        )
        self.session.add(new_review_point)
        return new_review_point

    def create_review_point_with_object(
        self,
        new_review_point: ReviewPoint,
    ) -> ReviewPoint:
        self.session.add(new_review_point)
        return new_review_point

    def get_review_point_by_name(self, review_point_name: str | Column[str]) -> ReviewPoint:
        return (
            self.session.query(ReviewPoint)
            .filter(ReviewPoint.review_point_name == review_point_name)
            .first()
        )

    def get_review_point_by_object(self, review_point_name: ReviewPoint) -> ReviewPoint:
        return (
            self.session.query(ReviewPoint)
            .filter(
                ReviewPoint.review_point_name == review_point_name.review_point_name
            )
            .first()
        )

    def get_review_point_by_id(self, review_point_id: int | Column[int]) -> ReviewPoint:
        return (
            self.session.query(ReviewPoint)
            .filter(ReviewPoint.id == review_point_id)
            .first()
        )

    def get_review_points_by_topic(
        self, topic: REVIEW_POINTS_TOPIC | None
    ) -> list[ReviewPoint]:
        return self.session.query(ReviewPoint).filter(ReviewPoint.topic == topic).all()

    def get_review_points_by_importance(self, importance: int | Column[int]):
        return (
            self.session.query(ReviewPoint)
            .filter(ReviewPoint.review_point_importance == importance)
            .all()
        )

    def update_review_point(
        self,
        review_point_id: int,
        review_point_name: str,
        review_point_importance: int,
        topic: REVIEW_POINTS_TOPIC | None,
    ):
        return (
            self.session.query(ReviewPoint)
            .filter(ReviewPoint.id == review_point_id)
            .update(
                {
                    "review_point_name": review_point_name,
                    "review_point_importance": review_point_importance,
                    "topic": topic,
                }
            )
        )

    def delete_review_point(self, review_point_id: int):
        return (
            self.session.query(ReviewPoint)
            .filter(ReviewPoint.id == review_point_id)
            .delete()
        )
