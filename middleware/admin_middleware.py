from middleware import Middleware
from fastapi import HTTPException, status
from models.user import UserRead


async def _validate_user_admin_middleware_(
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
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action",
        )
    return


validate_user_admin_middleware = Middleware(_validate_user_admin_middleware_)
