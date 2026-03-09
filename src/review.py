from mistralai import Mistral
from review_points.review_points import create_review_points_dict
import os
from contextlib import contextmanager
from github_module import get_pr_files
from pydantic import BaseModel

@contextmanager
def get_mistral_client(env_var_name="MISTRAL_API_KEY"):
    """Context manager to get a Mistral client using an access token from environment variables."""
    MISTRAL_API_KEY = os.getenv(env_var_name)
    if not MISTRAL_API_KEY:
        raise ValueError(env_var_name + " environment variable is not set")
    with Mistral(api_key=MISTRAL_API_KEY) as mistral_client:
        yield mistral_client


def generate_review_points(files_content, files_patches, points={}):
    """Function to generate a list of reviews that contain the corrected file based on review_points.
    Arguments:
        - files_content: A dictionary mapping file names to their content at the head of the PR
        - files_patches: A dictionary mapping file names to their patch (diff) in the PR
        - points: A dictionary mapping criterias to a list of example git diff (strings) that illustrate how to make files compliant with this criteria.
    Returns:
        - A dictionary mapping file names to a dictionary containing the changes that should be made in the file to make it compliant with the review points. The change is in the form of a git diff.
    """
    with get_mistral_client() as mistral_client:
        res = mistral_client.chat.complete(
            model="devstral-latest",
            response_format={
                "type": "json_object",
            },
            messages=[
                {
                    "role": "system",
                    "content": """
                    Goal: You are a nix code reviewer. You will need to generate a list of reviews that contain the corrected file based of review_points.
                    Inputs:
                        - files_content: A dictionary mapping file names to their content at the head of the PR
                        - review_points: A dictionnary mapping review point to dictionnary of criterias that maps criteria_names to a list of example git diff (strings) OR a description/instruction that illustrate how to make files compliant with this criteria.

                    Outputs:
                        - file_name: key is the name of the file that needs to be reviewed, value is a dictionnary containing:
                            - changes: a dictionnary mapping a review point with the git diff that makes the file compliant towards the review point. The change should be in the form of a git diff.

                        - FORMAT EXAMPLE:
                        {
                            "file_name": {
                                changes: {
                                    "review_point_1": "git diff that should be applied to the file to make it compliant with the review point 1",
                                    "review_point_2": "git diff that should be applied to the file to make it compliant with the review point 2",
                                }
                            },
                            "file_name_2": {
                                changes: {
                                    "review_point_1": "git diff that should be applied to the file to make it compliant with the review point 1",
                                }
                            }
                        }
                    """,
                },
                {
                    "role": "user",
                    "content": """
                    file_content: """
                    + str(files_content)
                    + """

                    review_points: """
                    + str(points)
                    + """
                    """,
                },
            ],
        )
    return res.choices[0].message.content

if __name__ == "__main__":
    files_content, files_patches = get_pr_files(prnumber=497957)
    criteria_names = ["meta", "finalAttrs"]
    points = create_review_points_dict(criteria_names)
    print(generate_review_points(files_content, files_patches, points=points))
