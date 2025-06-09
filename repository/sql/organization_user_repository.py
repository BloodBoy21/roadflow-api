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
