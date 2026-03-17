from quality.agents import AGENTS
from quality.review.reviewer import Reviewer
from mistralai.models.sdkerror import SDKError
import tempfile
import pytest
from unittest.mock import patch, MagicMock


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


def test_save_reviews_success():
    with tempfile.TemporaryDirectory() as temp_dir:
        reviewer = Reviewer(harshness=5)
        reviewer.checkout_pr(prnumber=1, owner="mana-byte", repo="nixpkgs")
        reviewer.review_files(agent=AGENTS.MISTRAL, model="devstral-latest")
        try:
            assert reviewer.save_reviews(temp_dir + "/test_reviews.json")
        except Exception as e:
            assert False, f"Unexpected error when saving reviews: {str(e)}"


def test_save_reviews_success_directory():
    with tempfile.TemporaryDirectory() as temp_dir:
        reviewer = Reviewer(harshness=5)
        reviewer.checkout_pr(prnumber=1, owner="mana-byte", repo="nixpkgs")
        reviewer.review_files(agent=AGENTS.MISTRAL, model="devstral-latest")
        try:
            assert reviewer.save_reviews(temp_dir)
        except Exception as e:
            assert False, f"Unexpected error when saving reviews: {str(e)}"


def test_save_reviews_fail():
    with tempfile.TemporaryDirectory() as temp_dir:
        reviewer = Reviewer(harshness=5)
        reviewer.checkout_pr(prnumber=1, owner="mana-byte", repo="nixpkgs")
        reviewer.review_files(agent=AGENTS.MISTRAL, model="devstral-latest")
        try:
            assert (
                reviewer.save_reviews("/invalid/path/ceiozcjziejcize/reviews.json")
                == False
            )
        except Exception as e:
            assert False, f"Unexpected error when saving reviews: {str(e)}"


def test_reviewer_initialization():
    """Test that Reviewer initializes correctly with different harshness levels."""
    # Test valid harshness values
    for harshness in [1, 3, 5, 7, 9]:
        reviewer = Reviewer(harshness=harshness)
        assert reviewer.harshness == harshness
    
    # Test invalid harshness values
    with pytest.raises(ValueError):
        Reviewer(harshness=0)
    
    with pytest.raises(ValueError):
        Reviewer(harshness=11)
    
    with pytest.raises(ValueError):
        Reviewer(harshness=-1)


@patch("quality.review.reviewer.GitHubService")
def test_reviewer_checkout_pr_rate_limit(mock_github_service):
    """Test that Reviewer handles GitHub API rate limiting."""
    mock_service = MagicMock()
    mock_service.get_pr_files.side_effect = Exception("API rate limit exceeded")
    mock_github_service.return_value = mock_service
    
    reviewer = Reviewer(harshness=5)
    
    with pytest.raises(ValueError, match="Error fetching repository"):
        reviewer.checkout_pr(prnumber=123456)


@patch("quality.review.reviewer.GitHubService")
def test_reviewer_checkout_pr_permission_denied(mock_github_service):
    """Test that Reviewer handles permission denied errors."""
    mock_service = MagicMock()
    mock_service.get_pr_files.side_effect = Exception("Repository access denied")
    mock_github_service.return_value = mock_service
    
    reviewer = Reviewer(harshness=5)
    
    with pytest.raises(ValueError, match="Error fetching repository"):
        reviewer.checkout_pr(prnumber=123456)


@patch("quality.review.reviewer.AgentService")
def test_review_files_agent_error(mock_agent_service):
    """Test that review_files handles agent service errors."""
    mock_service = MagicMock()
    mock_service.ask_agent_for_review.side_effect = SDKError("Agent unavailable")
    mock_agent_service.return_value = mock_service
    
    reviewer = Reviewer(harshness=5)
    reviewer.checkout_pr(prnumber=1, owner="mana-byte", repo="nixpkgs")
    
    with pytest.raises(SDKError, match="Agent unavailable"):
        reviewer.review_files(agent=AGENTS.MISTRAL, model="devstral-latest")


