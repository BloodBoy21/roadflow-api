from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Union
from .mongo_base import MongoModel


class LogBase(BaseModel):
    organizationId: int
    type: Optional[str]
    source: Optional[str]
    data: Optional[Union[Dict[str, Any], str, List[Dict[str, Any]]]] = {}
    agent: Optional[str] = None
    embeddings: Optional[List[int]] = []


class Log(MongoModel, LogBase):
    _collection_name = "logs"
