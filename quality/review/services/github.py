from contextlib import contextmanager

from github.PullRequest import PullRequest
from github.Repository import Repository
from quality.review.utils import create_suggestions_from_reviews
from enum import Enum
from typing import Any, final
from github import Github, Auth, GithubException, UnknownObjectException
import os

BLACK_LISTED_FILES = {
    "pkgs/top-level/python-packages.nix",
    "maintainers/maintainer-list.nix",
    "pkgs/by-name/hy/hyprland/info.json",
}


class REVIEW_TYPE(str, Enum):
    COMMENT = "COMMENT"
    APPROVE = "APPROVE"
    REQUEST_CHANGES = "REQUEST_CHANGES"


@final
class GitHubService:

    def __init__(self, env_var_name: str = "ACCESS_TOKEN"):
        self.env_var_name = env_var_name

    @contextmanager
    def __get_github_client(self):
        """Context manager to get a GitHub client using an access token from environment variables."""
        GITHUB_ACCESS_TOKEN = os.environ.get(self.env_var_name)
        if not GITHUB_ACCESS_TOKEN:
            raise ValueError(self.env_var_name + " environment variable is not set")
        auth = Auth.Token(GITHUB_ACCESS_TOKEN)
        with Github(auth=auth) as g:
            yield g

    def __get_pr(
        self, g: Github, prnumber: int, owner: str = "NixOS", repo: str = "nixpkgs"
    ) -> tuple[Repository, PullRequest]:
        try:
            repository = g.get_repo(f"{owner}/{repo}")
            pr = repository.get_pull(prnumber)
        except UnknownObjectException as e:
            raise ValueError(f"Error fetching repository or PR: {e}")
        return repository, pr

    def get_pr_files(
        self, prnumber: int, owner="NixOS", repo="nixpkgs"
    ) -> tuple[dict[str, str], dict[str, str]]:
        """Function to get files changed in a pull request.
        Arguments:
            - owner: The owner of the repository (default: "NixOS")
            - repo: The name of the repository (default: "nixpkgs")
            - prnumber: The number of the pull request (default: 0)
        Returns:
            - files_content: A dictionary mapping file names to their content at the head of the PR
            - files_patches: A dictionary mapping file names to their patch (diff) in the PR
        """
        with self.__get_github_client() as g:
            try:
                repository, pr = self.__get_pr(
                    g, prnumber=prnumber, owner=owner, repo=repo
                )
                files = pr.get_files()
                files_content, files_patches = {}, {}
                for file in files:
                    print(f"File: {file.filename}")
                    if file.filename in BLACK_LISTED_FILES:
                        print(f"Skipping blacklisted file: {file.filename}")
                        continue
                    patch = file.patch
                    file_content = repository.get_contents(
                        file.filename, ref=pr.head.sha
                    ).decoded_content.decode("utf-8")
                    if file_content:
                        files_content[file.filename] = file_content
                        files_patches[file.filename] = patch
            except ValueError as e:
                print(f"Error fetching PR: {e}")
                return {}, {}
            except GithubException as e:
                print(f"GitHub API error fetching PR files: {e}")
                return {}, {}
            except Exception as e:
                print(f"Unexpected error fetching PR files: {e}")
                return {}, {}
        return files_content, files_patches

    def submit_review(
        self,
        prnumber: int,
        review_body: str,
        reviews: dict[str, Any],
        owner: str = "NixOS",
        repo: str = "nixpkgs",
        review_type: REVIEW_TYPE = REVIEW_TYPE.COMMENT,
    ):
        if reviews == {}:
            print("No reviews to submit.")
            return
        with self.__get_github_client() as g:
            try:
                _, pr = self.__get_pr(g, prnumber=prnumber, owner=owner, repo=repo)
                review_comments = create_suggestions_from_reviews(reviews)
                _ = pr.create_review(
                    body=review_body, event=review_type.value, comments=review_comments
                )
            except ValueError as e:
                print(f"Error fetching PR: {e}")
            except GithubException as e:
                print(f"GitHub API error fetching PR files: {e}")
            except Exception as e:
                print(f"Error submitting review: {e}")
