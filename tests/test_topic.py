from src.review.topic import get_topic_by_builder_pattern
from src.review_points import REVIEW_POINTS_TOPIC
from src.github_module import get_pr_files


# Test case 1: PR with Rust builder pattern
def test_get_topic_by_builder_pattern_rust():
    """Test case 1: PR with Rust builder pattern"""
    files, _ = get_pr_files(prnumber=491498)
    keys = list(files.keys())
    res = get_topic_by_builder_pattern(files[keys[0]])
    assert(res == REVIEW_POINTS_TOPIC.RUST)

def test_get_topic_by_builder_pattern_python():
    """Test case 2: PR with Python builder pattern"""
    files, _ = get_pr_files(prnumber=499242)
    keys = list(files.keys())
    res = get_topic_by_builder_pattern(files[keys[0]])
    assert(res == REVIEW_POINTS_TOPIC.PYTHON)

    files, _ = get_pr_files(prnumber=498677)
    keys = list(files.keys())
    res = get_topic_by_builder_pattern(files[keys[0]])
    assert(res == REVIEW_POINTS_TOPIC.PYTHON)
    
def test_get_topic_by_builder_pattern_go():
    """Test case 3: PR with Go builder pattern"""
    files, _ = get_pr_files(prnumber=423507)
    keys = list(files.keys())
    res = get_topic_by_builder_pattern(files[keys[0]])
    assert(res == REVIEW_POINTS_TOPIC.GO)

def test_get_topic_by_builder_pattern_npm():
    """Test case 4: PR with npm builder pattern"""
    files, _ = get_pr_files(prnumber=332859)
    keys = list(files.keys())
    res = get_topic_by_builder_pattern(files[keys[0]])
    assert(res == REVIEW_POINTS_TOPIC.JAVASCRIPT)

def test_unsupported_builder():
    """Test case 5: PR with unsupported builder pattern"""
    files, _ = get_pr_files(prnumber=498549)
    keys = list(files.keys())
    res = get_topic_by_builder_pattern(files[keys[0]])
    assert(res == None)
