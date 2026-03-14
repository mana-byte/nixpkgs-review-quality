from typing import final

from src.review_points.models.review_point import ReviewPoint
from src.github_module import get_pr_files
from src.review.services.example import get_raw_examples_by_review_point
from src.review.services.review_point import get_review_point_instructions_by_name
from src.review.services.topic import (
    get_review_points_by_topic,
    get_topic_by_builder_pattern,
)
from src.review_points import REVIEW_POINTS_TOPIC


@final
class Reviewer:
    """
    A class representing a Nix code reviewer for a specific pull request.
    It fetches the PR files and evaluate the quality of the code based on predefined review points associated with the topics of the files in the PR.

    Attributes:
        prnumber (int): The number of the pull request to review.
        harshness (int): A parameter to adjust the strictness of the review (default: 5). This is directly link to review_point_importance, taking into account all review_point that have their importance < harshness.
        files (dict[str, str]): A dictionary mapping file names to their content at the head of the PR.
        patches (dict[str, str]): A dictionary mapping file names to their patch (diff) in the PR.
        topics_by_file (dict[str, REVIEW_POINTS_TOPIC]): A dictionary mapping file names to their identified topics.
        review_points_by_file (dict[str, list[str]]): A dictionary mapping file names to their associated review points based on their topics.

    """

    def __init__(self, prnumber: int, harshness: int = 5):
        self.prnumber = prnumber
        self.harshness = harshness
        self.files, self.patches = get_pr_files(prnumber=prnumber)
        self.topics_by_file = self.__generate_topics(self.files)
        self.review_points_by_file = self.__generate_review_points(self.topics_by_file)
        self.rerview_input = self.__generate_final_input(self.review_points_by_file)

    def __generate_topics(
        self, files: dict[str, str]
    ) -> dict[str, REVIEW_POINTS_TOPIC]:
        """
        Private method to generate topics for all the files in a PR. If a file doesn't match any topic, it is not included in the returned dictionary, and thus not reviewed.
        """
        topics_by_file: dict[str, REVIEW_POINTS_TOPIC] = {}
        for file_name, file_content in files.items():
            topic: REVIEW_POINTS_TOPIC | None = get_topic_by_builder_pattern(
                file_content
            )
            if topic is not None:
                topics_by_file[str(file_name)] = topic
        return topics_by_file

    def __generate_review_points(
        self, topics_by_file: dict[str, REVIEW_POINTS_TOPIC]
    ) -> dict[str, list[ReviewPoint]]:
        """
        Private method to generate review points for all the files in a PR based on their topics.
        """
        return {
            file_name: get_review_points_by_topic(topic)
            for file_name, topic in topics_by_file.items()
        }

    def __generate_final_input(
        self, review_points_by_file: dict[str, list[ReviewPoint]]
    ) -> dict[str, dict[str, dict[str, str | list[str] | None]]]:
        """
        Private method to generate the final input for the review. For each file, it creates a dictionary mapping each review point to its instruction and examples.
        """
        return {
            file_name: {
                str(review_point.review_point_name): {
                    "instructions": str(review_point.instructions),
                    "examples": get_raw_examples_by_review_point(review_point),
                }
                for review_point in review_points
            }
            for file_name, review_points in review_points_by_file.items()
        }

    def review(self):
        print(self.rerview_input)


if __name__ == "__main__":
    reviewer = Reviewer(prnumber=499242)
    reviewer.review()
