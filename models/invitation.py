from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from .organization import OrganizationRead


class RoleEnum(str, Enum):
    ADMIN = "admin"
    MEMBER = "member"
    OWNER = "owner"


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

    class Config:
        from_attributes = True
