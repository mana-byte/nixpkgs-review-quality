"""Tests for GitHubService class."""

import os
import pytest
from unittest.mock import patch, MagicMock
from quality.review.services.github import (
    GitHubService,
    REVIEW_TYPE,
)


def test_github_service_initialization():
    """Test that GitHubService initializes correctly."""
    service = GitHubService()
    assert service.env_var_name == "GITHUB_ACCESS_TOKEN"

    custom_service = GitHubService(env_var_name="CUSTOM_TOKEN")
    assert custom_service.env_var_name == "CUSTOM_TOKEN"


def test_get_github_client_missing_token():
    """Test that get_github_client raises ValueError when token is missing."""
    service = GitHubService()

    # Temporarily unset the environment variable
    old_token = os.environ.get("GITHUB_ACCESS_TOKEN")
    if "GITHUB_ACCESS_TOKEN" in os.environ:
        del os.environ["GITHUB_ACCESS_TOKEN"]

    try:
        with pytest.raises(
            ValueError, match="GITHUB_ACCESS_TOKEN environment variable is not set"
        ):
            with service._GitHubService__get_github_client():
                pass
    finally:
        # Restore the environment variable
        if old_token is not None:
            os.environ["GITHUB_ACCESS_TOKEN"] = old_token


@patch("github.Github")
def test_get_pr_files_repository_error(mock_github):
    """Test error handling when repository cannot be fetched."""
    service = GitHubService()

    # Set up mock
    mock_client = MagicMock()
    mock_github.return_value.__enter__.return_value = mock_client
    mock_client.get_repo.side_effect = Exception("Repository not found")

    # Set environment variable
    os.environ["GITHUB_ACCESS_TOKEN"] = "test_token"

    try:
        with pytest.raises(ValueError, match="Error fetching repository NixOS/nixpkgs"):
            service.get_pr_files(123)
    finally:
        if "GITHUB_ACCESS_TOKEN" in os.environ:
            del os.environ["GITHUB_ACCESS_TOKEN"]


@patch("github.Github")
def test_submit_review_empty_reviews(mock_github):
    """Test that submit_review handles empty reviews correctly."""
    service = GitHubService()

    # Set environment variable
    os.environ["GITHUB_ACCESS_TOKEN"] = "test_token"

    try:
        # Should not raise exception, just print message
        service.submit_review(123, "test body", {})

    finally:
        if "GITHUB_ACCESS_TOKEN" in os.environ:
            del os.environ["GITHUB_ACCESS_TOKEN"]


def test_review_type_enum():
    """Test that REVIEW_TYPE enum has expected values."""
    assert REVIEW_TYPE.COMMENT.value == "COMMENT"
    assert REVIEW_TYPE.APPROVE.value == "APPROVE"
    assert REVIEW_TYPE.REQUEST_CHANGES.value == "REQUEST_CHANGES"
