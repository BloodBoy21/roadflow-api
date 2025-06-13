from .base import MongoRepository
from models.mongo.workflow import Workflow
from loguru import logger


class WorkflowRepository(MongoRepository[Workflow]):
    """Repository for managing workflows in MongoDB."""

    def __init__(self):
        super().__init__(collection="workflows", model=Workflow)

    def get_main_workflows_by_org_id(
        self, org_id: int, event: str = ""
    ) -> list[Workflow]:
        """Get main workflows by organization ID."""
        pipeline = [
            {
                "$match": {
                    "organizationId": org_id,
                    "is_head": True,
                    "enabled": True,
                    "events": {"$in": [event] if event else [""]},
                }
            },
            {
                "$lookup": {
                    "from": "workflows",
                    "localField": "next_flow",
                    "foreignField": "_id",
                    "as": "next_workflow",
                }
            },
        ]
        logger.info(pipeline)
        raw_cursor = self.aggregate(pipeline)
        workflows = [self.model(**doc) for doc in raw_cursor]
        return workflows
