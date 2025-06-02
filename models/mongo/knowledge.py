from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .mongo_base import MongoModel


class KnowledgeBase(BaseModel):
    organizationId: Optional[int]
    text: Optional[str]
    embeddings: Optional[List[int]]
    tags: Optional[List[str]]
    tagsEmbeddings: Optional[List[int]]
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]


class Knowledge(MongoModel, KnowledgeBase):
    _collection_name = "knowledge"
