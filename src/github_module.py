from contextlib import contextmanager
from github import Github
from github import Auth
import os

BLACK_LISTED_FILES = {
    "pkgs/top-level/python-packages.nix",
    "maintainers/maintainer-list.nix",
    "pkgs/by-name/hy/hyprland/info.json",
}


@contextmanager
def get_github_client(env_var_name="GITHUB_ACCESS_TOKEN"):
    """Context manager to get a GitHub client using an access token from environment variables."""
    GITHUB_ACCESS_TOKEN = os.getenv(env_var_name)
    if not GITHUB_ACCESS_TOKEN:
        raise ValueError(env_var_name + " environment variable is not set")
    auth = Auth.Token(GITHUB_ACCESS_TOKEN)
    with Github(auth=auth) as g:
        yield g


def get_pr_files(
    prnumber: int, owner="NixOS", repo="nixpkgs"
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
    with get_github_client() as g:
        repo = g.get_repo(f"{owner}/{repo}")
        pr = repo.get_pull(prnumber)
        files = pr.get_files()
        files_content, files_patches = {}, {}
        for file in files:
            print(f"File: {file.filename}")
            if file.filename in BLACK_LISTED_FILES:
                print(f"Skipping blacklisted file: {file.filename}")
                continue
            try:
                patch = file.patch
                file_content = repo.get_contents(
                    file.filename, ref=pr.head.sha
                ).decoded_content.decode("utf-8")
                if file_content:
                    files_content[file.filename] = file_content
                    files_patches[file.filename] = patch
            except Exception as e:
                print(f"Error fetching content for {file.filename}: {e}")
    return files_content, files_patches


if __name__ == "__main__":
    get_pr_files(prnumber=493762)
