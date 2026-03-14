from src.agents.clients.mistralai import MistralClient
from src.agents.clients.base_client import BaseClient
from enum import Enum


class AGENTS(str, Enum):
    # IMPLEMENTED
    MISTRAL = "MISTRAL"
    # NOT IMPLEMENTED YET
    OPEN_AI = "OPEN_AI"
    CLAUDE = "CLAUDE"

    @classmethod
    def get_client_class(cls, agent: "AGENTS") -> type[BaseClient]:
        agent_to_client_mapping = {
            cls.MISTRAL: MistralClient,
        }
        client_class = agent_to_client_mapping.get(agent)
        if client_class is None:
            raise ValueError(f"Unsupported agent name: {agent}")
        return client_class
