from typing import Any, final

from src.agents import AGENTS
from src.review.services.agent import AgentService
from src.review_points.models.review_point import ReviewPoint
from src.review.services.github import GitHubService
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
        review_points_by_file (dict[str, list[ReviewPoint]]): A dictionary mapping file names to their associated review points based on their topics.
        review_input (dict[str, dict[str, dict[str, str | list[str] | None]]]): A dictionary mapping file names to their review points, where each review point is associated with its instructions and examples. This is the final input for the review process.

    """

    def __init__(
        self,
        harshness: int = 5,
    ):
        self.prnumber: int = 0
        self.owner: str = ""
        self.repo: str = ""
        self.harshness = harshness
        self.files = {}
        self.patches = {}
        self.topics_by_file = {}
        self.review_points_by_file = {}
        self.review_inputs = {}
        self.reviews: dict[str, list[dict[str, str | int]]] = {}

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
    ) -> dict[str, Any]:
        """
        Private method to generate the final input for the review.
        For each file, it creates a dictionary mapping each review point to its instruction and examples.
        """
        return {
            file_name: {
                "content": self.files[file_name],
                "review_points": {
                    str(review_point.review_point_name): {
                        "instructions": str(review_point.instructions),
                        "examples": get_raw_examples_by_review_point(review_point),
                    }
                    for review_point in review_points
                },
            }
            for file_name, review_points in review_points_by_file.items()
        }

    def checkout_pr(
        self,
        prnumber: int,
        owner: str = "NixOS",
        repo: str = "nixpkgs",
        env_var_name: str = "GITHUB_ACCESS_TOKEN",
    ):
        # Set PR information of the reviewer
        self.prnumber = prnumber
        self.owner = owner
        self.repo = repo

        # Fetch PR files and patches
        github_service = GitHubService(env_var_name=env_var_name)
        self.files, self.patches = github_service.get_pr_files(
            prnumber=prnumber, owner=owner, repo=repo
        )

        # Generate topics, review points and final input for the review process
        self.topics_by_file = self.__generate_topics(self.files)
        self.review_points_by_file = self.__generate_review_points(self.topics_by_file)
        self.review_inputs = self.__generate_final_input(self.review_points_by_file)

    def review_files(self, agent: AGENTS, model: str):
        if not self.review_inputs or self.review_inputs == {}:
            raise ValueError("No files to review.")
        agent_service = AgentService(agent, model)
        for file_name, review_input in self.review_inputs.items():
            print(f"Reviewing file: {file_name}")
            rep = agent_service.ask_agent_for_review(review_input)
            self.reviews[file_name] = rep["changes"]

    def submit_reviews(
        self,
        review_message: str = "",
        additional_review_message: str = "",
    ):
        if not self.reviews or self.reviews == {}:
            raise ValueError("No reviews to submit.")
        if review_message == "":
            with open("src/review/messages/default_review_message.md", "r") as f:
                review_message = f.read()
            if additional_review_message != "":
                review_message += "\n --- \n" + additional_review_message

        github_service = GitHubService()
        github_service.submit_review(
            self.prnumber,
            review_message,
            reviews=self.reviews,
            owner=self.owner,
            repo=self.repo,
        )


if __name__ == "__main__":
    reviewer = Reviewer()
    # fetch pr from personal fork
    reviewer.checkout_pr(prnumber=1, owner="mana-byte")
    reviewer.review_files(AGENTS.MISTRAL, "devstral-latest")
    reviewer.submit_reviews()
