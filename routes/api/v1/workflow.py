from fastapi import APIRouter, Depends, HTTPException, status
from helpers.auth import user_is_authenticated
from middleware.org_middleware import (
    validate_org_middleware,
    validate_user_verified_middleware,
)
from models.mongo.workflow import CreateWorkFlow, CreateWorkflowTask, Workflow
from models.user import UserRead
from repository import repository
from models.mongo.task import TaskOutput, TaskCreate
from models.response.api import Response
from middleware.admin_middleware import validate_user_admin_middleware

workflow_router = APIRouter()


@workflow_router.post("/{org_id}/workflow", response_model=Response[Workflow])
@validate_user_verified_middleware
@validate_org_middleware
async def create_workflow(
    org_id: int,
    data: CreateWorkFlow,
    user: UserRead = Depends(user_is_authenticated),
):
    try:
        workflow = repository.mongo.workflow.create(
            {**data.model_dump(), "organizationId": org_id, "created_by": user.id}
        )
        return {
            "data": workflow,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@workflow_router.post("/{org_id}/workflow/task", response_model=Response[Workflow])
@validate_user_verified_middleware
@validate_org_middleware
async def create_workflow_task(
    org_id: int,
    data: CreateWorkflowTask,
    user: UserRead = Depends(user_is_authenticated),
):
    try:
        workflow = repository.mongo.workflow.create(
            {**data.model_dump(), "organizationId": org_id, "created_by": user.id}
        )
        return {
            "data": workflow,
        }
    except Exception as e:
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
