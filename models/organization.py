from pydantic import BaseModel, Field
from typing import Optional, List
from .user import UserRead
from .member import MemberRead
from .integration import IntegrationRead
from .agent import AgentRead


class OrganizationBase(BaseModel):
    name: str
    domain: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None


class OrganizationCreate(OrganizationBase):
    ownerId: int


class OrganizationRead(OrganizationBase):
    id: int
    users: Optional[List[UserRead]] = []
    members: Optional[List[MemberRead]] = []
    integrations: Optional[List[IntegrationRead]] = []
    agents: Optional[List[AgentRead]] = []
    ownerId: Optional[int] = None
    owner: Optional[UserRead] = None

    class Config:
        from_attributes = True
