from src.review_points.repositories.example_repo import ExampleRepo

class ExampleService:
    def __init__(self, repository: ExampleRepo):
        self.repository: ExampleRepo = repository

    def get_example_data(self, example_id: int):
        return self.repository.get_example_by_id(example_id)
