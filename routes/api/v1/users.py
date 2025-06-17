from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger

import services.user_service as user_service
import services.user_service.organization as user_org_service
from helpers.auth import user_is_authenticated
from models.organization_user import OrganizationUserRead
from models.user import UserRead

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
