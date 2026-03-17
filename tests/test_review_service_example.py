from quality.review.services.example import get_raw_examples_by_review_point
from quality.data.models import ReviewPoint, Example
from quality.data.repositories.review_point_repo import ReviewPointRepo
from quality.data.database.session import get_db
import ast


def test_get_raw_examples_by_review_point():
    with get_db() as db:
        review_point_repo = ReviewPointRepo(db)
        review_point = review_point_repo.get_review_point_by_id(1)
        examples = get_raw_examples_by_review_point(review_point)
        assert len(examples) > 0
        test_dict = ast.literal_eval(examples[0])
        assert type(test_dict["before"]) == str
        assert type(test_dict["after"]) == str
        assert type(test_dict["explanation"]) == str


def test_get_raw_examples_by_review_point_is_none():
    false_review_point = ReviewPoint(
        id=69420,
        review_point_name="False Review Point",
        instructions="This review point does not exist in the database.",
    )
    examples = get_raw_examples_by_review_point(false_review_point)
    assert examples == []
