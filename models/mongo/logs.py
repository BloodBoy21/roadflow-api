from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from .mongo_base import MongoModel


class LogBase(BaseModel):
    organizationId: Optional[int]
    type: Optional[str]
    source: Optional[str]
    data: Optional[Dict[str, Any]]
    agent: Optional[str]
    embeddings: Optional[List[int]]
    createdAt: Optional[datetime]


class Log(MongoModel, LogBase):
    _collection_name = "logs"
