import argparse

from src.agents import AGENTS
from src.cli.review import handle_reviewer
from src.review.services.github import REVIEW_TYPE


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Tool for reviewing nixpkgs PRs using LLMs and prompt engineering."
    )

    _ = parser.add_argument(
        "--pr",
        type=int,
        help="The number of the pull request to review.",
    )

    _ = parser.add_argument(
        "--agent",
        type=AGENTS,
        choices=list(AGENTS),
        default=AGENTS.MISTRAL.value,
        help=f"The agent to use for the review. Possible values are: {[agent.value for agent in AGENTS]}.",
    )

    _ = parser.add_argument(
        "--model",
        type=str,
        default="devstral-latest",
        help="The model to use for the review. This is directly link to the agent chosen",
    )

    _ = parser.add_argument(
        "--harshness",
        type=int,
        choices=range(1, 6),
        default=5,
        help="A parameter to adjust the strictness of the review (default: 5). This is directly link to review_point_importance, taking into account all review_point that have their importance < harshness.",
    )

    _ = parser.add_argument(
        "--repo",
        type=str,
        default="NixOS/nixpkgs",
        help="format owner/repo, e.g. NixOS/nixpkgs (default: NixOS/nixpkgs)",
    )

    _ = parser.add_argument(
        "--review-type",
        type=REVIEW_TYPE,
        default=REVIEW_TYPE.COMMENT,
        choices=list(REVIEW_TYPE),
        help="The type of review to submit (default: COMMENT).",
    )

    _ = parser.add_argument(
        "--additional-review-message",
        type=str,
        default="",
        help="The additional message to include in the review body (default: '').",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    handle_reviewer(args)

if __name__ == "__main__":
    main()

