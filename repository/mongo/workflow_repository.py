from .base import MongoRepository
from models.mongo.workflow import Workflow, WorkflowBase


class WorkflowRepository(MongoRepository[Workflow]):
    """Repository for managing workflows in MongoDB."""

    def __init__(self):
        super().__init__(collection="workflows", model=Workflow)
