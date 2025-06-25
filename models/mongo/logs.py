import json
from typing import Any

from pydantic import BaseModel, field_validator

from utils.object_id import ObjectId

from .mongo_base import MongoModel
from datetime import datetime


class LogBase(BaseModel):
    organizationId: int
    type: str | None
    source: str | None
    data: dict[str, Any] | str | list[dict[str, Any]] | None = {}
    agent: str | None = None
    embeddings: list[int] | None = []
    source_id: ObjectId | None = None

class LogOutput(BaseModel):
    id: ObjectId
    type: str | None = None
    source: str | None = None
    data: dict[str, Any] | str | list[dict[str, Any]] | None = {}
    source: ObjectId | str = None
    source_event: dict[str, Any] | None = None
    createdAt: datetime = None


class Log(MongoModel, LogBase):
    _collection_name = "logs"
