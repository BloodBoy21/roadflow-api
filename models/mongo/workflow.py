from pydantic import BaseModel
from typing import Optional, List
from .mongo_base import MongoModel
from utils.object_id import ObjectId
from enum import Enum


class EventType(str, Enum):
    GIT_WEBHOOK = "git_webhook"
    MANUAL_PROMPT = "manual_prompt"


class FlowBase(BaseModel):
    organizationId: int
    is_head: Optional[bool] = False
    next_flow: Optional[ObjectId]
    is_task: Optional[bool] = False
    enabled: Optional[bool] = True
    events: List[EventType] = []
    created_by: Optional[int] = None


class WorkflowBase(FlowBase):
    agent: Optional[str] = ""
    prompt: Optional[str] = ""


class WorkflowTaskBase(FlowBase):
    task_type: Optional[str] = ""
    extra_data: Optional[dict] = {}
    task_template_id: Optional[ObjectId] = None


class CreateWorkFlow(BaseModel):
    prompt: str
    is_head: bool = False
    next_flow: Optional[ObjectId] = None
    is_task: bool = False
    enabled: bool = True
    events: List[EventType] = []
    agent: str


class CreateWorkflowTask(BaseModel):
    task_type: str
    is_head: bool = False
    next_flow: Optional[ObjectId] = None
    is_task: bool = True
    enabled: bool = True
    events: List[EventType] = []
    parameters: Optional[dict] = {}
    task_template_id: ObjectId


class Workflow(MongoModel, WorkflowBase, WorkflowTaskBase):
    _collection_name = "workflows"
