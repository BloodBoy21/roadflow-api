from middleware import Middleware
from fastapi import HTTPException, status
from repository import repository
from typing import Optional
from models.user import UserRead


async def _validate_org_middleware_(
    org_id: Optional[int] = None,
    orgId: Optional[int] = None,
    user: UserRead = None,
    **kwargs,
):
    """
    Middleware for validating account.
    """
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    org_id = org_id or orgId
    if not org_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization ID is required",
        )
    is_member = await repository.sql.organization_user.user_in_organization(
        user_id=user.id, organization_id=org_id
    )
    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )
    return


async def _validate_user_confirmed_middleware_(
    user: UserRead = None,
    **kwargs,
):
    """
    Middleware for validating if the user is confirmed.
    """
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    if not user.verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not confirmed",
        )
    return


validate_org_middleware = Middleware(_validate_org_middleware_)
validate_user_verified_middleware = Middleware(_validate_user_confirmed_middleware_)
