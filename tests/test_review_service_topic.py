import pytest
from quality.review.services.topic import (
    get_topic_by_builder_pattern,
    get_review_points_by_topic,
)
from quality.review_points import REVIEW_POINTS_TOPIC
from tests.test_repo_review_points import review_point


PYTHON_TEST_FILE = """
{
  lib,
  stdenv,
  python3Packages,
  fetchFromGitHub,

  # tests
  uv,
  versionCheckHook,
  writableTmpDirAsHomeHook,
}:

python3Packages.buildPythonApplication (finalAttrs: {
  pname = "mistral-vibe";
  version = "2.4.2";
  pyproject = true;

  ...
"""

RUST_TEST_FILE = """
{
  lib,
  fetchFromGitHub,
  rustPlatform,
}:
rustPlatform.buildRustPackage (finalAttrs: {
  pname = "rustfetch";
  version = "0.2.0";

  src = fetchFromGitHub {
    owner = "lemuray";
    repo = "rustfetch";
    tag = "v${finalAttrs.version}";
    hash = "sha256-iGcxDKl36kbEi+OiH4gB2+HxP37bpqAMZguIXDzq3Jw=";
  };
  cargoHash = "sha256-87wfFczmgCft4ke/RQKi54wvqFKGRJMtqhkwQgDCedg=";

  meta = {
    description = "CLI tool designed to fetch system information in the fastest and safest way possible";
    homepage = "https://github.com/lemuray/rustfetch";
    changelog = "https://github.com/lemuray/rustfetch/releases/tag/${finalAttrs.src.tag}";
    license = lib.licenses.mit;
    platforms = lib.platforms.all;
    maintainers = with lib.maintainers; [ lefaucheur0769 ];
    mainProgram = "rustfetch";
  };
})
"""

GO_TEST_FILE = """
{
  lib,
  buildGoModule,
  fetchFromGitHub,
  nix-update-script,
}:

buildGoModule (finalAttrs: {
  pname = "scripthaus";
  version = "0.5.1";

  src = fetchFromGitHub {
    owner = "scripthaus-dev";
    repo = "scripthaus";
    rev = "v${finalAttrs.version}";
    hash = "sha256-ZWOSLkqjauONa+fKkagpUgWB4k+l1mzEEiC0RAMUmo0=";
  };

  vendorHash = "sha256-GUZNPLBgqN1zBzCcPl7TB9/4/Yk4e7K6I20nVaM6ank=";

  env.CGO_ENABLED = 1;

  ldflags = [
    "-s"
    "-w"
  ];

  postInstall = ''
    mv $out/bin/cmd $out/bin/scripthaus
  '';

  passthru.updateScript = nix-update-script {
    extraArgs = [
      "--version-regex"
      "^(v[0-9.]+)$"
    ];
  };

  meta = {
    description = "Run bash, Python, and JS snippets from your Markdown files directly from the command-line";
    homepage = "https://github.com/scripthaus-dev/scripthaus";
    license = lib.licenses.mpl20;
    maintainers = with lib.maintainers; [ raspher ];
    mainProgram = "scripthaus";
  };
})
"""

NPM_TEST_FILE = """
{
  lib,
  buildNpmPackage,
  fetchFromGitHub,
  nix-update-script,
}:

buildNpmPackage rec {
  pname = "git-run";
  version = "0.5.5";

  src = fetchFromGitHub {
    owner = "mixu";
    repo = "gr";
    rev = "v${version}";
    hash = "sha256-WPnar87p0GYf6ehhVEUeZd2pTjS95Zl6NpiJuIOQ5Tc=";
  };

  npmDepsHash = "sha256-PdxKFopmuNRWkSwPDX1wcNTvRtbVScl1WsZi7sdkKMw=";

  makeCacheWritable = true;
  dontBuild = true;

  passthru.updateScript = nix-update-script { };

  meta = {
    description = "Multiple git repository management tool";
    homepage = "https://mixu.net/gr/";
    license = lib.licenses.bsd3;
    mainProgram = "gr";
    maintainers = with lib.maintainers; [ pyrox0 ];
  };
}
"""

UNSUPPORTED_TEST_FILE = """
{
  wl-clipboard,
  nix-update-script,
  nixosTests,
}:

stdenv.mkDerivation (finalAttrs: {
  pname = "nyxt";
  version = "3.12.0";
...
"""


def test_get_topic_by_builder_pattern_python():
    """Test that get_topic_by_builder_pattern correctly identifies the topic from the builder pattern."""
    topic = get_topic_by_builder_pattern(PYTHON_TEST_FILE)
    assert topic is not None
    assert topic.name == "PYTHON"


def test_get_topic_by_builder_pattern_rust():
    """Test that get_topic_by_builder_pattern correctly identifies the topic from the builder pattern."""
    topic = get_topic_by_builder_pattern(RUST_TEST_FILE)
    assert topic is not None
    assert topic.name == "RUST"


def test_get_topic_by_builder_pattern_go():
    """Test that get_topic_by_builder_pattern correctly identifies the topic from the builder pattern."""
    topic = get_topic_by_builder_pattern(GO_TEST_FILE)
    assert topic is not None
    assert topic.name == "GO"


def test_get_topic_by_builder_pattern_npm():
    """Test that get_topic_by_builder_pattern correctly identifies the topic from the builder pattern."""
    topic = get_topic_by_builder_pattern(NPM_TEST_FILE)
    assert topic is not None
    assert topic.name == "JAVASCRIPT"


