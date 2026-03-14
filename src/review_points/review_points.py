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
    #         instructions="Replace rec with finalAttrs in the builder function without breaking its recursiveness. finalAttrs is a more modern and efficient way to inherit attributes from stdenv in Nix.",
    #         review_point_importance=3,
    #         topic=REVIEW_POINTS_TOPIC.GLOBAL,
    #     )
    #
    #     _ = review_point_repo.create_review_point_with_object(review_point)

    with get_db() as db:
        review_point_repo = ReviewPointRepo(db)
        example_repo = ExampleRepo(db)

        id = review_point_repo.get_review_point_by_name("finalAttrs").id

        example = Example(
            example_name="finalAttrs changelog",
            example="""
            {
                "before": "changelog = "https://github.com/holoviz/datashader/blob/${src.tag}/CHANGELOG.rst";"
                "after": "changelog = "https://github.com/holoviz/datashader/blob/${finalAttrs.src.tag}/CHANGELOG.rst";"
                "explanation": "Keep the builder function recursive by replacing rec with finalAttrs, which allows to inherit attributes from stdenv in a more modern and efficient way. In this example, we replace src.tag with finalAttrs.src.tag to maintain the recursive nature of the builder function while using finalAttrs for better performance and maintainability."
            }
            """,
            review_point_id=id,
        )
        _ = example_repo.create_example_with_object(example)
