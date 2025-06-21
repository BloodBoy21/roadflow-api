
from pydantic import BaseModel


class PlatformBase(BaseModel):
    name: str
    description: str | None = None


class PlatformCreate(PlatformBase):
    pass


class PlatformRead(PlatformBase):
    id: int

