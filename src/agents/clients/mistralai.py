from contextlib import contextmanager
from typing import Any, Iterator, override
from mistralai import Mistral

from src.agents.clients.base_client import BaseClient


class MistralClient(BaseClient):

    @override
    def ask(self, system_prompt: str, user_prompt: str, model: str) -> str:
        with self.get_client() as mistral_client:
            res = mistral_client.chat.complete(
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
        """Context manager to get a Mistral client using an access token from environment variables."""
        with Mistral(api_key=self.api_key) as mistral_client:
            yield mistral_client
