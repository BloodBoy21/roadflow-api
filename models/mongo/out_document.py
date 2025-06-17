from datetime import datetime

from pydantic import BaseModel

from utils.object_id import ObjectId

from .mongo_base import MongoModel


class OutDocumentBase(BaseModel):
    organizationId: int | None
    imageUrl: str | None
    workflow: ObjectId | None
    text: str | None
    publish: bool | None
    platformsIds: list[int] | None
    tags: list[str] | None
    createdAt: datetime | None


class OutDocument(MongoModel, OutDocumentBase):
    _collection_name = "outDocuments"
