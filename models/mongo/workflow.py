from enum import Enum

from pydantic import BaseModel

from utils.object_id import ObjectId

from .mongo_base import MongoModel
from .task import Task


class EventType(str, Enum):
    GIT_WEBHOOK = "git_webhook"
    MANUAL_PROMPT = "manual_prompt"


class FlowBase(BaseModel):
    organizationId: int
    is_head: bool | None = False
    next_flow: ObjectId | None
    is_task: bool | None = False
    enabled: bool | None = True
    events: list[EventType] = []
    created_by: int | None = None


class WorkflowBase(FlowBase):
    agent: str | None = ""
    prompt: str | None = ""


class WorkflowTaskBase(FlowBase):
    parameters: dict | None = {}
    task_template_id: ObjectId | None = None


class CreateWorkFlow(BaseModel):
    prompt: str
    is_head: bool = False
    events: list[EventType] = []
    agent: str


class CreateWorkflowTask(BaseModel):
    parameters: dict | None = {}
    task_template_id: ObjectId


class Workflow(MongoModel, WorkflowBase, WorkflowTaskBase, FlowBase):
    _collection_name = "workflows"
    task: Task | None = None
