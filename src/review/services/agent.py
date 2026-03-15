from typing import Any, final
from src.agents import AGENTS
import ast


@final
class AgentService:
    def __init__(self, agent: AGENTS, model: str):
        self.system_prompt = self.__read_system_prompt()
        self.agent = agent
        self.model = model
        self.agent_client = AGENTS.get_client_class(agent)

    def __read_system_prompt(self) -> str:
        with open("src/agents/prompts/agent_system_prompt.md", "r") as f:
            return f.read()

    def ask_agent_for_review(
        self,
        review_input: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Ask specified agent for code review for a specific review point
        """
        client = self.agent_client(env_var_name=self.agent + "_API_KEY")
        rep = client.ask(
            system_prompt=self.system_prompt,
            user_prompt=str(review_input),
            model=self.model,
        )
        return ast.literal_eval(rep)
