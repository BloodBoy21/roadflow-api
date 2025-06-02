from pydantic import BaseModel
from typing import Optional, List
from .user import UserRead
from .member import MemberRead
from .integration import IntegrationRead
from .agent import AgentRead


class OrganizationBase(BaseModel):
    name: str
    domain: str
    description: Optional[str] = None
    image: Optional[str] = None


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationRead(OrganizationBase):
    id: int
    users: List[UserRead] = []
    members: List[MemberRead] = []
    integrations: List[IntegrationRead] = []
    agents: List[AgentRead] = []

    class Config:
        orm_mode = True
