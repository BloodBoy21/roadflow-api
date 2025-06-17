import math
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field, model_validator

T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    success: bool = Field(default=True)
    data: T | None = Field(default=None)  # Use Optional for None default


class ErrorResponse(BaseModel):
    success: bool = Field(default=False)
    error: str | None = Field(default=None)
    data: Any | None = Field(default=None)


class PaginateResponse(BaseModel, Generic[T]):
    success: bool = Field(default=True)
    data: list[T] | T = Field(
        default_factory=list
    )  # Use default_factory for mutable types
    pages: int = Field(default=0)
    total: int = Field(default=0)


class PaginateQuery(BaseModel, Generic[T]):
    count: int = Field(default=0)
    pages: int = Field(default=1)
    data: list[T] = Field(default_factory=list)  # Use default_factory for mutable types
    limit: int = Field(default=10)

    @model_validator(mode="before")
    def calculate_pages(cls, values: dict):
        count = values.get("count", 0)
        limit = values.get("limit", 10)
        values["pages"] = math.ceil(count / limit) if limit > 0 else 1
        return values


class InvitationAccept(BaseModel):
    token: str
