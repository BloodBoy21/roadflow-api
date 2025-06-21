
from pydantic import BaseModel

from .organization import OrganizationRead


class InputWebhookBase(BaseModel):
    name: str
    key: str
    description: str | None = None
    org_id: int
    type: str


class InputWebhookCreate(BaseModel):
    name: str
    description: str | None = None
    type: str


class InputWebhookRead(InputWebhookBase):
    id: int
    organization: OrganizationRead | None = None

