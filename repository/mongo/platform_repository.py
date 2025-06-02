from .base import MongoRepository
from models.mongo.platform import Platform, PlatformBase


class PlatformRepository(MongoRepository[Platform]):
    """Repository for managing platform in MongoDB."""

    def __init__(self):
        super().__init__(collection="platforms", model=Platform)
