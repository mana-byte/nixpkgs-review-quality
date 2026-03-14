from src.review_points import REVIEW_POINTS_TOPIC
from src.review_points.repositories import example_repo
from src.review_points.repositories.review_point_repo import ReviewPointRepo
from src.review_points.repositories.example_repo import ExampleRepo
from src.review_points.database.session import get_db
from src.review_points.models.example import Example
from src.review_points.models.review_point import ReviewPoint


if __name__ == "__main__":
    with get_db() as db:
        review_point_repo = ReviewPointRepo(db)

        review_point = ReviewPoint(
            review_point_name="Modern Build Usage",
            instructions="SUPER DIPER COOL",
            review_point_importance=1,
            topic=REVIEW_POINTS_TOPIC.PYTHON,
        )

        _ = review_point_repo.create_review_point_with_object(review_point)

    # with get_db() as db:
    #     review_point_repo = ReviewPointRepo(db)
    #     example_repo = ExampleRepo(db)
    #
    #     id = review_point_repo.get_review_point_by_name("finalAttrs").id
    #
    #     example = Example(
    #         example_name="finalAttrs example",
    #         example="finalAttrs = { inherit (stdenv) stdenv; };",
    #         review_point_id=id,
    #     )
    #     _ = example_repo.create_example_with_object(example)
