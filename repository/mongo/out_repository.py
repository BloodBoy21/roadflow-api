from models.mongo.out_document import OutDocument

from .base import MongoRepository


class OutDocumentRepository(MongoRepository[OutDocument]):
    """Repository for managing out documents in MongoDB."""

    def __init__(self):
        super().__init__(collection="outDocuments", model=OutDocument)

    def get_by_section(
        self, org_id: int, agent: str, page: int = 1, limit: int = 20
    ) -> tuple[list[OutDocument], int, int]:
        """
        Retrieve documents by section with pagination.

        Args:
            org_id (int): Organization ID.
            section (str): Section to filter documents.
            page (int): Page number for pagination.
            limit (int): Number of documents per page.

        Returns:
            tuple: List of documents, total pages, and total count.
        """
        query = {"organizationId": org_id, "agent": agent}
        return self.paginate(query=query, page=page, limit=limit)
