from contextlib import contextmanager
from mistralai import Mistral
import os


@contextmanager
def get_mistral_client(env_var_name: str="MISTRAL_API_KEY"):
    """Context manager to get a Mistral client using an access token from environment variables."""
    MISTRAL_API_KEY = os.getenv(env_var_name)
    if not MISTRAL_API_KEY:
        raise ValueError(env_var_name + " environment variable is not set")
    with Mistral(api_key=MISTRAL_API_KEY) as mistral_client:
        yield mistral_client
