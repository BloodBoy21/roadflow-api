from .base import MongoRepository
from models.mongo.changelog import Changelog, ChangelogBase


class ChangelogRepository(MongoRepository[Changelog]):
    """Repository for managing changelog in MongoDB."""

    def __init__(self):
        super().__init__(collection="changelogs", model=Changelog)
