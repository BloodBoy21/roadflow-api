
from pydantic import BaseModel

from .agent import AgentRead
from .integration import IntegrationRead
from .user import UserRead


class OrganizationBase(BaseModel):
    name: str
    domain: str | None = None
    description: str | None = None
    image: str | None = None


class OrganizationCreate(OrganizationBase):
    ownerId: int


class OrganizationRead(OrganizationBase):
    id: int
    users: list[UserRead] | None = []
    integrations: list[IntegrationRead] | None = []
    agents: list[AgentRead] | None = []
    ownerId: int | None = None
    owner: UserRead | None = None

