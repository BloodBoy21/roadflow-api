import importlib
import os
from datetime import datetime
from pathlib import Path

from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from loguru import logger

from .base import AgentBase
from .helpers.common import snake_to_camel

APP_NAME = os.getenv("APP_NAME", "roadflow")


def get_available_agents(folder: Path, exclude: str = "") -> list[str]:
    """
    Return a list of available agent names (without `_agent.py` suffix) from a folder.

    Args:
        folder (Path): The folder path to scan for agent files.
        exclude (str): Stem name to exclude (default is 'multi_agent').

    Returns:
        list[str]: List of agent names (without file extension).
    """
    return [
        f.stem.replace("_agent", "")
        for f in folder.glob("*_agent.py")
        if f.is_file() and f.stem != exclude
    ]


class AgentCaller:
    def __init__(self, org_id: int, agent: LlmAgent = None):
        self.agent = agent
        self.org_id = org_id
        self.session_service = InMemorySessionService()
        self.id = self.__get_id()
        self.session = None

    @staticmethod
    def create(org_id: int, agent: str):
        agent_instance: LlmAgent = AgentCaller.get_llm_agent(org_id, agent)
        if not agent_instance:
            logger.error(f"Agent {agent} not found for org_id {org_id}")
            return None
        return AgentCaller(org_id=org_id, agent=agent_instance)

    @staticmethod
    def get_llm_agent(org_id: int, agent_name: str) -> LlmAgent:
        """
        Get an LlmAgent instance by org_id and agent_name.
        """
        agent: AgentBase = AgentCaller.get_agent(org_id, agent_name)
        if not isinstance(agent, AgentBase):
            raise TypeError(
                f"Expected an instance of AgentBase, got {type(agent).__name__}"
            )
        return agent.build()

    @staticmethod
    def get_agent(org_id: int, agent_name: str) -> AgentBase:
        """
        Get an agent instance by org_id and agent_name.
        """
        if not agent_name:
            raise ValueError("Agent name cannot be None or empty")
        available_agents = get_available_agents(Path(__file__).parent)
        if agent_name not in available_agents:
            raise ValueError(
                f"Agent '{agent_name}' is not available. Available agents: {available_agents}"
            )
        agent_module = importlib.import_module(f"services.agents.{agent_name}_agent")
        agent_class: AgentBase = getattr(
            agent_module, f"{snake_to_camel(agent_name)}Agent"
        )
        if not issubclass(agent_class, AgentBase):
            raise TypeError(
                f"Agent class {agent_class.__name__} is not a subclass of AgentBase"
            )
        return agent_class(org_id=org_id)

    def init_runner(self):
        self.runner = Runner(
            agent=self.agent,
            app_name=APP_NAME,
            session_service=self.session_service,
        )

    async def generate(self, text: str):
        await self.__get_session()
        self.init_runner()
        logger.info(
            f"Generating response for org_id {self.org_id} with session {self.id}"
        )
        message_content = types.Content(
            parts=[types.Part.from_text(text=text)],
            role="user",
        )
        events = self.runner.run_async(
            user_id=str(self.org_id),
            new_message=message_content,
            session_id=self.id,
        )
        response = ""
        async for event in events:
            if event.is_final_response():
                logger.info(f"Final response: {event.content}")
                response = event.content.parts[0].text if event.content else ""
                break
        return response.strip()

    async def stop(self):
        logger.info(f"Stopping session for org_id {self.org_id}")
        try:
            pass
        except Exception as e:
            logger.error(f"Error stopping session: {e}")

    async def __get_session(self):
        logger.info(f"Getting session for org_id {self.org_id}")
        try:
            session = await self.session_service.get_session(
                app_name=APP_NAME,
                user_id=str(self.org_id),
                session_id=self.id,
            )
            if session:
                logger.info(
                    f"Session for org_id {self.org_id} already exists: {session.id}"
                )
                return session
        except Exception as e:
            logger.error(f"Error getting session: {e}")
        logger.info(
            f"Creating new session for org_id {self.org_id}, session_id {self.id}"
        )
        self.session = await self.session_service.create_session(
            app_name=APP_NAME,
            user_id=str(self.org_id),
            session_id=self.id,
        )
        return self.session

    def __get_id(self):
        today = datetime.now().strftime("%Y%m%d")
        return f"{self.org_id}_{today}"
