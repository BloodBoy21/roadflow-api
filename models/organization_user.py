
from pydantic import BaseModel

from .organization import OrganizationRead
from .user import UserRead


class OrganizationUserBase(BaseModel):
    organizationId: int
    userId: int
    role: str = "member"





class OrganizationUserCreate(OrganizationUserBase):
    pass


class OrganizationUserRead(OrganizationUserBase):
    id: int
    organization: OrganizationRead | None = None
    user: UserRead | None = None
