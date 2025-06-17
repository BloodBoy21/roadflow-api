from datetime import datetime

from pydantic import BaseModel

from .mongo_base import MongoModel


class KnowledgeBase(BaseModel):
    organizationId: int | None
    text: str | None
    embeddings: list[int] | None
    tags: list[str] | None
    tagsEmbeddings: list[int] | None
    createdAt: datetime | None
    updatedAt: datetime | None


class Knowledge(MongoModel, KnowledgeBase):
    _collection_name = "knowledge"
