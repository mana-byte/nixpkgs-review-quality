from contextlib import contextmanager
from typing import Any, Iterator, override
from openai import OpenAI

from quality.agents.clients.base_client import BaseClient


class OpenAIClient(BaseClient):
    """OpenAI client class to interact with openai api"""

    @override
    def ask(self, system_prompt: str, user_prompt: str, model: str) -> str:
        """Sends a prompt to the OpenaAI API and returns the response content as a string."""
        with self.get_client() as openai_client:
            res = openai_client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                response_format={"type": "json_object"},
            )
            return res.choices[0].message.content

    @override
    @contextmanager
    def get_client(self) -> Iterator[Any]:
        """Context manager to get a OpenAI client using an access token from environment variables."""
        with OpenAI(api_key=self.api_key) as openai_client:
            yield openai_client
