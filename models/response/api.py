from pydantic import BaseModel, Field, model_validator
from typing import Generic, TypeVar, Any, List, Optional, Union
import math

T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    success: bool = Field(default=True)
    data: Optional[T] = Field(default=None)  # Use Optional for None default


class ErrorResponse(BaseModel):
    success: bool = Field(default=False)
    error: Optional[str] = Field(default=None)
    data: Optional[Any] = Field(default=None)


class PaginateResponse(BaseModel, Generic[T]):
    success: bool = Field(default=True)
    data: Union[List[T], T] = Field(
        default_factory=list
    )  # Use default_factory for mutable types
    pages: int = Field(default=0)
    total: int = Field(default=0)


class PaginateQuery(BaseModel, Generic[T]):
    count: int = Field(default=0)
    pages: int = Field(default=1)
    data: List[T] = Field(default_factory=list)  # Use default_factory for mutable types
    limit: int = Field(default=10)

    @model_validator(mode="before")
    def calculate_pages(cls, values: dict):
        count = values.get("count", 0)
        limit = values.get("limit", 10)
        values["pages"] = math.ceil(count / limit) if limit > 0 else 1
        return values


class InvitationAccept(BaseModel):
    token: str
