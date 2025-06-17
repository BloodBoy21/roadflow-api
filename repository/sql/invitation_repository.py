from models.invitation import InvitationRead

from .base import SQLRepository


class InvitationRepository(SQLRepository[InvitationRead]):
    """Repository for managing invitations in SQL."""

    def __init__(self):
        super().__init__(model=InvitationRead, collection="Invitation")
