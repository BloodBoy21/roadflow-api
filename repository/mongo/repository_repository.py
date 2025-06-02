from .base import MongoRepository
from models.mongo.repository import Repository, RepositoryBase


class RepositoryRepository(MongoRepository[Repository]):
    """Repository for managing repository in MongoDB."""

    def __init__(self):
        super().__init__(collection="repositories", model=Repository)
