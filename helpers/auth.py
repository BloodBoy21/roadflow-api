import jwt
from datetime import datetime, timedelta
import os
from loguru import logger
from fastapi import HTTPException, status, Depends
from models.user import UserRead as User
from models.response.auth import UserToken
from fastapi.security import OAuth2PasswordBearer
from typing import Union
from repository import repository

SECRET_KEY = os.getenv("SECRET_TOKEN_KEY")
EXP_TIME = int(os.getenv("EXP_TOKEN_TIME_IN_DAYS", 7))  # Default to 7 days if not set

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")


def create_token(user_id) -> str:
    return jwt.encode(
        {"user_id": user_id, "exp": datetime.now() + timedelta(days=EXP_TIME)},
        SECRET_KEY,
        algorithm="HS256",
    )


def decode_token(token) -> Union[UserToken, None]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None


async def user_is_authenticated(token: str = Depends(oauth2_scheme)) -> User:
    try:
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        payload = decode_token(token)
        logger.info(f"Decoded token: {payload}")
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        payload: UserToken = UserToken(**payload)
        logger.info(f"Decoded token payload: {payload}")
        user: User = await repository.sql.user.get_by_id(id=payload.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        ) from None
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        ) from None
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        ) from e
    return user
