from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger

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
    try:
        changelogs, pages, total = repository.mongo.changelog.get_changelogs(
            org_id=org_id, page=page, limit=limit
        )
        return {
            "data": changelogs,
            "total": total,
            "pages": pages,
        }
    except Exception as e:
        logger.error(f"Error fetching changelogs for org_id {org_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching changelogs: {str(e)}",
        ) from e
