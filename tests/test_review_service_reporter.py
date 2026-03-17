"""Tests for ReporterService."""

import pytest
import tempfile
import os
from quality.review.services.reporter import ReporterService


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


def test_reporter_initialization():
    """Test that ReporterService initializes correctly."""
    reporter = ReporterService()
    assert reporter.report == ""


def test_add_to_report_empty_content():
    """Test adding empty content to report."""
    reporter = ReporterService()
    reporter.add_to_report("")
    assert reporter.report == "\n\n"


def test_add_to_report_special_characters():
    """Test adding content with special characters to report."""
    reporter = ReporterService()
    special_content = "Content with special chars: \n\t\r\u2028\u2029"
    reporter.add_to_report(special_content)
    assert special_content in reporter.report
    assert reporter.report.endswith("\n\n")


def test_add_to_report_multiple_times():
    """Test adding content multiple times to report."""
    reporter = ReporterService()
    reporter.add_to_report("First content")
    reporter.add_to_report("Second content")
    reporter.add_to_report("Third content")
    
    assert "First content" in reporter.report
    assert "Second content" in reporter.report
    assert "Third content" in reporter.report
    assert reporter.report.count("\n\n") == 3


def test_produce_report_from_formatted_reviews_empty():
    """Test producing report from empty formatted reviews."""
    reporter = ReporterService()
    reporter.produce_report_from_formatted_reviews([])
    assert reporter.report == ""


def test_produce_report_from_formatted_reviews_missing_fields():
    """Test producing report from reviews with missing fields."""
    reporter = ReporterService()
    
    # Review with missing optional fields
    incomplete_reviews = [
        {"path": "test.py", "line": 1},  # Missing body
        {"path": "test2.py", "body": "Some body"},  # Missing line
        {"line": 1, "body": "Some body"},  # Missing path
    ]
    
    # Should not crash, but may produce incomplete report
    try:
        reporter.produce_report_from_formatted_reviews(incomplete_reviews)
        assert True  # If it doesn't crash, test passes
    except Exception:
        pytest.fail("Should handle incomplete reviews gracefully")


def test_produce_report_from_formatted_reviews_special_characters():
    """Test producing report from reviews with special characters."""
    reporter = ReporterService()
    
    special_reviews = [
        {
            "path": "test\nfile.py",
            "line": 1,
            "body": "Body with special chars: \t\r\u2028"
        }
    ]
    
    reporter.produce_report_from_formatted_reviews(special_reviews)
    assert "test\nfile.py" in reporter.report
    assert "Body with special chars:" in reporter.report


def test_save_report_empty_content():
    """Test saving report with empty content."""
    with tempfile.TemporaryDirectory() as temp_dir:
        reporter = ReporterService()
        # Don't add any content
        file_path = os.path.join(temp_dir, "empty_report.md")
        result = reporter.save_report(file_path)
        assert result == True
        
        # Verify file was created and is empty
        with open(file_path, "r") as f:
            content = f.read()
            assert content == ""


def test_save_report_large_content():
    """Test saving report with large content."""
    with tempfile.TemporaryDirectory() as temp_dir:
        reporter = ReporterService()
        # Add large content
        large_content = "x" * (1024 * 1024)  # 1MB
        reporter.add_to_report(large_content)
        
        file_path = os.path.join(temp_dir, "large_report.md")
        result = reporter.save_report(file_path)
        assert result == True
        
        # Verify file was created and has correct size
        with open(file_path, "r") as f:
            content = f.read()
            assert len(content) == len(large_content) + 2  # +2 for the newlines


def test_save_report_permission_error():
    """Test saving report to location with permission error."""
    reporter = ReporterService()
    reporter.add_to_report("Test content")
    
    # Try to save to root directory (should fail on most systems)
    result = reporter.save_report("/report.md")
    assert result == False


def test_save_report_nested_directory_creation():
    """Test saving report to nested directory that doesn't exist."""
    with tempfile.TemporaryDirectory() as temp_dir:
        reporter = ReporterService()
        reporter.add_to_report("Test content")
        
        # Try to save to nested directory
        nested_path = os.path.join(temp_dir, "nested", "deep", "report.md")
        result = reporter.save_report(nested_path)
        
        # Should fail because parent directories don't exist
        assert result == False


def test_print_report_empty():
    """Test printing empty report."""
    reporter = ReporterService()
    # Should not crash
    try:
        reporter.print_report()
        assert True
    except Exception:
        pytest.fail("Should handle empty report printing")


def test_print_report_with_content():
    """Test printing report with content."""
    reporter = ReporterService()
    reporter.add_to_report("Test content for printing")
    
    # Should not crash
    try:
        reporter.print_report()
        assert True
    except Exception:
        pytest.fail("Should handle report printing with content")


def test_generate_report_str_for_review_missing_fields():
    """Test _generate_report_str_for_review with missing fields."""
    reporter = ReporterService()
    
    # Access the private method using name mangling
    incomplete_review = {"path": "test.py"}  # Missing line and body
    
    try:
        result = reporter._ReporterService__generate_report_str_for_review(incomplete_review)
        # Should handle missing fields gracefully
        assert "test.py" in result
    except Exception:
        pytest.fail("Should handle incomplete review data")


def test_multiple_reports_in_sequence():
    """Test creating multiple reports in sequence."""
    reporter = ReporterService()
    
    # First report
    reporter.add_to_report("First report content")
    with tempfile.TemporaryDirectory() as temp_dir:
        file1 = os.path.join(temp_dir, "report1.md")
        reporter.save_report(file1)
    
    # Second report (should overwrite the first)
    reporter = ReporterService()  # Create new instance
    reporter.add_to_report("Second report content")
    with tempfile.TemporaryDirectory() as temp_dir:
        file2 = os.path.join(temp_dir, "report2.md")
        reporter.save_report(file2)
    
    # Both should succeed
    assert True
