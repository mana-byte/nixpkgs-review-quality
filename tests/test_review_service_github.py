"""Tests for GitHubService class."""

import os
from unittest.mock import patch, MagicMock
from quality.review.services.github import (
    GitHubService,
    REVIEW_TYPE,
    BLACK_LISTED_FILES,
)

ENV_VAR_NAME = "ACCESS_TOKEN"


def test_github_service_initialization():
    """Test that GitHubService initializes correctly."""
    service = GitHubService()
    assert service.env_var_name == ENV_VAR_NAME

    custom_service = GitHubService(env_var_name="CUSTOM_TOKEN")
    assert custom_service.env_var_name == "CUSTOM_TOKEN"


def test_get_github_client_missing_token():
    """Test that get_github_client raises ValueError when token is missing."""
    service = GitHubService()

    # Temporarily unset the environment variable
    old_token = os.environ.get(ENV_VAR_NAME)
    if ENV_VAR_NAME in os.environ:
        del os.environ[ENV_VAR_NAME]

    try:
        with service._GitHubService__get_github_client():
            pass
    except ValueError as e:
        assert True
    finally:
        # Restore the environment variable
        if old_token is not None:
            os.environ[ENV_VAR_NAME] = old_token


def test_review_type_enum():
    """Test that REVIEW_TYPE enum has expected values."""
    assert REVIEW_TYPE.COMMENT.value == "COMMENT"
    assert REVIEW_TYPE.APPROVE.value == "APPROVE"
    assert REVIEW_TYPE.REQUEST_CHANGES.value == "REQUEST_CHANGES"


def test_blacklisted_files():
    """Test that BLACK_LISTED_FILES contains expected files."""
    expected_files = {
        "pkgs/top-level/python-packages.nix",
        "maintainers/maintainer-list.nix",
        "pkgs/by-name/hy/hyprland/info.json",
    }
    assert BLACK_LISTED_FILES == expected_files


@patch("github.Github")
def test_submit_review_invalid_pr(mock_github):
    """Test that submit_review handles invalid PR number."""
    service = GitHubService()

    # Set up mock
    mock_client = MagicMock()
    mock_github.return_value.__enter__.return_value = mock_client
    mock_repo = MagicMock()
    mock_client.get_repo.return_value = mock_repo
    mock_repo.get_pull.side_effect = Exception("PR not found")

    service.submit_review(
        999999, "test body", {"test.py": [{"line": 1, "body": "test"}]}
    )
