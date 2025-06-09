from pydantic import BaseModel
from typing import Optional
from .user import UserRead
from .organization import OrganizationRead


class OrganizationUserBase(BaseModel):
    organizationId: int
    userId: int


class OrganizationUserCreate(OrganizationUserBase):
    pass


class OrganizationUserRead(OrganizationUserBase):
    id: int
    organization: Optional[OrganizationRead] = None
    user: Optional[UserRead] = None

    class Config:
        orm_mode = True
