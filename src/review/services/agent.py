from typing import final
from src.agents import AGENTS


@final
class AgentService:
    def __init__(self, agent: AGENTS, model: str):
        self.system_prompt = ""
        self.client_prompt = "tok tok who is there"
        self.agent = agent
        self.model = model
        self.agent_client = AGENTS.get_client_class(agent)

    def ask_agent_for_review(self):
        """
        Ask specified agent for code review for a specific review point
        """
        client = self.agent_client(env_var_name=self.agent + "_API_KEY")
        rep = client.ask(
            system_prompt=self.system_prompt,
            user_prompt=self.client_prompt,
            model=self.model,
        )
        print(rep)


if __name__ == "__main__":
    agent_service = AgentService(AGENTS.MISTRAL, "ministral-8b-latest")
    agent_service.ask_agent_for_review()
