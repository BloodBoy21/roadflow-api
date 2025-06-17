from models.mongo.agents import Agent, AgentBase

from .base import MongoRepository


class AgentRepository(MongoRepository[Agent]):
    """Repository for managing Agents in MongoDB."""

    def __init__(self):
        super().__init__(collection="agents", model=Agent)

    def get_agent_config(self, org_id: int, name: str) -> AgentBase:
        """
        Returns the agent configuration for a given organization ID.
        """
        if org_id is None:
            raise ValueError("org_id is not set for the agent.")
        agent = self.find_one({"organizationId": org_id, "name": name})
        if not agent:
            return None
        return agent
