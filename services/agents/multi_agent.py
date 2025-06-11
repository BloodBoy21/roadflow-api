from .base import AgentBase
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from loguru import logger
import importlib
from .helpers.common import snake_to_camel

mex_tz = ZoneInfo("America/Mexico_City")


class MultiAgent(AgentBase):
    def __init__(self, org_id: int = None):
        self.sub_agents = self.__get_agents__(org_id)
        super().__init__(
            name="MultiAgent",
            description="An agent that can perform multiple tasks using various tools. It can switch between different roles and handle diverse requests efficiently using sub agents.",
            instructions=self._instructions_,
            org_id=org_id,
            sub_agents=self.sub_agents,
        )

    @property
    def _instructions_(self):
        PROMPT_TEMPLATE = """\
        You are **MultiAgent**, an expert orchestrator in multi-agent systems.

        ### Available Sub-Agents
        {agent_catalog}


        ---

        ### Your Mission
        1. Carefully analyze the user's request.
        2. Select the most appropriate sub-agent(s) based on their descriptions.
          - If the task involves multiple sequential steps, coordinate them in **order**.
          - If parts of the task can be processed independently, orchestrate a **parallel** query and merge the results.
        3. Ensure the final response is coherent, complete, and consistent.
        4. Deliver **a single final response** that is clear, professional, and user-friendly.
        5. If a default agent is specified, give it selection priority when appropriate.

        ---

        ### Style Guidelines
        - Respond in **Spanish**, using a **formal and courteous** tone.
        - Do **not** disclose internal orchestration details (e.g., agent names, method calls, IDs).
        - If none of the sub-agents can fulfill the request, respond with:  
          _"Lo siento, no dispongo de la información necesaria para resolver tu solicitud."_

        ---

        ### Metadata
        Use the following metadata to assist orchestration:
        - Current date and time: **{datetime}** (YYYY-MM-DD HH:MM:SS)

        ---

        ### Output Format
        Return **only** the final text to be shown to the user.
        """
        agent_catalog_lines = [
            f"- **{ag.name}**: {ag.description.strip()}" for ag in self.sub_agents
        ]
        catalog = "\n".join(agent_catalog_lines)

        return PROMPT_TEMPLATE.format(
            agent_catalog=catalog,
            datetime=datetime.now(mex_tz).strftime("%Y-%m-%d %H:%M:%S"),
        )

    def __get_agents__(self, org_id: int = None):
        """
        Discover and return the list of sub-agents available for this multi-agent.
        """
        agents_path = Path(__file__).parent
        agents_files = [
            f.stem
            for f in agents_path.glob("*_agent.py")
            if f.is_file() and f.stem != "multi_agent"
        ]
        agents = []

        for agent_file in agents_files:
            try:
                logger.info(f"Importing agent: {agent_file}")
                module = importlib.import_module(f"services.agents.{agent_file}")
                class_name = f"{snake_to_camel(agent_file)}"
                agent_class = getattr(module, class_name)
                if issubclass(agent_class, AgentBase):
                    agent_instance = agent_class(org_id=org_id)
                    agents.append(agent_instance.build())
                else:
                    logger.warning(f"{class_name} is not a subclass of AgentBase")
            except (ImportError, AttributeError, TypeError) as e:
                logger.error(f"Error importing agent '{agent_file}': {e}")

        return agents
