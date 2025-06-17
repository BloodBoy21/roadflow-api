from typing import Any

from pydantic import BaseModel

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


class Log(MongoModel, LogBase):
    _collection_name = "logs"
