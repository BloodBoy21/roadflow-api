from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .mongo_base import MongoModel


class RepositoryBase(BaseModel):
    integrationId: int
    organizationId: int
    type: str
    name: Optional[str]
    description: Optional[str]
    gitId: Optional[str]
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]


class Repository(MongoModel, RepositoryBase):
    _collection_name = "repositories"
