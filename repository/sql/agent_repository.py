from .base import SQLRepository
from models.agent import AgentRead


class AgentRepository(SQLRepository[AgentRead]):
    """Repository for managing agent in SQL."""

    def __init__(self):
        super().__init__(collection="Agent", model=AgentRead)
