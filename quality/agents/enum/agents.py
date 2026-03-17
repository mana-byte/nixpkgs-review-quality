"""This module defines the AGENTS enumeration, which represents the supported AI agents. Each agent is represented as a string value. The get_client_class method can be used to retrieve the corresponding client class for each agent."""

from enum import Enum

from quality.agents.clients import MistralClient, OpenAIClient
from quality.agents.clients.base_client import BaseClient


class AGENTS(str, Enum):
    """Enumeration of supported AI agents. Each agent is represented as a string value. The get_client_class method can be used to retrieve the corresponding client class for each agent."""

    # IMPLEMENTED
    MISTRAL = "MISTRAL"
    OPEN_AI = "OPEN_AI"
    # NOT IMPLEMENTED YET
    # CLAUDE = "CLAUDE"

    @classmethod
    def get_client_class(cls, agent: "AGENTS") -> type[BaseClient]:
        """Returns the client class corresponding to the given agent. If the agent is not supported, raises a ValueError."""
        agent_to_client_mapping = {
            cls.MISTRAL: MistralClient,
            cls.OPEN_AI: OpenAIClient,
        }
        client_class = agent_to_client_mapping.get(agent)
        if client_class is None:
            raise ValueError(f"Unsupported agent name: {agent}")
        return client_class
