from pydantic import BaseModel, SecretStr, Field, field_validator
from typing import Optional, List
from .integration import IntegrationRead
from .member import MemberRead
import re


class UserBase(BaseModel):
    first_name: str
    last_name: str
    avatar: Optional[str] = None
    email: str
    password: Optional[str] = None
    verified: Optional[bool] = False


class UserCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: Optional[str] = Field(default=None, max_length=50)
    email: str
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("password")
    def validate_password(cls, v):
        valid_password_regex = re.compile(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[a-zA-Z\d@$!%*?&]{8,}$"
        )
        if not valid_password_regex.match(v):
            raise ValueError(
                "Invalid password format (min 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 special character)"
            )
        return v

    @field_validator("email")
    def validate_email(cls, v):
        valid_email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if not valid_email_regex.match(v):
            raise ValueError("Invalid email format")
        return v


class UserOut(BaseModel):
    first_name: str
    last_name: str
    avatar: Optional[str] = None


class UserRead(UserBase):
    id: int
    integrations: Optional[List[IntegrationRead]] = []
    members: Optional[List[MemberRead]] = []
    password: Optional[SecretStr] = None
    is_admin: Optional[bool] = False

    class Config:
        from_attributes = True
