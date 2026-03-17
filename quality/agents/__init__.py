"""This module provides a unified interface for interacting with various AI agents. It defines an enumeration of supported agents and a method to retrieve the corresponding client class for each agent. This allows users to easily switch between different AI agents without changing their codebase, as long as they adhere to the defined client interface."""

from quality.agents.enum.agents import AGENTS

__all__ = ["AGENTS"]
