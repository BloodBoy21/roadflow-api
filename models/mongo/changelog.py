from datetime import datetime

from pydantic import BaseModel

from .mongo_base import MongoModel


class ChangelogBase(BaseModel):
    organizationId: int
    title: str
    description: str
    position: int
    show: bool
    createdAt: datetime
    updatedAt: datetime


class Changelog(MongoModel, ChangelogBase):
    _collection_name = "changelog"
