from models.organization_user import OrganizationUserRead

from .base import SQLRepository


class OrganizationUserRepository(SQLRepository[OrganizationUserRead]):
    """Repository for managing organization_user in SQL."""

    def __init__(self):
        super().__init__(model=OrganizationUserRead, collection="OrganizationUser")

    async def add_user(
        self, user_id: int, organization_id: int, role: str = "member"
    ) -> OrganizationUserRead:
        """Add a user to an organization."""
        if await self.exists(userId=user_id, organizationId=organization_id):
            raise ValueError("User already exists in the organization.")
        return await self.create(
            {"userId": user_id, "organizationId": organization_id, "role": role}
        )

    async def get_organizations_by_user_id(
        self, user_id: int
    ) -> list[OrganizationUserRead]:
        """Get all organizations for a user."""
        return await self.find({"userId": user_id}, {"include": {"organization": True}})

    async def user_in_organization(self, user_id: int, organization_id: int) -> bool:
        """Check if a user is in an organization."""
        return await self.exists(userId=user_id, organizationId=organization_id)

    async def get_members_by_organization_id(
        self, organization_id: int, page: int = 1, limit: int = 20
    ) -> tuple[list[OrganizationUserRead], int, int]:
        """Get all members of an organization."""
        query = {"organizationId": organization_id}
        return await self.paginate(
            query, page=page, limit=limit, options={"include": {"user": True}}
        )

    async def get_user_by_id_and_organization_id(
        self, user_id: int, organization_id: int
    ) -> OrganizationUserRead | None:
        """Get a user by user ID and organization ID."""
        return await self.find_one(
            {"userId": user_id, "organizationId": organization_id},
            {"include": {"user": True}},
        )
