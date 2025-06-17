from datetime import datetime
from typing import Any

from pydantic import BaseModel

from .mongo_base import MongoModel


class PlatformBase(BaseModel):
    platformId: int | None
    title: str | None
    organizationId: int | None
    configuration: dict[str, Any] | None
    enabled: bool | None
    createdAt: datetime | None
    updatedAt: datetime | None


class Platform(MongoModel, PlatformBase):
    _collection_name = "platform"
