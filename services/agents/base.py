from typing import Dict, List
from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    SseServerParams,
    StdioServerParameters,
)
from google.genai import types
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from models.inputs.agent import ContentConfig

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gemini-2.0-flash")


class AgentFactory:
    @staticmethod
    def create_agent(
        agent_name: str,
        tools: List[types.Tool],
        server_params: SseServerParams | StdioServerParameters,
        agent_params: Dict[str, str] = None,
        model: str = DEFAULT_MODEL,
        description: str = "An agent that can perform various tasks using tools.",
        content_config: ContentConfig = None,
        output_key: str = None,
    ) -> LlmAgent:
        """
        Create an LLM agent with the specified parameters.
        """
        if agent_params is None:
            agent_params = {}

        toolset = MCPToolset(
            tools=tools,
            server_params=server_params,
            agent_params=agent_params,
        )

        return LlmAgent(
            name=agent_name,
            toolset=toolset,
            model=model,
            description=description,
            global_instruction=AgentFactory.global_prompt,
            generate_content_config=types.GenerateContentConfig(
                temperature=content_config.temperature,
                top_p=content_config.top_p,
                top_k=content_config.top_k,
            ),
            output_key=output_key or AgentFactory.create_output_key(agent_name),
        )

    @property
    def global_prompt(self) -> str:
        """
        Returns the global prompt for the agent.
        """
        today = datetime.now(ZoneInfo("America/Mexico_City")).strftime("%Y-%m-%d")
        return f"""
        ## Internal utils
        Today is: {today} (America/Mexico_City timezone)
        
      """

    @staticmethod
    def create_output_key(agent_name: str) -> str:
        """
        Create a unique output key for the agent.
        """
        timestamp = datetime.now(ZoneInfo("America/Mexico_City")).strftime(
            "%Y%m%d%H%M%S"
        )
        return f"{agent_name}_output_{timestamp}"
