from fastapi import APIRouter
from .users import user_router
from .agents import agents_router

v1_router = APIRouter()

v1_router.include_router(user_router, prefix="/user", tags=["user"])
v1_router.include_router(agents_router, prefix="/agents", tags=["agents"])


@v1_router.get("/")
async def root():
    return {"message": "Welcome to the API v1!"}
