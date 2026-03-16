from typing import Any


def find_line_numbers(file: str, word: str) -> list[int]:
    lines = file.splitlines()
    return [i + 1 for i, line in enumerate(lines) if word in line]


def number_each_line(file: str) -> str:
    lines = file.splitlines()
    return "\n".join(f"{i + 1}: {line}" for i, line in enumerate(lines))


def create_suggestions_from_reviews(reviews: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "path": file_path,
            "line": change["line_number"],
            "side": "RIGHT",  # Referring to the new code in the PR
            "body": (
                f"{change['explanation']}\n\n"
                f"```suggestion\n"
                f"{change['after']}\n"
                f"```"
            ),
        }
        for file_path, changes in reviews.items()
        for change in changes
    ]
