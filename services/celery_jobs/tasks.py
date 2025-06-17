
from loguru import logger

from lib.celery import celery_app
from repository import repository
from services.workflows import WorkflowService


@celery_app.task(bind=True, name="agents.hello")
def hello(self):
    print("hello world")


@celery_app.task(bind=True, name="workflows.run")
def run_workflow(
    self,
    workflow_id: str,
    payload: dict = None,
    source: str = "",
    source_log_id: str = None,
):
    """
    Run a specific workflow by its ID.
    This is a placeholder for the actual workflow execution logic.
    """
    workflow = repository.mongo.workflow.find_by_id(workflow_id)
    if not workflow:
        logger.error(f"Workflow with ID {workflow_id} not found.")
        return
    WorkflowService.run_workflow(
        workflow, payload, context={}, source=source, source_log_id=source_log_id
    )
    return
