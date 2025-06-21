from venv import logger

from fastapi import APIRouter, Depends, HTTPException, status

from helpers.auth import user_is_authenticated
from lib.cache import get_cache
from middleware.admin_middleware import validate_user_admin_middleware
from middleware.org_middleware import (
    validate_org_middleware,
    validate_user_verified_middleware,
)
from middleware.workflow_middleware import validate_workflow_middleware
from models.mongo.task import TaskCreate, TaskOutput
from models.mongo.workflow import CreateWorkFlow, CreateWorkflowTask, Workflow
from models.response.api import Response
from models.user import UserRead
from repository import repository

cache = get_cache()
workflow_router = APIRouter()


@workflow_router.post("/{org_id}/workflow", response_model=Response[Workflow])
@validate_user_verified_middleware
@validate_org_middleware
async def create_workflow(
    org_id: int,
    data: CreateWorkFlow,
    head_node: str = None,
    user: UserRead = Depends(user_is_authenticated),
):
    try:
        last_node = None
        if head_node:
            last_node = repository.mongo.workflow.get_last_node_id(
                workflow_id=head_node
            )
            if not last_node:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Head node not found"
                )
        workflow = repository.mongo.workflow.create(
            {
                **data.model_dump(),
                "is_head": not bool(head_node),
                "organizationId": org_id,
                "created_by": user.id,
                "enabled": True,
                "next_flow": None,
            }
        )
        if head_node:
            repository.mongo.workflow.update_by_id(
                id=head_node,
                data={"next_flow": workflow.id},
            )
        cache.delete(f"workflow_last_node_{head_node}")
        return {
            "data": workflow,
        }
    except Exception as e:
        logger.error(f"Error creating workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@workflow_router.post("/{org_id}/workflow/task", response_model=Response[Workflow])
@validate_user_verified_middleware
@validate_org_middleware
@validate_workflow_middleware
async def create_workflow_task(
    org_id: int,
    data: CreateWorkflowTask,
    head_node: str = None,
    user: UserRead = Depends(user_is_authenticated),
):
    try:
        last_node = None
        if head_node:
            last_node = repository.mongo.workflow.get_last_node_id(
                workflow_id=head_node
            )
            if not last_node:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Head node not found"
                )
        workflow = repository.mongo.workflow.create(
            {
                **data.model_dump(),
                "organizationId": org_id,
                "created_by": user.id,
                "is_task": True,
                "enabled": True,
                "next_flow": None,
            }
        )
        if head_node:
            repository.mongo.workflow.update_by_id(
                id=head_node,
                data={"next_flow": workflow.id},
            )
        cache.delete(f"workflow_last_node_{head_node}")
        return {
            "data": workflow,
        }
    except Exception as e:
        logger.error(f"Error creating workflow task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@workflow_router.post(
    "/task", status_code=status.HTTP_201_CREATED, response_model=Response[TaskOutput]
)
@validate_user_verified_middleware
@validate_user_admin_middleware
async def create_task(
    data: TaskCreate,
    user: UserRead = Depends(user_is_authenticated),
):
    try:
        task = repository.mongo.task.create(data=data)
        return {
            "data": task,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@workflow_router.get(
    "/task/all",
    response_model=Response[list[TaskOutput]],
)
async def get_all_tasks(
    user: UserRead = Depends(user_is_authenticated),
):
    try:
        tasks = repository.mongo.task.get_all_tasks()
        return {
            "data": tasks,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@workflow_router.get(
    "/{org_id}",
    response_model=Response[list[Workflow]],
)
@validate_user_verified_middleware
@validate_org_middleware
async def get_workflows(
    org_id: int,
    user: UserRead = Depends(user_is_authenticated),
):
    try:
        workflows: list[Workflow] = (
            repository.mongo.workflow.get_main_workflows_by_org_id(org_id=org_id)
        )
        return {
            "data": workflows,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@workflow_router.get(
    "/{org_id}/nodes/{workflow_id}",
    response_model=Response[list[Workflow]],
)
@validate_user_verified_middleware
@validate_org_middleware
@validate_workflow_middleware
async def get_workflow_nodes(
    org_id: int,
    workflow_id: str,
    user: UserRead = Depends(user_is_authenticated),
):
    try:
        workflows: list[Workflow] = repository.mongo.workflow.get_workflow_nodes(
            workflow_id=workflow_id
        )

        return {
            "data": workflows,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@workflow_router.patch(
    "/{org_id}/node/{node_id}",
    response_model=Response[Workflow],
)
@validate_user_verified_middleware
@validate_org_middleware
@validate_workflow_middleware
async def update_workflow_node(
    org_id: int,
    node_id: str,
    data: CreateWorkflowTask | CreateWorkFlow,
    user: UserRead = Depends(user_is_authenticated),
):
    try:
        workflow = repository.mongo.workflow.update_by_id(id=node_id, data=data)
        return {
            "data": workflow,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@workflow_router.delete(
    "/{org_id}/node/{node_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@validate_user_verified_middleware
@validate_org_middleware
@validate_workflow_middleware
async def delete_workflow_node(
    org_id: int,
    node_id: str,
    user: UserRead = Depends(user_is_authenticated),
):
    try:
        [current, before_node, next_node] = (
            repository.mongo.workflow.get_chains_of_node(node_id=node_id)
        )
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Workflow node not found"
            )
        if before_node:
            repository.mongo.workflow.update_by_id(
                id=before_node.id,
                data={"next_flow": next_node.id if next_node else None},
            )
        repository.mongo.workflow.delete_by_id(id=node_id)
        cache.delete(f"workflow_last_node_{node_id}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@workflow_router.delete(
    "/{org_id}/workflow/{workflow_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@validate_user_verified_middleware
@validate_org_middleware
@validate_workflow_middleware
async def delete_workflow(
    org_id: int,
    workflow_id: str,
    user: UserRead = Depends(user_is_authenticated),
):
    try:
        workflow: Workflow = repository.mongo.workflow.find_by_id(workflow_id)
        if not workflow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found"
            )
        if not workflow.is_head:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only head workflows can be deleted",
            )
        repository.mongo.workflow.delete_workflow(id=workflow_id)
        cache.delete(f"workflow_last_node_{workflow_id}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
