from enum import Enum
from typing import Any

from pydantic import BaseModel, field_validator

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
    title: str
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

    @field_validator("parameters")
    def validate_parameters(cls, v):
        if not isinstance(v, list):
            raise ValueError("Parameters must be a list")
        for param in v:
            if not isinstance(param, Parameter):
                raise ValueError("Each parameter must be an instance of Parameter")
            param.name = param.name.strip().lower().replace(" ", "_")
        return v

class TaskOutput(BaseModel):
    id: ObjectId
    title: str
    description: str | None = ""
    parameters: list[Parameter] = []


class Task(MongoModel, TaskBase):
    _collection_name = "tasks"
