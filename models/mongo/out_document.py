from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .mongo_base import MongoModel
from utils.object_id import ObjectId


class OutDocumentBase(BaseModel):
    organizationId: Optional[int]
    imageUrl: Optional[str]
    workflow: Optional[ObjectId]
    text: Optional[str]
    publish: Optional[bool]
    platformsIds: Optional[List[int]]
    tags: Optional[List[str]]
    createdAt: Optional[datetime]


class OutDocument(MongoModel, OutDocumentBase):
    _collection_name = "outDocuments"
