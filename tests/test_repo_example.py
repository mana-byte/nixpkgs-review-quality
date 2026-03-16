from collections.abc import Iterator
from contextlib import contextmanager
from quality.review_points.models.example import Example
from quality.review_points.repositories.example_repo import ExampleRepo
from quality.review_points.database.session import get_db

ID = 8999

example = Example(
    id=ID, example_name="Example 1", example="Example 1", review_point_id=1
)


@contextmanager
def get_repo() -> Iterator[ExampleRepo]:
    with get_db() as db:
        yield ExampleRepo(db)


def test_create_example():
    with get_repo() as repo:
        repo.create_example_with_object(example)


def test_get_example_by_id():
    with get_repo() as repo:
        test = repo.get_example_by_id(ID)
        assert test.id == ID
        assert test.example_name == "Example 1"
        assert test.example == "Example 1"
        assert test.review_point_id == 1


def test_get_example_by_name():
    with get_repo() as repo:
        test = repo.get_example_by_name("Example 1")
        assert test.id == ID
        assert test.example_name == "Example 1"
        assert test.example == "Example 1"
        assert test.review_point_id == 1


def test_update_example():
    with get_repo() as repo:
        example_update = Example(
            example_name="Example 1", example="Example 2", review_point_id=1
        )
        repo.update_example(ID, example_update)
        test = repo.get_example_by_id(ID)
        assert test.example == "Example 2"


def test_delete_example():
    with get_repo() as repo:
        repo.delete_example(ID)
        test = repo.get_example_by_id(ID)
        assert test is None
