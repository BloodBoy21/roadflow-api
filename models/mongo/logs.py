import json
from typing import Any

from pydantic import BaseModel, field_validator

from utils.object_id import ObjectId

from .mongo_base import MongoModel


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
    source_event: list[dict[str, Any]] | None = None

    @field_validator("source_event", mode="before")
    def validate_source_event(cls, v):
        list_items = []
        if isinstance(v, dict):
            v = [v]
        for item in v:
            if isinstance(item, dict):
                list_items.append(json.loads(json.dumps(item, default=str)))

        return list_items if list_items else None

class Log(MongoModel, LogBase):
    _collection_name = "logs"
