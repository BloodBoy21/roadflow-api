from datetime import datetime

from pydantic import BaseModel

from .mongo_base import MongoModel


class ChangelogBase(BaseModel):
    organizationId: int
    title: str
    description: str
    position: int
    show: bool
    estimated_date: datetime | None = None


class Changelog(MongoModel, ChangelogBase):
    _collection_name = "changelog"
