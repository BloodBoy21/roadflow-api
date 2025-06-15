from pydantic import BaseModel
from typing import Optional, Dict
from .mongo_base import MongoModel
from enum import Enum


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
    description: Optional[str] = ""
    default: Optional[any] = None
    required: bool = False
    options: Optional[list] = None  # For ENUM-like parameters


class TaskBase(BaseModel):
    title: str
    function_name: str
    description: Optional[str] = ""
    parameters: Optional[Dict[str, Parameter]] = {}


class TaskOutput(BaseModel):
    title: str
    description: Optional[str] = ""
    parameters: Optional[Dict[str, Parameter]] = {}


class Task(MongoModel, TaskBase):
    _collection_name = "tasks"
