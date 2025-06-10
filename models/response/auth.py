from pydantic import BaseModel
from models.user import UserOut


class AuthResponse(UserOut):
    """Response model for authentication operations."""

    access_token: str
    token_type: str = "bearer"


class UserToken(BaseModel):
    user_id: int
    exp: int
