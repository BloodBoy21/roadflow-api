
from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger

from helpers.auth import user_is_authenticated
from helpers.webhook import generate_webhook_id
from middleware.org_middleware import (
    validate_org_middleware,
    validate_user_verified_middleware,
)
from models.input_webhook import InputWebhookCreate, InputWebhookRead
from models.invitation import InvitationCreate
from models.response.api import Response
from models.user import UserRead
from repository import repository
from services.organization_service import accept_invite, send_invite_to_org

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


@organization_router.post(
    "/{org_id}/invite",
    status_code=status.HTTP_201_CREATED,
)
@validate_user_verified_middleware
@validate_org_middleware
async def invite_user_to_organization(
    org_id: int,
    data: list[InvitationCreate],
    user: UserRead = Depends(user_is_authenticated),
):
    try:
        # Here you would typically process the data, e.g., update a database, trigger a build, etc.
        # For now, we just log it
        await send_invite_to_org(org_id, data)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@organization_router.get(
    "/invite/{token}",
    status_code=status.HTTP_200_OK,
)
@validate_user_verified_middleware
async def validate_invite_token(
    token: str,
    user: UserRead = Depends(user_is_authenticated),
):
    try:
        # Validate the invite token and return the invitation details
        await accept_invite(token, user.id)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=str(e)) from e
