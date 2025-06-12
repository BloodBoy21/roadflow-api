from pydantic import BaseModel
from typing import Optional
from .organization import OrganizationRead


class InputWebhookBase(BaseModel):
    name: str
    key: str
    description: Optional[str] = None
    org_id: int
    type: str


class InputWebhookCreate(BaseModel):
    name: str
    description: Optional[str] = None
    type: str


class InputWebhookRead(InputWebhookBase):
    id: int
    organization: Optional[OrganizationRead] = None

    class Config:
        from_attributes = True
