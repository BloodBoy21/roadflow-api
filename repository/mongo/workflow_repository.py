from .base import MongoRepository
from models.mongo.workflow import Workflow
from loguru import logger
from utils.object_id import ObjectId


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
        if event:
            pipeline[0]["$match"]["events"] = {"$in": [event]}
        logger.info(pipeline)
        raw_cursor = self.aggregate(pipeline)
        workflows = [self.model(**doc) for doc in raw_cursor]
        return workflows

    def get_workflow_nodes(self, workflow_id: str) -> list[Workflow]:
        """Get workflow nodes by workflow ID."""
        pipeline = pipeline = [
            {"$match": {"_id": ObjectId(workflow_id)}},
            {
                "$graphLookup": {
                    "from": "workflows",
                    "startWith": "$next_flow",
                    "connectFromField": "next_flow",
                    "connectToField": "_id",
                    "as": "linked_nodes",
                    "depthField": "depth",
                }
            },
            {
                "$addFields": {
                    "all_nodes": {"$concatArrays": [["$$ROOT"], "$linked_nodes"]}
                }
            },
            {"$unwind": "$all_nodes"},
            {"$replaceRoot": {"newRoot": "$all_nodes"}},
            {"$sort": {"depth": 1}},
            {
                "$lookup": {
                    "from": "tasks",
                    "localField": "task_template_id",
                    "foreignField": "_id",
                    "as": "task",
                }
            },
            {"$unwind": {"path": "$task", "preserveNullAndEmptyArrays": True}},
        ]
        raw_cursor = self.aggregate(pipeline)
        workflows = [self.model(**doc) for doc in raw_cursor]
        return workflows
