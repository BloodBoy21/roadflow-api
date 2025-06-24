from fastapi import HTTPException, status

from middleware import Middleware
from models.organization_user import OrganizationUserRead
from models.user import UserRead
from repository import repository


async def _can_access_to_resource(
    allowed_roles: list[str],
    user: UserRead = None,
    org_id: int | None = None,
    *args,
    **kwargs,
):
    user_id = user.id
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    if not allowed_roles:
      return
    if not org_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization ID is required",
        )
    is_member = await repository.sql.organization_user.user_in_organization(
        user_id=user_id, organization_id=org_id
    )
    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )
    org_user: OrganizationUserRead = await repository.sql.organization_user.get_user_by_id_and_organization_id(
        user_id=user_id, organization_id=org_id
    )
    if org_user.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )
    return


def user_has_permission(allowed_roles: list[str]):
    def middleware_callback(*args, **kwargs):
        return _can_access_to_resource(*args, **kwargs,allowed_roles=allowed_roles, )

    return Middleware(middleware_callback)
