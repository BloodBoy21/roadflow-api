
from pydantic import BaseModel

from models.inputs.agent import ContentConfig

from .mongo_base import MongoModel


class AgentBase(BaseModel):
    organizationId: int
    name: str
    description: str | None = ""
    instructions: str | None = None
    content_config: ContentConfig | None = ContentConfig()
    global_instruction: str | None = None


class AgentOutput(BaseModel):
    name: str
    description: str | None = ""
    instructions: str | None = ""
    content_config: ContentConfig | None = ContentConfig()
    global_instruction: str | None = ""


class AgentUpdate(BaseModel):
    description: str | None = None
    instructions: str | None = None
    content_config: ContentConfig | None = None
    global_instruction: str | None = None


class Agent(MongoModel, AgentBase):
    _collection_name = "agents"
