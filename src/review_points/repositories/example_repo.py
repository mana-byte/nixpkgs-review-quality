from sqlalchemy.orm import Session
from src.review_points.models.example import Example
from typing import final


@final
class ExampleRepo:
    def __init__(self, session: Session):
        self.session = session

    def create_example(self, example: str, review_point_id: int):
        new_example = Example(example=example, review_point_id=review_point_id)
        self.session.add(new_example)

    def get_example_by_id(self, example_id: int):
        return self.session.query(Example).filter(Example.id == example_id).first()

    def get_examples_by_review_point_id(self, review_point_id: int):
        return (
            self.session.query(Example)
            .filter(Example.review_point_id == review_point_id)
            .all()
        )

    def update_example(self, example_id: int, new_example: str):
        return (
            self.session.query(Example)
            .filter(Example.id == example_id)
            .update({"example": new_example})
        )

    def delete_example(self, example_id: int):
        return self.session.query(Example).filter(Example.id == example_id).delete()
