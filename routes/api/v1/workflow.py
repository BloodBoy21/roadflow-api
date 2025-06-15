from fastapi import APIRouter, Depends, HTTPException
from helpers.auth import user_is_authenticated
from middleware.org_middleware import (
    validate_org_middleware,
    validate_user_verified_middleware,
)
from models.mongo.workflow import CreateWorkFlow, CreateWorkflowTask, Workflow
from models.user import UserRead
from repository import repository

workflow_router = APIRouter()


@workflow_router.post("/{org_id}/workflow", response_model=Workflow)
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
        return workflow
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@workflow_router.post("/{org_id}/workflow/task", response_model=Workflow)
@validate_user_verified_middleware
@validate_org_middleware
async def create_workflow_task(
    org_id: int,
    data: CreateWorkflowTask,
    user: UserRead = Depends(user_is_authenticated),
):
    try:
        workflow = repository.mongo.workflow.create_task(
            {**data.model_dump(), "organizationId": org_id, "created_by": user.id}
        )
        return workflow
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
