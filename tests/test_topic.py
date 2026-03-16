from quality.review.services.topic import get_topic_by_builder_pattern
from quality.review_points import REVIEW_POINTS_TOPIC
from quality.review.services.github import GitHubService

from contextlib import contextmanager


@contextmanager
def github_service():
    service = GitHubService()
    yield service


# Test case 1: PR with Rust builder pattern
def test_get_topic_by_builder_pattern_rust():
    """Test case 1: PR with Rust builder pattern"""
    with github_service() as service:
        files, _ = service.get_pr_files(prnumber=491498)
        first_file = next(iter(files))  # Get the first file
        res = get_topic_by_builder_pattern(files[first_file])
        assert res == REVIEW_POINTS_TOPIC.RUST


# Test case 2: PR with Python builder pattern
def test_get_topic_by_builder_pattern_python():
    """Test case 2: PR with Python builder pattern"""
    with github_service() as service:
        # Test case 2.1
        files, _ = service.get_pr_files(prnumber=499242)
        first_file = next(iter(files))
        res = get_topic_by_builder_pattern(files[first_file])
        assert res == REVIEW_POINTS_TOPIC.PYTHON

        # Test case 2.2
        files, _ = service.get_pr_files(prnumber=498677)
        first_file = next(iter(files))
        res = get_topic_by_builder_pattern(files[first_file])
        assert res == REVIEW_POINTS_TOPIC.PYTHON


# Test case 3: PR with Go builder pattern
def test_get_topic_by_builder_pattern_go():
    """Test case 3: PR with Go builder pattern"""
    with github_service() as service:
        files, _ = service.get_pr_files(prnumber=423507)
        first_file = next(iter(files))
        res = get_topic_by_builder_pattern(files[first_file])
        assert res == REVIEW_POINTS_TOPIC.GO


# Test case 4: PR with npm builder pattern
def test_get_topic_by_builder_pattern_npm():
    """Test case 4: PR with npm builder pattern"""
    with github_service() as service:
        files, _ = service.get_pr_files(prnumber=332859)
        first_file = next(iter(files))
        res = get_topic_by_builder_pattern(files[first_file])
        assert res == REVIEW_POINTS_TOPIC.JAVASCRIPT


# Test case 5: PR with unsupported builder pattern
def test_unsupported_builder():
    """Test case 5: PR with unsupported builder pattern"""
    with github_service() as service:
        files, _ = service.get_pr_files(prnumber=498549)
        first_file = next(iter(files))
        res = get_topic_by_builder_pattern(files[first_file])
        assert res is None
