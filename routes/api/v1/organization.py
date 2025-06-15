from fastapi import APIRouter, Depends, HTTPException
from models.input_webhook import InputWebhookCreate, InputWebhookRead
from repository import repository
from models.response.api import Response
from helpers.auth import user_is_authenticated
from middleware.org_middleware import (
    validate_org_middleware,
    validate_user_verified_middleware,
)
from models.user import UserRead
from helpers.webhook import generate_webhook_id

organization_router = APIRouter()


@organization_router.post(
    "/{org_id}/webhook/input", response_model=Response[InputWebhookRead]
)
@validate_user_verified_middleware
@validate_org_middleware
async def create_webhook_input(
    org_id: int,
    data: InputWebhookCreate,
    user: UserRead = Depends(user_is_authenticated),
):
    try:
        # Here you would typically process the data, e.g., update a database, trigger a build, etc.
        # For now, we just log it
        webhook_id = generate_webhook_id()
        webhook = await repository.sql.input_webhook.create(
            {**data.model_dump(), "org_id": org_id, "key": webhook_id}
        )
        return {
            "data": webhook,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@organization_router.delete(
    "/{org_id}/webhook/input/{webhook_id}",
    status_code=204,
)
@validate_user_verified_middleware
@validate_org_middleware
async def delete_webhook_input(
    org_id: int,
    webhook_id: str,
    user: UserRead = Depends(user_is_authenticated),
):
    try:
        # Here you would typically process the data, e.g., update a database, trigger a build, etc.
        # For now, we just log it
        await repository.sql.input_webhook.delete({"id": webhook_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
