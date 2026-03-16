"""Base client for for interacting with language model APIs."""

import os
from contextlib import contextmanager
from typing import Any, Iterator


class BaseClient:
    """Base client class for interacting with language model APIs. This class provides a common interface for different LLM clients, handling API key management and defining the structure for sending prompts and receiving responses."""

    def __init__(self, env_var_name: str):
        self.env_var_name: str = env_var_name
        self.api_key: str | None = os.getenv(env_var_name)
        if not self.api_key:
            raise ValueError(env_var_name + " environment variable is not set")

    @contextmanager
    def get_client(self) -> Iterator[Any]:
        """Context manager to get a client instance using an access token from environment variables."""
        raise NotImplementedError("This method should be implemented by subclasses.")

    def ask(self, system_prompt: str, user_prompt: str, model: str) -> str:
        """Method to send a prompt to the client and receive a response."""
        raise NotImplementedError("This method should be implemented by subclasses.")
