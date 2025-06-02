from pydantic import BaseModel
from typing import Optional
from .mongo_base import MongoModel


class WorkflowBase(BaseModel):
    organizationId: Optional[int]
    agent: str
    prompt: Optional[str]
    integrationId: Optional[int]
    nextAgent: Optional[str]


class Workflow(MongoModel, WorkflowBase):
    _collection_name = "workflows"
