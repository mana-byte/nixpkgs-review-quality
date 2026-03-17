"""Repository for managing Example entities in the database."""

from sqlalchemy import Column
from sqlalchemy.orm import Session
from quality.data.models.example import Example
from typing import final


@final
class ExampleRepo:
    """Repository class for performing CRUD operations on Example entities. This class provides methods to create, read, update, and delete examples in the database."""

    def __init__(self, session: Session):
        self.session = session

    def create_example_with_object(self, new_example: Example) -> Example:
        self.session.add(new_example)
        return new_example

    def get_example_by_id(self, example_id: int | Column[int]) -> Example:
        return self.session.query(Example).filter(Example.id == example_id).first()

    def get_example_by_name(self, example_name: str | Column[str]) -> Example:
        return (
            self.session.query(Example)
            .filter(Example.example_name == example_name)
            .first()
        )

    def get_examples_by_review_point_id(
        self, review_point_id: int | Column[int]
    ) -> list[Example]:
        return (
            self.session.query(Example)
            .filter(Example.review_point_id == review_point_id)
            .all()
        )

    def update_example(self, example_id: int, new_example: Example):
        matching_hash = {
            "example_name": new_example.example_name,
            "example": new_example.example,
            "review_point_id": new_example.review_point_id,
        }
        return (
            self.session.query(Example)
            .filter(Example.id == example_id)
            .update(matching_hash)
        )

    def delete_example(self, example_id: int):
        return self.session.query(Example).filter(Example.id == example_id).delete()
