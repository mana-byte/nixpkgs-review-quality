from collections.abc import Iterator
from contextlib import contextmanager
from quality.data.models import ReviewPoint
from quality.data.repositories.review_point_repo import ReviewPointRepo
from quality.data.database.session import get_db
from quality.data import REVIEW_POINTS_TOPIC

ID = 8999

review_point = ReviewPoint(
    id=ID,
    review_point_name="Review Point 1",
    review_point_importance=5,
    topic=REVIEW_POINTS_TOPIC.PYTHON,
)


@contextmanager
def get_repo() -> Iterator[ReviewPointRepo]:
    with get_db() as db:
        yield ReviewPointRepo(db)


def test_create_review_point():
    with get_repo() as repo:
        _ = repo.create_review_point_with_object(review_point)


def test_get_review_point_by_id():
    with get_repo() as repo:
        test = repo.get_review_point_by_id(ID)
        assert test.id == ID
        assert test.review_point_name == "Review Point 1"
        assert test.review_point_importance == 5
        assert test.topic == REVIEW_POINTS_TOPIC.PYTHON


def test_get_review_point_by_id_None():
    with get_repo() as repo:
        test = repo.get_review_point_by_id(69420)
        assert test is None


def test_get_review_point_by_name():
    with get_repo() as repo:
        test = repo.get_review_point_by_name("Review Point 1")
        assert test.id == ID
        assert test.review_point_name == "Review Point 1"
        assert test.review_point_importance == 5
        assert test.topic == REVIEW_POINTS_TOPIC.PYTHON


def test_get_review_point_by_name_is_none():
    with get_repo() as repo:
        test = repo.get_review_point_by_name(
            "SUPER DUPER NONE EXISTANT REVIEWPOINT NAME"
        )
        assert test is None


def test_get_review_points_by_topic():
    with get_repo() as repo:
        test = repo.get_review_points_by_topic(REVIEW_POINTS_TOPIC.PYTHON)
        assert len(test) > 0
        assert test[0].topic == REVIEW_POINTS_TOPIC.PYTHON


def test_get_review_points_by_importance():
    with get_repo() as repo:
        test = repo.get_review_points_by_importance(5)
        assert len(test) > 0
        assert test[0].review_point_importance == 5


def test_update_review_point():
    with get_repo() as repo:
        _ = repo.update_review_point(
            ID, "Review Point 1", 4, REVIEW_POINTS_TOPIC.PYTHON
        )
        test = repo.get_review_point_by_id(ID)
        assert test.review_point_importance == 4


def test_update_review_point():
    with get_repo() as repo:
        false_id = 69420000
        _ = repo.update_review_point(
            false_id, "Review Point 1", 4, REVIEW_POINTS_TOPIC.PYTHON
        )
        # Nothing should happen
        test = repo.get_review_point_by_id(ID)
        assert test.review_point_importance == 5
        false_review_point = repo.get_review_point_by_id(false_id)
        assert false_review_point is None


def test_delete_review_point():
    with get_repo() as repo:
        _ = repo.delete_review_point(ID)
        test = repo.get_review_point_by_id(ID)
        assert test is None


def test_delete_review_point_is_none():
    with get_repo() as repo:
        false_id = 69420
        _ = repo.delete_review_point(false_id)
        test = repo.get_review_point_by_id(false_id)
        assert test is None
