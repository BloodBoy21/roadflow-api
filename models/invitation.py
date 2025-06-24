from datetime import datetime

from pydantic import BaseModel

from shared.roles import RoleEnum

from .organization import OrganizationRead


class InvitationBase(BaseModel):
    email: str
    role: RoleEnum
    organizationId: int
    accepted: bool = False


class InvitationCreate(BaseModel):
    email: str
    role: RoleEnum


class InvitationRead(InvitationBase):
    id: int
    createdAt: datetime
    expiresAt: datetime
    organization: OrganizationRead | None = None


