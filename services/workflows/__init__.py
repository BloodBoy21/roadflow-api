from repository import repository
from models.mongo.workflow import Workflow
from typing import List, Optional, Dict
from loguru import logger
from services.agents import AgentCaller
import asyncio


class WorkflowService:
    def __init__(self, org_id: Optional[int] = None, event=str):
        """
        Initialize the WorkflowService with an optional organization ID.
        """
        self.org_id = org_id
        self.event = event

    def get_workflow(self) -> List[Workflow]:
        """
        Get all workflows for a given organization ID.
        """
        return repository.mongo.workflow.get_main_workflows_by_org_id(
            org_id=self.org_id, event=self.event
        )

    def run(self, payload: Dict = None):
        """
        Run a specific workflow by its ID.
        """
        from services.celery_jobs.tasks import run_workflow

        workflows = self.get_workflow()
        logger.info(
            f"Running workflows for organization ID {self.org_id} with event {self.event}: {len(workflows)} workflows found."
        )
        for workflow in workflows:
            logger.info(f"Running workflow: {workflow.id}")
            run_workflow.delay(workflow_id=str(workflow.id), payload=payload)

    @staticmethod
    def run_workflow(workflow: Workflow, payload: Dict, context: Dict = {}):
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
            return WorkflowService.run_task(workflow, payload=payload, context=context)
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
        
        Context: {context}
        
        Input data to analyze and process:
        {payload}
        
        """

        res = asyncio.run(agent_caller.generate(text=prompt))
        logger.info(f"Workflow {workflow.id} executed successfully: {res}")
        if not res:
            logger.error(f"Failed to run workflow: {workflow.id}")
            return
        if workflow.next_flow:
            next_workflow = repository.mongo.workflow.find_by_id(workflow.next_flow)
            if not context["prev_workflow"]:
                context["prev_workflow"] = []
            context["prev_workflow"].append(
                {
                    "workflow_id": str(workflow.id),
                    "result": res,
                }
            )
            payload["last_response"] = res
            return WorkflowService.run_workflow(
                next_workflow, payload=payload, context=context
            )
        return

    @staticmethod
    def run_task(workflow: Workflow, payload: Dict = {}, context: Dict = {}):
        """
        Run a specific workflow task
        This is a static method to allow running tasks without needing an instance.
        """
        return
