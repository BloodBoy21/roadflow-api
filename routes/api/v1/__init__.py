from fastapi import APIRouter

v1_router = APIRouter()


@v1_router.get("/")
async def root():
    return {"message": "Welcome to the API v1!"}
