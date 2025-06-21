import asyncio
import json
from typing import Dict, List, Optional

from loguru import logger

from models.mongo.logs import LogBase
from models.mongo.workflow import Workflow
from repository import repository
from services.agents import AgentCaller
from utils.object_id import ObjectId

from .tasks import run_task


class WorkflowService:
    def __init__(self, org_id: int | None = None, event=str):
        """
        Initialize the WorkflowService with an optional organization ID.
        """
        self.org_id = org_id
        self.event = event

    def get_workflow(self) -> list[Workflow]:
        """
        Get all workflows for a given organization ID.
        """
        return repository.mongo.workflow.get_main_workflows_by_org_id(
            org_id=self.org_id, event=self.event
        )

    def run(self, payload: dict = None):
        """
        Run a specific workflow by its ID.
        """
        from services.celery_jobs.tasks import run_workflow

        log = repository.mongo.logs.create(
            LogBase(
                organizationId=self.org_id,
                type="input",
                source=self.event,
                data=payload or {},
            )
        )
        workflows = self.get_workflow()
        logger.info(
            f"Running workflows for organization ID {self.org_id} with event {self.event}: {len(workflows)} workflows found."
        )
        for workflow in workflows:
            logger.info(f"Running workflow: {workflow.id}")
            run_workflow.delay(
                workflow_id=str(workflow.id),
                payload=payload,
                source=self.event,
                source_log_id=str(log.id),
            )

    @staticmethod
    def run_workflow(
        workflow: Workflow,
        payload: dict,
        context: dict = {},
        source: str = "",
        source_log_id: str | None = None,
    ):
        """
        Run a specific workflow
        This is a static method to allow running workflows without needing an instance.
        """
        if not isinstance(workflow, Workflow):
            raise TypeError(
                f"Expected an instance of Workflow, got {type(workflow).__name__}"
            )
        if not workflow.enabled:
            logger.warning(
                f"Workflow {workflow.id} is not enabled. Skipping execution."
            )
            return
        if workflow.is_task:
            return WorkflowService.run_task(
                workflow,
                payload=payload,
                context=context,
                source=source,
                source_log_id=source_log_id,
            )
        agent_caller = AgentCaller.create(
            org_id=workflow.organizationId, agent=workflow.agent
        )
        if not agent_caller:
            logger.error(
                f"Agent {workflow.agent} not found for organization ID {workflow.organizationId}"
            )
            return
        prompt = f"""
        ## Workflow Execution Prompt
        You are an AI agent responsible for executing workflows based on the provided context and input data.
        Your task is to analyze the input data, process it according to the workflow's logic, and return the result.
        Ensure that you follow the workflow's steps and utilize the context provided to make informed decisions.
        
        ## Workflow Details
        User prompt: {workflow.prompt}
        
        Context: {json.dumps(context, indent=2)}
        
        Input data to analyze and process:
        {json.dumps(payload, indent=2)}
        
        """

        res = asyncio.run(agent_caller.generate(text=prompt))
        logger.info(f"Workflow {workflow.id} executed successfully: {res}")
        repository.mongo.logs.create(
            LogBase(
                agent=workflow.agent,
                data=json.dumps(payload, indent=2) if isinstance(res, dict) else res,
                organizationId=workflow.organizationId,
                type="workflow",
                source=source or "workflow_run",
                source_id=ObjectId(source_log_id) if source_log_id else None,
            )
        )
        if not res:
            logger.error(f"Failed to run workflow: {workflow.id}")
            return
        context["last_response"] = res
        if workflow.next_flow:
            next_workflow = repository.mongo.workflow.find_by_id(workflow.next_flow)
            if not context.get("prev_workflow"):
                context["prev_workflow"] = []
            context["prev_workflow"].append(
                {
                    "workflow_id": str(workflow.id),
                    "result": res,
                }
            )
            return WorkflowService.run_workflow(
                next_workflow,
                payload=payload,
                context=context,
                source=source,
                source_log_id=source_log_id,
            )
        return

    @staticmethod
    def run_task(
        workflow: Workflow,
        payload: dict = {},
        context: dict = {},
        source: str = "",
        source_log_id: str | None = None,
    ):
        """
        Run a specific workflow task
        This is a static method to allow running tasks without needing an instance.
        """
        task_template = repository.mongo.task.find_by_id(workflow.task_template_id)
        if not task_template:
            logger.error(
                f"Task template {workflow.task_template_id} not found for workflow {workflow.id}"
            )
            return
        logger.info(f"Running task {task_template.id} for workflow {workflow.id}")
        result = run_task(
            task_name=task_template.function_name,
            payload=workflow.parameters or payload,
            context=context,
            source=source,
            source_log_id=source_log_id,
        )
        logger.info(
            f"Task {task_template.id} executed successfully for workflow {workflow.id}"
        )
        repository.mongo.logs.create(
            LogBase(
                agent=workflow.agent,
                data=json.dumps(result, indent=2)
                if isinstance(result, dict)
                else result,
                organizationId=workflow.organizationId,
                type="task",
                source=source or "task_run",
                source_id=ObjectId(source_log_id) if source_log_id else None,
            )
        )
        context["last_response"] = result
        if workflow.next_flow:
            next_workflow = repository.mongo.workflow.find_by_id(workflow.next_flow)
            if not context.get("prev_workflow"):
                context["prev_workflow"] = []
            context["prev_workflow"].append(
                {
                    "workflow_id": str(workflow.id),
                    "result": json.dumps(result, indent=2)
                    if isinstance(result, dict)
                    else result,
                }
            )
            return WorkflowService.run_workflow(
                next_workflow,
                payload=payload,
                context=context,
                source=source,
                source_log_id=source_log_id,
            )
        return
