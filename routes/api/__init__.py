from fastapi import APIRouter

from routes.api.v1 import v1_router

api_router = APIRouter()

api_router.include_router(v1_router, prefix="/v1", tags=["v1"])
