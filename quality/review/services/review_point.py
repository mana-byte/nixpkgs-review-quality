from quality.data.models.review_point import ReviewPoint
from quality.data.repositories.review_point_repo import ReviewPointRepo
from quality.data.database.session import get_db


def get_review_point_instructions_by_name(review_point_name: str) -> str | None:
    with get_db() as db:
        review_point_repo = ReviewPointRepo(db)
        review_point = review_point_repo.get_review_point_by_name(review_point_name)
        if review_point:
            return str(review_point.instructions)
        return
