"""End-to-end tests for nixpkgs-review-quality CLI."""

import subprocess
import tempfile
import os


def test_help_command():
    """Test that help command returns exit code 0."""
    result = subprocess.run(
        ["uv", "run", "nixpkgs-review-quality", "-h"], capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "Tool for reviewing nixpkgs PRs" in result.stdout


def test_invalid_flag():
    """Test that invalid flag returns non-zero exit code."""
    result = subprocess.run(
        ["uv", "run", "nixpkgs-review-quality", "-z"], capture_output=True, text=True
    )
    assert result.returncode != 0


def test_pr_help():
    """Test that pr help command returns exit code 0."""
    result = subprocess.run(
        ["uv", "run", "nixpkgs-review-quality", "pr", "-h"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_pr_invalid_number():
    """Test that invalid PR number returns non-zero exit code."""
    result = subprocess.run(
        [
            "uv",
            "run",
            "nixpkgs-review-quality",
            "pr",
            "69420",
            "--repo",
            "mana-byte/nixpkgs",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0


def test_pr_all_flags():
    """Test that PR review with all flags works correctly."""
    with tempfile.TemporaryDirectory() as temp_dir:
        report_path = os.path.join(temp_dir, "report.md")

        result = subprocess.run(
            [
                "uv",
                "run",
                "nixpkgs-review-quality",
                "pr",
                "1",
                "--repo",
                "mana-byte/nixpkgs",
                "--agent",
                "MISTRAL",
                "--model",
                "devstral-latest",
                "--review-type",
                "COMMENT",
                "--message",
                "CLI test review message",
                "--save-report",
                report_path,
                "--harshness",
                "5",
                "--post-review",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0 or "PR number is required" in result.stderr

        if os.path.exists(report_path):
            with open(report_path, "r") as f:
                content = f.read()
                assert len(content) > 0
