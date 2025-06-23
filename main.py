import os
from contextlib import asynccontextmanager
from typing import Union

import redis.asyncio as redis
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_limiter import FastAPILimiter
from loguru import logger

from helpers.auth import create_token
from helpers.error_handling import raise_server_error
from lib.cache import get_cache
from lib.mongo import client as mongo_client
from lib.prisma import prisma
from models.inputs.api import UserLogin
from models.response.api import ErrorResponse, Response
from models.response.auth import AuthResponse
from models.user import UserCreate
from routes.api import api_router
from services import user_service

origins = os.getenv("CORS_ORIGINS", "*").split(",")
print(f"Origins: {origins}")

is_production = ["prod", "production"].count(os.getenv("ENV", "dev")) > 0


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up")
    logger.info("Setting up cache")
    await prisma.connect()
    logger.info("Setting up prisma")
    cache = get_cache()
    logger.info(f"Cache: {cache.ping()}")
    redis_connection = redis.from_url(
        os.getenv("REDIS_URI", "redis://localhost:6379"),
        encoding="utf-8",
        decode_responses=True,
    )
    await FastAPILimiter.init(redis_connection)
    yield
    mongo_client.close()
    logger.info("Shutting down")
    await FastAPILimiter.close()


app = FastAPI(
    title="RoadFlow API",
    description="API for RoadFlow",
    version="0.1",
    lifespan=lifespan,
    docs_url="/docs" if not is_production else None,
    redoc_url="/redoc" if not is_production else None,
    openapi_url="/openapi.json" if not is_production else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix="/api", tags=["api"])


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post(
    "/signup",
    response_model=Union[Response[AuthResponse], ErrorResponse],
    tags=["auth"],
)
async def signup(user: UserCreate):
    """Endpoint to create a new user."""
    try:
        created_user = await user_service.create_user(user)
        token = create_token(user_id=created_user.id)
        user_service.send_validation_email(created_user)
        return {
            "data": {
                **created_user.model_dump(),
                "access_token": token,
            }
        }
    except ValueError as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.exception("Unexpected error during user signup")
        raise_server_error(
            e,
            "An unexpected error occurred during user signup.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@app.post(
    "/auth", response_model=Union[Response[AuthResponse], ErrorResponse], tags=["auth"]
)
async def auth(user_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_service.login_user(
        UserLogin(
            email=user_data.username,
            password=user_data.password,
        )
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )
    token = create_token(user.id)
    return {"access_token": token, "token_type": "bearer"}





@app.post(
    "/login", response_model=Union[Response[AuthResponse], ErrorResponse], tags=["auth"]
)
async def login(user: UserLogin):
    """Endpoint to log in a user."""
    try:
        logged_in_user = await user_service.login_user(user)
        token = create_token(user_id=logged_in_user.id)
        return {
            "data": {
                **logged_in_user.model_dump(),
                "access_token": token,
            }
        }
    except ValueError as e:
        logger.error(f"Error logging in user: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        ) from e
    except Exception as e:
        logger.exception("Unexpected error during user login")
        raise_server_error(
            e,
            "An unexpected error occurred during user login.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


if __name__ == "__main__":
    import dotenv
    import uvicorn

    env = os.getenv("ENV", "dev")
    print(f"env:{env}")
    reload = env == "dev"
    if reload:
        dotenv.load_dotenv(verbose=True)
    app = "main:app" if reload else app
    port = os.getenv("PORT", 3000)
    uvicorn.run(app, host="0.0.0.0", port=int(port), reload=reload)
