from .base import SQLRepository
from models.integration import IntegrationRead


class IntegrationRepository(SQLRepository[IntegrationRead]):
    """Repository for managing integration in SQL."""

    def __init__(self):
        super().__init__(model=IntegrationRead, collection="Integration")
