import re
from src.review_points import REVIEW_POINTS_TOPIC

def get_topic_by_builder_pattern(pr_file: str, pattern: str=r"\b\w*build\w*\b") -> REVIEW_POINTS_TOPIC | None:
    matches = re.findall(pattern, pr_file, flags=re.IGNORECASE)
    for match in matches:
        topic = REVIEW_POINTS_TOPIC.builder_to_topic(match)
        if topic:
            return topic
    return 

if __name__ == "__main__":
    from src.github_module import get_pr_files
    files, patches = get_pr_files(prnumber=491498)
    keys = list(files.keys())
    res = get_topic_by_builder_pattern(files[keys[0]])
    print(res)


