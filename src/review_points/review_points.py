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

        py_review_points = review_point_repo.get_review_points_by_topic(REVIEW_POINTS_TOPIC.PYTHON)
        for review_point in py_review_points:
            print(review_point.review_point_name, review_point.id, review_point.review_point_importance, review_point.topic)

        # review_point = ReviewPoint(
        #     review_point_name="Import Check",
        #     review_point_importance=2,
        #     topic=REVIEW_POINTS_TOPIC.PYTHON,
        # )
        #
        # _ = review_point_repo.create_review_point_with_object(review_point)

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
