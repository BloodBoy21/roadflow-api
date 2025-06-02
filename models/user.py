from pydantic import BaseModel
from typing import Optional, List
from .integration import IntegrationRead
from .member import MemberRead


class UserBase(BaseModel):
    first_name: str
    last_name: str
    avatar: Optional[str] = None
    organization_id: int


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
    integrations: List[IntegrationRead] = []
    members: List[MemberRead] = []

    class Config:
        orm_mode = True
