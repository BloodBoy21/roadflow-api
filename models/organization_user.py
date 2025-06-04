from pydantic import BaseModel
from typing import Optional
from .user import UserRead
from .organization import OrganizationRead


class OrganizationUserBase(BaseModel):
    organization_id: int
    user_id: int


class OrganizationUserCreate(OrganizationUserBase):
    pass


class OrganizationUserRead(OrganizationUserBase):
    id: int
    organization: Optional[OrganizationRead]
    user: Optional[UserRead]

    class Config:
        orm_mode = True
