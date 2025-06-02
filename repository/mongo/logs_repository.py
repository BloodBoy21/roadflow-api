from .base import MongoRepository
from models.mongo.logs import Log, LogBase


class LogsRepository(MongoRepository[Log]):
    """Repository for managing logs in MongoDB."""

    def __init__(self):
        super().__init__(collection="logs", model=Log)
