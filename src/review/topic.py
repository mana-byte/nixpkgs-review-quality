import re
from src.review_points import REVIEW_POINTS_TOPIC
from src.review_points.models.review_point import ReviewPoint
from src.review_points.repositories.review_point_repo import ReviewPointRepo
from src.review_points.database.session import get_db


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


def get_review_points_by_topic(topic: REVIEW_POINTS_TOPIC) -> list[ReviewPoint]:
    with get_db() as db:
        review_point_repo = ReviewPointRepo(db)
        return review_point_repo.get_review_points_by_topic(topic)


if __name__ == "__main__":
    from src.github_module import get_pr_files

    files, patches = get_pr_files(prnumber=491498)
    keys = list(files.keys())
    res = get_topic_by_builder_pattern(files[keys[0]])
    if res:
        review_points = get_review_points_by_topic(res)