@patch("quality.review.reviewer.AgentService")
def test_review_files_empty_review_input(mock_agent_service):
    """Test that review_files handles empty review input."""
    mock_service = MagicMock()
    mock_service.ask_agent_for_review.return_value = {"changes": []}
    mock_agent_service.return_value = mock_service
    
    reviewer = Reviewer(harshness=5)
    reviewer.checkout_pr(prnumber=1, owner="mana-byte", repo="nixpkgs")
    
    # Mock the review_inputs to be empty
    reviewer.review_inputs = {}
    
    with pytest.raises(ValueError, match="No files to review"):
        reviewer.review_files(agent=AGENTS.MISTRAL, model="devstral-latest")


@patch("quality.review.reviewer.GitHubService")
def test_reviewer_checkout_pr_large_files(mock_github_service):
    """Test that Reviewer handles very large files."""
    # Create a very large file content
    large_content = "x" * (10 * 1024 * 1024)  # 10MB file
    
    mock_service = MagicMock()
    mock_service.get_pr_files.return_value = (
        {"large_file.py": large_content},
        {"large_file.py": "large patch"}
    )
    mock_github_service.return_value = mock_service
    
    reviewer = Reviewer(harshness=5)
    
    # This should work but might be slow, so we just test it doesn't crash
    try:
        reviewer.checkout_pr(prnumber=123456)
        assert reviewer.files is not None
        assert reviewer.patches is not None
    except MemoryError:
        # If we get a memory error, that's expected for very large files
        pytest.skip("Test skipped due to memory constraints")


@patch("quality.review.reviewer.GitHubService")
def test_reviewer_checkout_pr_special_characters(mock_github_service):
    """Test that Reviewer handles files with special characters."""
    special_content = "Content with special chars: \n\t\r\x00\u2028\u2029"
    
    mock_service = MagicMock()
    mock_service.get_pr_files.return_value = (
        {"special_file.py": special_content},
        {"special_file.py": "special patch"}
    )
    mock_github_service.return_value = mock_service
    
    reviewer = Reviewer(harshness=5)
    reviewer.checkout_pr(prnumber=123456)
    
    assert reviewer.files is not None
    assert reviewer.patches is not None
    assert "special_file.py" in reviewer.files


@patch("quality.review.reviewer.GitHubService")
@patch("quality.review.reviewer.AgentService")
def test_reviewer_full_workflow_with_errors(mock_agent_service, mock_github_service):
    """Test the full review workflow with various error conditions."""
    # Setup GitHub mock
    mock_github = MagicMock()
    mock_github.get_pr_files.return_value = (
        {"test.py": "print('hello')"},
        {"test.py": "+print('hello')"}
    )
    mock_github_service.return_value = mock_github
    
    # Setup Agent mock
    mock_agent = MagicMock()
    mock_agent.ask_agent_for_review.return_value = {
        "changes": [
            {
                "line_number": 1,
                "before": "print('hello')",
                "after": "print('hello world')",
                "explanation": "Added ' world'"
            }
        ]
    }
    mock_agent_service.return_value = mock_agent
    
    reviewer = Reviewer(harshness=5)
    
    # Test full workflow
    reviewer.checkout_pr(prnumber=123456)
    reviewer.review_files(agent=AGENTS.MISTRAL, model="devstral-latest")
    
    assert reviewer.reviews is not None
    assert len(reviewer.reviews) > 0
    
    # Test saving reviews
    with tempfile.TemporaryDirectory() as temp_dir:
        result = reviewer.save_reviews(temp_dir + "/test_reviews.json")
        assert result == True


@patch("quality.review.reviewer.GitHubService")
def test_reviewer_checkout_pr_mixed_file_types(mock_github_service):
    """Test that Reviewer handles mixed file types correctly."""
    files_content = {
        "python_file.py": "print('python')",
        "nix_file.nix": "{ pkgs }: pkgs.python",
        "text_file.txt": "plain text",
        "json_file.json": '{"key": "value"}',
    }
    
    files_patches = {
        "python_file.py": "+print('python')",
        "nix_file.nix": "+{ pkgs }: pkgs.python",
        "text_file.txt": "+plain text",
        "json_file.json": '+{"key": "value"}',
    }
    
    mock_service = MagicMock()
    mock_service.get_pr_files.return_value = (files_content, files_patches)
    mock_github_service.return_value = mock_service
    
    reviewer = Reviewer(harshness=5)
    reviewer.checkout_pr(prnumber=123456)
    
    assert reviewer.files is not None
    assert reviewer.patches is not None
    assert len(reviewer.files) == 4
    assert len(reviewer.patches) == 4
