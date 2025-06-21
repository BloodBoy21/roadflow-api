from models.mongo.out_document import OutDocument

from .base import MongoRepository


class OutDocumentRepository(MongoRepository[OutDocument]):
    """Repository for managing out documents in MongoDB."""

    def __init__(self):
        super().__init__(collection="outDocuments", model=OutDocument)
