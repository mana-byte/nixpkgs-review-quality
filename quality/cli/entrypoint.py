import argparse

from quality.agents import AGENTS
from quality.cli.review import handle_reviewer
from quality.review.services.github import REVIEW_TYPE


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Tool for reviewing nixpkgs PRs using LLMs and prompt engineering."
    )

    _ = parser.add_argument(
        "--version",
        "-v",
        action="version",
        version="%(prog)s 1.0",
        help="Show program version",
    )

    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Available commands"
    )

    # sub command pr
    review_parser: argparse.ArgumentParser = subparsers.add_parser(
        "pr", help="Review a pull request"
    )
    _ = review_parser.add_argument(
        "pr_number",
        type=int,
        help="The number of the pull request to review (required).",
    )

    _ = review_parser.add_argument(
        "--post-review",
        action="store_true",
        help="Whether to post the review on GitHub after generating it (default: False). If not set, the review will only be printed to the console.",
    )

    _ = review_parser.add_argument(
        "--agent",
        "-a",
        type=AGENTS,
        choices=list(AGENTS),
        default=AGENTS.MISTRAL,
        help=f"The agent to use for the review. Possible values: {[agent.value for agent in AGENTS]}.",
    )
    _ = review_parser.add_argument(
        "--model",
        "-m",
        type=str,
        default="devstral-latest",
        help="The model to use for the review (default: devstral-latest).",
    )
    _ = review_parser.add_argument(
        "--harshness",
        type=int,
        choices=range(1, 6),
        default=5,
        help="Review strictness (1-5, default: 5). Only review points with importance < harshness will be considered.",
    )
    _ = review_parser.add_argument(
        "--repo",
        "-r",
        type=str,
        default="NixOS/nixpkgs",
        help="Repository in format owner/repo (default: NixOS/nixpkgs).",
    )
    _ = review_parser.add_argument(
        "--review-type",
        type=REVIEW_TYPE,
        choices=list(REVIEW_TYPE),
        default=REVIEW_TYPE.COMMENT,
        help="Type of review to submit (default: COMMENT).",
    )
    _ = review_parser.add_argument(
        "--message",
        type=str,
        default="",
        help="Additional message to include in the review body.",
    )

    return parser


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "pr":
        handle_reviewer(args)


if __name__ == "__main__":
    main()
