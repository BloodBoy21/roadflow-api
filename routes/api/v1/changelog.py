from fastapi import APIRouter, Depends

from helpers.auth import user_is_authenticated
from middleware.org_middleware import (
    validate_org_middleware,
    validate_user_verified_middleware,
)
from models.mongo.changelog import Changelog
from models.response.api import PaginateResponse
from models.user import UserRead
from repository import repository

changelog_router = APIRouter()

@changelog_router.get(
    "/{org_id}",
    response_model=PaginateResponse[Changelog],
)
@validate_user_verified_middleware
@validate_org_middleware
async def get_changelog(org_id: int,page:int=1,limit:int=20, user: UserRead = Depends(user_is_authenticated)):
    changelogs,pages,total = await repository.mongo.changelog.get_changelogs(org_id=org_id, page=page, limit=limit)
    return {
      "data": changelogs,
      "total": total,
      "pages": pages,
    }
