from models.invitation import InvitationRead

from .base import SQLRepository


class InvitationRepository(SQLRepository[InvitationRead]):
    """Repository for managing invitations in SQL."""

    def __init__(self):
        super().__init__(model=InvitationRead, collection="Invitation")

    async def get_by_email_and_org(
        self, email: str, organization_id: int
    ) -> InvitationRead | None:
        """Get an invitation by email and organization ID."""
        query = {
            "email": email,
            "organizationId": organization_id,
        }
        return await self.find_one(query)

    async def get_by_organization_id(
        self, organization_id: int, page: int = 1, limit: int = 20
    ) -> tuple[list[InvitationRead], int, int]:
        """Get all invitations for a specific organization."""
        query = {"organizationId": organization_id}
        return await self.paginate(query, page=page, limit=limit)