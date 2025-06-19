from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from utils.object_id import ObjectId

from .mongo_base import MongoModel


class ParameterType(str, Enum):
    STRING = "string"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    FLOAT = "float"
    OBJECT = "object"
    ARRAY = "array"


class Parameter(BaseModel):
    name: str
    type: ParameterType
    description: str | None = ""
    default: Any | None = None
    required: bool = False
    options: list | None = None  # For ENUM-like parameters


class TaskBase(BaseModel):
    title: str
    function_name: str
    description: str | None = ""
    parameters: list[Parameter] = []


class TaskCreate(TaskBase):
    pass


class TaskOutput(BaseModel):
    id: ObjectId
    title: str
    description: str | None = ""
    parameters: list[Parameter] = []


class Task(MongoModel, TaskBase):
    _collection_name = "tasks"
