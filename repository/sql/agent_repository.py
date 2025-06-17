from models.agent import AgentRead

from .base import SQLRepository


class AgentRepository(SQLRepository[AgentRead]):
    """Repository for managing agent in SQL."""

    def __init__(self):
        super().__init__(collection="Agent", model=AgentRead)
