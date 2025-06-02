from .base import MongoRepository
from models.mongo.knowledge import Knowledge, KnowledgeBase


class KnowledgeRepository(MongoRepository[Knowledge]):
    """Repository for managing knowledge in MongoDB."""

    def __init__(self):
        super().__init__(collection="knowledge", model=Knowledge)