def test_get_topic_by_builder_pattern_no_match():
    """Test that get_topic_by_builder_pattern returns None when no builder pattern is found."""
    topic = get_topic_by_builder_pattern(UNSUPPORTED_TEST_FILE)
    assert topic is None


def test_get_review_points_by_topic():
    """Test that get_review_points_by_topic returns a list of review points for a given topic."""
    topic = get_topic_by_builder_pattern(PYTHON_TEST_FILE)
    if topic is None:
        assert False, "Topic should not be None for the test file"
    review_points = get_review_points_by_topic(topic)
    assert isinstance(review_points, list)
    assert all(rp.topic in [topic, "Global"] for rp in review_points)

def test_get_review_points_by_topic_no_global():
    """Test that get_review_points_by_topic returns only topic-specific review points when withGlobal is False."""
    topic = get_topic_by_builder_pattern(PYTHON_TEST_FILE)
    if topic is None:
        assert False, "Topic should not be None for the test file"
    review_points = get_review_points_by_topic(topic, withGlobal=False)
    assert isinstance(review_points, list)
    assert all(rp.topic == topic for rp in review_points)


def test_get_topic_by_builder_pattern_empty_file():
    """Test that get_topic_by_builder_pattern handles empty file content."""
    topic = get_topic_by_builder_pattern("")
    assert topic is None


def test_get_topic_by_builder_pattern_whitespace_only():
    """Test that get_topic_by_builder_pattern handles whitespace-only content."""
    topic = get_topic_by_builder_pattern("   \n\t\r  ")
    assert topic is None


def test_get_topic_by_builder_pattern_unsupported_builder():
    """Test that get_topic_by_builder_pattern handles unsupported builder patterns."""
    unsupported_file = """
    {
      lib,
      stdenv,
    }:
    
    stdenv.mkDerivation {
      name = "unsupported";
      version = "1.0.0";
      src = ./.;
      meta = {
        description = "Unsupported builder pattern";
      };
    }
    """
    topic = get_topic_by_builder_pattern(unsupported_file)
    assert topic is None


def test_get_topic_by_builder_pattern_multiple_builders():
    """Test that get_topic_by_builder_pattern handles files with multiple builder patterns."""
    multi_builder_file = """
    {
      lib,
      python3Packages,
      rustPlatform,
    }:
    
    python3Packages.buildPythonApplication (finalAttrs: {
      pname = "python-app";
      version = "1.0.0";
    })
    
    rustPlatform.buildRustPackage (finalAttrs: {
      pname = "rust-lib";
      version = "1.0.0";
    })
    """
    # Should return the first matching topic (PYTHON)
    topic = get_topic_by_builder_pattern(multi_builder_file)
    assert topic is not None
    assert topic.name == "PYTHON"


def test_get_topic_by_builder_pattern_nested_expressions():
    """Test that get_topic_by_builder_pattern handles nested expressions."""
    nested_file = """
    {
      lib,
      python3Packages,
    }:
    
    let
      buildPythonApp = python3Packages.buildPythonApplication;
    in {
      myApp = buildPythonApp (finalAttrs: {
        pname = "nested-app";
        version = "1.0.0";
      });
    }
    """
    topic = get_topic_by_builder_pattern(nested_file)
    assert topic is not None
    assert topic.name == "PYTHON"


def test_get_topic_by_builder_pattern_with_comments():
    """Test that get_topic_by_builder_pattern handles files with comments."""
    commented_file = """
    {
      lib,
      # This is a comment
      python3Packages, /* multi-line
                                     comment */
      # buildPythonApplication
    }:
    
    python3Packages.buildPythonApplication (finalAttrs: {
      pname = "commented-app";
      version = "1.0.0";
    })
    """
    topic = get_topic_by_builder_pattern(commented_file)
    assert topic is not None
    assert topic.name == "PYTHON"


def test_get_topic_by_builder_pattern_case_sensitivity():
    """Test that get_topic_by_builder_pattern is case-sensitive."""
    case_file = """
    {
      lib,
      Python3Packages,
    }:
    
    Python3Packages.BuildPythonapPlicatIon (finalAttrs: {
      pname = "case-app";
      version = "1.0.0";
    })
    """
    topic = get_topic_by_builder_pattern(case_file)
    assert topic is None


def test_get_review_points_by_topic_invalid_topic():
    """Test that get_review_points_by_topic handles invalid topic."""
    # Create a mock topic that doesn't exist
    class MockTopic:
        def __init__(self):
            self.name = "NONEXISTENT"
    
    mock_topic = MockTopic()
    review_points = get_review_points_by_topic(mock_topic, withGlobal=False)
    # Should return empty list for non-existent topic
    assert isinstance(review_points, list)
    assert len(review_points) == 0


def test_get_review_points_by_topic_with_global_false():
    """Test that get_review_points_by_topic with withGlobal=False excludes global points."""
    topic = get_topic_by_builder_pattern(PYTHON_TEST_FILE)
    if topic is None:
        assert False, "Topic should not be None for the test file"
    
    review_points_with_global = get_review_points_by_topic(topic, withGlobal=True)
    review_points_without_global = get_review_points_by_topic(topic, withGlobal=False)
    
    # Should have fewer or equal points when excluding global
    assert len(review_points_without_global) <= len(review_points_with_global)
    # All points without global should be in the with global list
    review_points_with_global_id = {point.id for point in review_points_with_global}
    for point in review_points_without_global:
        assert point.id in review_points_with_global_id
