from .base import SQLRepository
from models.organization import OrganizationRead


class OrganizationRepository(SQLRepository[OrganizationRead]):
    """Repository for managing organization in SQL."""

    def __init__(self):
        super().__init__(model=OrganizationRead,collection="Organization")
