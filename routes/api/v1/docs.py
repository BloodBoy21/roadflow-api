from fastapi import APIRouter, Depends

from helpers.auth import user_is_authenticated
from middleware.org_middleware import (
    validate_org_middleware,
    validate_user_verified_middleware,
)
from models.mongo.out_document import OutDocument
from models.response.api import PaginateResponse
from models.user import UserRead
from repository import repository

docs_router = APIRouter()


@docs_router.get("/{org_id}/{section}", response_model=PaginateResponse[OutDocument])
@validate_user_verified_middleware
@validate_org_middleware
async def get_docs(org_id: int, section: str,page:int=1,limit:int=20, user: UserRead = Depends(user_is_authenticated)):
    agent = ""
    match section:
      case "engineering":
        agent = "EngineerAgent"
      case "product":
        agent = "ProductAgent"
      case "operations":
        agent = "OperationsAgent"
      case "customer_success":
        agent = "CustomerSuccessAgent"
      case "growth":
        agent = "GrowthAgent"
      case _:
        agent = "default"
    docs,pages, total = repository.mongo.out_document.get_by_section(
        org_id=org_id, agent=agent, page=page, limit=limit
    )
    return {
        "data": docs,
        "pages": pages,
        "total": total,
    }
