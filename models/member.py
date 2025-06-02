from pydantic import BaseModel
from typing import Optional


class MemberBase(BaseModel):
    organization_id: int
    user_id: Optional[int] = None
    first_name: str
    last_name: str
    role: str
    role_description: Optional[str] = None
    gender: Optional[str] = None


class MemberCreate(MemberBase):
    pass


class MemberRead(MemberBase):
    id: int

    class Config:
        orm_mode = True
