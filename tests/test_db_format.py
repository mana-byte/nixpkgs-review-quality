from quality.review_points.database.session import get_db
from quality.review_points.models import Example
import ast


def test_all_examples_have_before_after_and_explanation():
    """Test to ensure that all examples in the database have 'before', 'after', and 'explanation' fields populated."""
    with get_db() as db:
        all_examples = db.query(Example).all()
        for expl in all_examples:
            try:
                example_dict = ast.literal_eval(str(expl.example))
            except Exception as e:
                assert (
                    False
                ), f"From example id: {expl.id}, example_name: {expl.example_name}. Error: {e}. Example is not a valid dictionary: {expl.example}."
            assert example_dict["before"] is not None
            assert example_dict["after"] is not None
            assert example_dict["explanation"] is not None
