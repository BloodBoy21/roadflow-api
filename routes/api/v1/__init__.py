from fastapi import APIRouter

from .agents import agents_router
from .docs import docs_router
from .git import git_router
from .organization import organization_router
from .users import user_router
from .workflow import workflow_router

v1_router = APIRouter()

v1_router.include_router(user_router, prefix="/user", tags=["user"])
v1_router.include_router(agents_router, prefix="/agents", tags=["agents"])
v1_router.include_router(git_router, prefix="/git", tags=["git"])
v1_router.include_router(
    organization_router, prefix="/organization", tags=["organization"]
)
v1_router.include_router(workflow_router, prefix="/workflow", tags=["workflow"])
v1_router.include_router(docs_router, prefix="/docs", tags=["docs"])

@v1_router.get("/")
async def root():
    return {"message": "Welcome to the API v1!"}
