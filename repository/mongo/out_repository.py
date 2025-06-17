from models.mongo.out_document import OutDocument

from .base import MongoRepository


class OutDocumentRepository(MongoRepository[OutDocument]):
    """Repository for managing ou\1_\2 in MongoDB."""

    def __init__(self):
        super().__init__(collection="outDocuments", model=OutDocument)
