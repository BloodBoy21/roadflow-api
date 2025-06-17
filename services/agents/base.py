import os
from datetime import datetime
from zoneinfo import ZoneInfo

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import (
    SseServerParams,
    StdioServerParameters,
)
from google.genai import types

from models.inputs.agent import ContentConfig
from models.mongo.agents import AgentBase as MongoAgent
from repository import repository

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gemini-2.0-flash")


class AgentFactory:
    @staticmethod
    def create_agent(
        agent_name: str,
        tools: list[types.Tool],
        server_params: SseServerParams | StdioServerParameters = None,
        agent_params: dict[str, str] = None,
        model: str = DEFAULT_MODEL,
        description: str = "An agent that can perform various tasks using tools.",
        content_config: ContentConfig = None,
        output_key: str = None,
        global_instruction: str = None,
        instructions: str = None,
        sub_agents: list[LlmAgent] = None,
    ) -> LlmAgent:
        """
        Create an LLM agent with the specified parameters.
        """
        if agent_params is None:
            agent_params = {}
        return LlmAgent(
            name=agent_name,
            model=model,
            tools=tools,
            description=description,
            instruction=instructions or "",
            global_instruction=AgentFactory.global_prompt(
                custom_prompt=global_instruction or ""
            ),
            generate_content_config=types.GenerateContentConfig(
                temperature=content_config.temperature,
                top_p=content_config.top_p,
                top_k=content_config.top_k,
            ),
            output_key=output_key or AgentFactory.create_output_key(agent_name),
            sub_agents=sub_agents or [],
        )

    @staticmethod
    def global_prompt(custom_prompt: str = "") -> str:
        """
        Returns the global prompt for the agent.
        """
        today = datetime.now(ZoneInfo("America/Mexico_City")).strftime("%Y-%m-%d")
        return f"""
        ## Internal utils
        Today is: {today} (America/Mexico_City timezone)
        
        ## Global Instruction
        {custom_prompt}
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


class AgentBase:
    def __init__(
        self,
        name,
        description: str = "",
        org_id: int = None,
        sub_agents: list[LlmAgent] = None,
        instructions: str = None,
    ):
        self.agent: LlmAgent = None
        self.name: str = name
        self.description: str = description
        self.instructions: str = instructions or ""
        self.sub_agents: list[LlmAgent] = sub_agents
        self.org_id = org_id
        self.content_config: ContentConfig = ContentConfig()
        self.global_instruction: str = None
        self._get_config()

    def build(self):
        """
        Returns an instance of the current agent.
        """
        if self.agent is not None:
            return self.agent
        self.agent = AgentFactory.create_agent(
            agent_name=self.name,
            tools=self.build_tools,
            server_params=None,
            agent_params=None,
            description=self.description,
            content_config=self.content_config,
            global_instruction=self.global_instruction,
            instructions=self.instructions,
            sub_agents=self.sub_agents,
        )
        return self.agent

    @property
    def build_tools(self) -> list[types.Tool]:
        """
        Returns the tools available for the agent.
        """
        return []

    def get_agent_info(self) -> dict[str, str]:
        """
        Returns the agent information.
        """
        return {
            "name": self.name,
            "description": self.description,
            "instructions": self.instructions,
            "global_instruction": self.global_instruction,
            "content_config": self.content_config.model_dump(),
        }

    def _get_config(self) -> dict[str, str]:
        """
        Returns the agent configuration.
        """
        if self.org_id is None:
            raise ValueError("org_id is not set for the agent.")
        config_agent = repository.mongo.agent.get_agent_config(
            org_id=self.org_id, name=self.name
        )
        if config_agent is None:
            repository.mongo.agent.create(
                MongoAgent(
                    organizationId=self.org_id,
                    name=self.name,
                    description=self.description,
                    instructions=self.instructions,
                    content_config=self.content_config,
                    global_instruction=self.global_instruction,
                )
            )
            return
        self.instructions = (
            config_agent.instructions
            if config_agent.instructions
            else self.instructions
        )
        self.description = (
            config_agent.description if config_agent.description else self.description
        )
        self.content_config = (
            config_agent.content_config
            if config_agent.content_config
            else self.content_config
        )
        self.global_instruction = (
            config_agent.global_instruction
            if config_agent.global_instruction
            else self.global_instruction
        )
