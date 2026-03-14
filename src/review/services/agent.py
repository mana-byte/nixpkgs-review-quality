from typing import final
from src.agents import AGENTS


@final
class AgentService:
    def __init__(self, agent: AGENTS):
        self.system_prompt = ""
        self.client_prompt = ""
        self.agent = agent
        self.agent_client = AGENTS.get_client_class(agent)

    def ask_agent_for_review(self):
        print(self.agent)


if __name__ == "__main__":
    agent_service = AgentService(AGENTS.MISTRAL)
    agent_service.ask_agent_for_review()
