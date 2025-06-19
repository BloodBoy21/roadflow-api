from models.mongo.task import Task, TaskBase

from .base import MongoRepository


class TaskRepository(MongoRepository[Task]):
    """Repository for managing Tasks in MongoDB."""

    def __init__(self):
        super().__init__(collection="tasks", model=Task)

    def get_all_tasks(self) -> list[TaskBase]:
        """
        Returns all tasks
        """
        tasks = self.find(query={})
        return list(tasks)
