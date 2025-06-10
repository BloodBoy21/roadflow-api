from pydantic import BaseModel
from typing import Optional


class PlatformBase(BaseModel):
    name: str
    description: Optional[str] = None


class PlatformCreate(PlatformBase):
    pass


class PlatformRead(PlatformBase):
    id: int

    class Config:
        from_attributes = True
