from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger

import services.user_service as user_service
import services.user_service.organization as user_org_service
from helpers.auth import user_is_authenticated, decode_email_token
from models.organization_user import OrganizationUserRead
from models.user import UserRead
from helpers.error_handling import raise_server_error
from typing import Union
from models.response.auth import AuthResponse
from models.response.api import ErrorResponse, Response
user_router = APIRouter()


@user_router.get(
    "/organizations",
    response_model=list[OrganizationUserRead],
    status_code=status.HTTP_200_OK,
)
async def get_user_organizations(user: UserRead = Depends(user_is_authenticated)):
    """
    Get all organizations the user is a member of.
    """
    try:
        organizations = await user_org_service.get_user_organizations(user_id=user.id)
        return organizations
    except Exception as e:
        logger.error(f"Error retrieving user organizations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e


@user_router.post(
    "/send-validation-email",
    status_code=status.HTTP_200_OK,
)
async def send_validation_email(user: UserRead = Depends(user_is_authenticated)):
    """
    Send a validation email to the user.
    """
    try:
        await user_service.send_validation_email(user)
    except Exception as e:
        logger.error(f"Error sending validation email: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e

@user_router.get(
    "/verify",
    response_model=Union[Response[AuthResponse], ErrorResponse],
    tags=["auth"],
)
async def verify_email(token: str):
    """Endpoint to verify a user's email."""
    try:
        payload: dict = decode_email_token(token)
        if not payload:
            raise ValueError("Invalid or expired token")
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired token",
            )
        user: UserRead = await user_service.verify_user_email(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return {
            "data": {
                **user.model_dump(),
                "message": "Email verified successfully",
            }
        }
    except ValueError as e:
        logger.error(f"Error verifying email: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.exception("Unexpected error during email verification")
        raise_server_error(
            e,
            "An unexpected error occurred during email verification.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )