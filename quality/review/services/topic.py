import re
from quality.review_points import REVIEW_POINTS_TOPIC
from quality.review_points.models.review_point import ReviewPoint
from quality.review_points.repositories.review_point_repo import ReviewPointRepo
from quality.review_points.database.session import get_db


def get_topic_by_builder_pattern(
    pr_file: str, pattern: str = r"\b\w*build\w*\b"
) -> REVIEW_POINTS_TOPIC | None:
    """Extracts the builder from the nix expression using regex and returns the corresponding REVIEW_POINTS_TOPIC."""
    matches: list[str] = re.findall(pattern, pr_file, flags=re.IGNORECASE)
    for match in matches:
        topic = REVIEW_POINTS_TOPIC.builder_to_topic(match)
        if topic:
            return topic
    return


def get_review_points_by_topic(
    topic: REVIEW_POINTS_TOPIC, withGlobal: bool = True
) -> list[ReviewPoint]:
    """
    Fetches review points from the database based on the provided topic. If withGlobal is True, it also includes review points from the GLOBAL topic.
    The review points returned don't expire on commit, allowing them to be used outside the context of the database session.
    """
    with get_db(expire_on_commit=False) as db:
        review_point_repo = ReviewPointRepo(db)
        if withGlobal:
            global_review_points = review_point_repo.get_review_points_by_topic(
                REVIEW_POINTS_TOPIC.GLOBAL
            )
            topic_review_points = review_point_repo.get_review_points_by_topic(topic)
            return global_review_points + topic_review_points
    return review_point_repo.get_review_points_by_topic(topic)
