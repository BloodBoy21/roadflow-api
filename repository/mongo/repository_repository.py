from models.mongo.repository import Repository

from .base import MongoRepository


class RepositoryRepository(MongoRepository[Repository]):
    """Repository for managing repository in MongoDB."""

    def __init__(self):
        super().__init__(collection="repositories", model=Repository)
