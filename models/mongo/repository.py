from datetime import datetime

from pydantic import BaseModel

from .mongo_base import MongoModel


class RepositoryBase(BaseModel):
    integrationId: int
    organizationId: int
    type: str
    name: str | None
    description: str | None
    gitId: str | None
    createdAt: datetime | None
    updatedAt: datetime | None


class Repository(MongoModel, RepositoryBase):
    _collection_name = "repositories"
