from src.review_points import REVIEW_POINTS_TOPIC
from src.review_points.repositories import example_repo
from src.review_points.repositories.review_point_repo import ReviewPointRepo
from src.review_points.repositories.example_repo import ExampleRepo
from src.review_points.database.session import get_db
from src.review_points.models.example import Example
from src.review_points.models.review_point import ReviewPoint


if __name__ == "__main__":
    # with get_db() as db:
    #     review_point_repo = ReviewPointRepo(db)
    #
    #     review_point = ReviewPoint(
    #         review_point_name="finalAttrs",
    #         review_point_importance=5,
    #         topic=REVIEW_POINTS_TOPIC.GLOBAL,
    #     )
    #
    #     _ = review_point_repo.create_review_point_with_object(review_point)
    #
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

    with get_db() as db:
        review_point_repo = ReviewPointRepo(db)
        rep = review_point_repo.get_review_points_by_topic(REVIEW_POINTS_TOPIC.GLOBAL)
        print(rep[0].review_point_name)

        example_repo = ExampleRepo(db)
        rep = example_repo.get_examples_by_review_point_id(rep[0].id)
        print(rep[0].example)
