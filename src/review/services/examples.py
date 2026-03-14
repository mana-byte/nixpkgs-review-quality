from src.review_points.models.review_point import ReviewPoint
from src.review_points.database.session import get_db
from src.review_points.repositories.example_repo import ExampleRepo

def get_raw_examples_by_review_point(review_point: ReviewPoint) -> list[str]:
    with get_db() as db:
        example_repo = ExampleRepo(db)
        examples = example_repo.get_examples_by_review_point(review_point)
        return [str(example.example) for example in examples]
