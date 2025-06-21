from pydantic import BaseModel


class AgentBase(BaseModel):
    name: str
    enabled: bool = True
    organization_id: int


class AgentCreate(AgentBase):
    pass


class AgentRead(AgentBase):
    id: int

