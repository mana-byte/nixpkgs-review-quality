from quality.agents import AGENTS
from quality.review.reviewer import Reviewer
from mistralai.models.sdkerror import SDKError


def test_reviewer_checkout_pr():
    """Test that the Reviewer can checkout a PR and fetch files."""
    reviewer = Reviewer(harshness=5)
    reviewer.checkout_pr(prnumber=474854)
    assert reviewer.prnumber == 474854
    assert reviewer.files is not None
    assert reviewer.patches is not None
    assert reviewer.topics_by_file is not None
    assert isinstance(reviewer.review_inputs, dict)


def test_reviewer_checkout_pr_invalid_pr():
    """Test that the Reviewer raises an error when trying to checkout an invalid PR."""
    reviewer = Reviewer(harshness=5)
    try:
        reviewer.checkout_pr(prnumber=999999999)  # Assuming this PR does not exist
        assert False, "Expected ValueError for invalid PR number"
    except ValueError as e:
        assert True


def test_reviewer_checkout_pr_no_access_token():
    """Test that the Reviewer raises an error when the GitHub access token is not set."""
    reviewer = Reviewer(harshness=5)
    try:
        reviewer.checkout_pr(prnumber=474854, env_var_name="NON_EXISTENT_ENV_VAR")
        assert False, "Expected ValueError for missing GitHub access token"
    except ValueError as e:
        assert "NON_EXISTENT_ENV_VAR environment variable is not set" in str(e)


def test_reviewer_checkout_pr_no_valid_repo():
    """Test that the Reviewer raises an error when the repository cannot be accessed."""
    reviewer = Reviewer(harshness=5)
    try:
        reviewer.checkout_pr(
            prnumber=474854,
            owner="nonexistent_owner",
            repo="nonexistent_repo'zieounzeucnzeeiorhvzeiurhviuerhfuvvhvuerhv",
        )
        assert False, "Expected ValueError for inaccessible repository"
    except ValueError as e:
        assert "Error fetching repository" in str(e) or "PR not found" in str(e)


def test_review_files_no_review_inputs():
    """Test that review_files raises an error when there are no review inputs."""
    reviewer = Reviewer(harshness=5)
    try:
        reviewer.review_files(agent=AGENTS.MISTRAL, model="some_model")
        assert False, "Expected ValueError for no review inputs"
    except ValueError as e:
        assert "No files to review." in str(e)


def test_review_files_invalid_model():
    """Test that review_files raises an error when an invalid model is specified."""
    reviewer = Reviewer(harshness=5)
    reviewer.checkout_pr(prnumber=474854)
    try:
        reviewer.review_files(agent=AGENTS.MISTRAL, model="gpt-4o")
        assert False, "Expected ValueError for invalid model"
    except SDKError as e:
        assert True


def test_submit_reviews_no_reviews():
    """Test that submit_reviews raises an error when there are no reviews to submit."""
    reviewer = Reviewer(harshness=5)
    try:
        reviewer.submit_reviews()
        assert False, "Expected ValueError for no reviews to submit"
    except ValueError as e:
        assert "No reviews to submit." in str(e)


def test_reviewer_review_files_and_submit_reviews():
    """Test that the Reviewer can review files and submit reviews."""
    reviewer = Reviewer(harshness=5)
    reviewer.checkout_pr(prnumber=1, owner="mana-byte", repo="nixpkgs")
    reviewer.review_files(agent=AGENTS.MISTRAL, model="devstral-latest")
    assert reviewer.reviews is not None
    assert isinstance(reviewer.reviews, dict)
    try:
        reviewer.submit_reviews(additional_review_message="Test review message")
    except ValueError as e:
        assert False, f"Unexpected error when submitting reviews: {str(e)}"
