from pydantic import BaseModel
from typing import Optional


class IntegrationBase(BaseModel):
    title: str
    name: str
    token: Optional[str] = None
    organization_id: int
    owner_id: int


class IntegrationCreate(IntegrationBase):
    pass


class IntegrationRead(IntegrationBase):
    id: int

    class Config:
        from_attributes = True
