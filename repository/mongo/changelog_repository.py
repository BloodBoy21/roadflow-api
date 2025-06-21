from models.mongo.changelog import Changelog

from .base import MongoRepository


class ChangelogRepository(MongoRepository[Changelog]):
    """Repository for managing changelog in MongoDB."""

    def __init__(self):
        super().__init__(collection="changelogs", model=Changelog)

    def get_changelogs(
        self, org_id: int, page: int = 1, limit: int = 20
    ) -> tuple[list[Changelog], int, int]:
        """
        Retrieve changelogs for an organization with pagination.

        Args:
            org_id (int): Organization ID.
            page (int): Page number for pagination.
            limit (int): Number of changelogs per page.

        Returns:
            tuple: List of changelogs, total pages, and total count.
        """
        query = {"organizationId": org_id}
        return self.paginate(
            query=query, page=page, limit=limit, options={"sort": [("position", 1)]}
        )
