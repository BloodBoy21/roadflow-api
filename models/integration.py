
from pydantic import BaseModel


class IntegrationBase(BaseModel):
    title: str
    name: str
    token: str | None = None
    organization_id: int
    owner_id: int


class IntegrationCreate(IntegrationBase):
    pass


class IntegrationRead(IntegrationBase):
    id: int


