from pydantic import BaseModel
from typing import Optional
from .mongo_base import MongoModel
from models.inputs.agent import ContentConfig


class AgentBase(BaseModel):
    organizationId: int
    name: str
    description: Optional[str] = ""
    instructions: Optional[str] = None
    content_config: Optional[ContentConfig] = ContentConfig()
    global_instruction: Optional[str] = None


class Agent(MongoModel, AgentBase):
    _collection_name = "agents"
