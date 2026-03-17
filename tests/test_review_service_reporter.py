"""Tests for ReporterService."""

from quality.review.services.reporter import ReporterService
import tempfile


def test_add_to_report():
    """Test adding content to the report."""
    reporter = ReporterService()
    reporter.add_to_report("Test content")
    assert reporter.report == "Test content\n\n"


def test_produce_report_from_formatted_reviews():
    """Test producing a report from formatted reviews."""
    reporter = ReporterService()
    reviews = [
        {"path": "test1.py", "line": "5", "body": "Review 1"},
        {"path": "test2.py", "line": "10", "body": "Review 2"},
    ]
    reporter.produce_report_from_formatted_reviews(reviews)
    expected = '### File: test1.py\n**Line 5**: \n\nReview 1\n\n\n### File: test2.py\n**Line 10**: \n\nReview 2\n\n\n'
    assert reporter.report == expected

def test_save_report_success():
    """Test saving a report to a file successfully."""
    with tempfile.TemporaryDirectory() as temp_dir:
        reporter = ReporterService()
        reporter.add_to_report("Test content")
        result = reporter.save_report(temp_dir + "/test_report.md")
        assert result is True


def test_save_report_directory():
    """Test saving a report when the provided path is a directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        reporter = ReporterService()
        reporter.add_to_report("Test content")
        result = reporter.save_report(temp_dir)
        assert result is True


def test_save_report_failure():
    """Test handling failure when saving a report."""
    reporter = ReporterService()
    reporter.add_to_report("Test content")
    result = reporter.save_report("/invalid/path/ceiozcjziejcize/report.md")
    assert result is False
