from .base import SQLRepository
from models.organization_user import OrganizationUserRead


class OrganizationUserRepository(SQLRepository[OrganizationUserRead]):
    """Repository for managing organization_user in SQL."""

    def __init__(self):
        super().__init__(model=OrganizationUserRead, collection="OrganizationUser")

    async def add_user(
        self, user_id: int, organization_id: int
    ) -> OrganizationUserRead:
        """Add a user to an organization."""
        if await self.exists(userId=user_id, organizationId=organization_id):
            raise ValueError("User already exists in the organization.")
        return await self.create({"userId": user_id, "organizationId": organization_id})

    async def get_organizations_by_user_id(
        self, user_id: int
    ) -> list[OrganizationUserRead]:
        """Get all organizations for a user."""
        return await self.find({"userId": user_id}, {"include": {"organization": True}})
