from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from .mongo_base import MongoModel


class PlatformBase(BaseModel):
    platformId: Optional[int]
    title: Optional[str]
    organizationId: Optional[int]
    configuration: Optional[Dict[str, Any]]
    enabled: Optional[bool]
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]


class Platform(MongoModel, PlatformBase):
    _collection_name = "platform"
