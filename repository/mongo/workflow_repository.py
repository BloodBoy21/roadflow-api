from loguru import logger

from lib.cache import get_cache
from models.mongo.workflow import Workflow
from utils.object_id import ObjectId

from .base import MongoRepository

EXP_CACHE_TIMEOUT = 60 * 60 * 1  # 1 hour``

cache = get_cache()


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

    def get_last_node_id(self, workflow_id: str) -> str | None:
        """Get the last node of a workflow chain starting at the given workflow ID."""
        pipeline = [
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
            {
                "$addFields": {
                    "sort_depth": {"$ifNull": ["$depth", -1]}  # root gets -1
                }
            },
            {"$sort": {"sort_depth": -1}},  # last node has highest depth
            {"$limit": 1},
        ]
        last_node_cache_key = f"workflow_last_node_{workflow_id}"
        last_node_id = cache.get(last_node_cache_key)
        if last_node_id:
            return ObjectId(last_node_id.decode("utf-8"))
        raw_cursor = self.aggregate(pipeline)
        doc = next(raw_cursor, None)
        if doc:
            last_node_id = str(doc["_id"])
            cache.set(last_node_cache_key, last_node_id, timeout=EXP_CACHE_TIMEOUT)
            return ObjectId(last_node_id)
        return None
