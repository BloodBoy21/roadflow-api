from pydantic import BaseModel

from utils.object_id import ObjectId

from .mongo_base import MongoModel


class OutDocumentBase(BaseModel):
    organizationId: int | None
    imageUrl: str | None = None
    workflow: ObjectId | None = None
    text: str | None
    publish: bool | None = False
    platformsIds: list[int] | None = None
    tags: list[str] | None = None
    agent: str | None


class OutDocument(MongoModel, OutDocumentBase):
    _collection_name = "outDocuments"
