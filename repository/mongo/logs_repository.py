from models.mongo.logs import Log

from .base import MongoRepository


class LogsRepository(MongoRepository[Log]):
    """Repository for managing logs in MongoDB."""

    def __init__(self):
        super().__init__(collection="logs", model=Log)

    def get_by_organization_id(
        self, organization_id: int, limit: int = 20, page: int = 1
    ) -> tuple[list[Log], int, int]:
        """Get logs by organization ID with pagination."""
        pipeline = [
            {
                "$match": {
                    "organizationId": organization_id,
                }
            },
            {
                "$lookup": {
                    "from": "logs",
                    "localField": "source_id",
                    "foreignField": "_id",
                    "as": "source_event",
                }
            },
            {
                "$sort": {"_id": -1}  # Sort by _id in descending order
            },
            {
                "$skip": (page - 1) * limit
            },
            {
                "$limit": limit
            }
        ]
        cursor = self.aggregate(pipeline)
        logs = list(cursor)
        total = self.count({"organizationId": organization_id})
        pages = (total + limit - 1) // limit  # Calculate total pages
        return logs, pages, total
