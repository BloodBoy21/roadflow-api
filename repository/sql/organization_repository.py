from models.organization import OrganizationRead

from .base import SQLRepository


class OrganizationRepository(SQLRepository[OrganizationRead]):
    """Repository for managing organization in SQL."""

    def __init__(self):
        super().__init__(model=OrganizationRead, collection="Organization")
