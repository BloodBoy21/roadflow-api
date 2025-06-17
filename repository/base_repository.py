from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T], ABC):
    """Abstract base repository that defines the common interface for all repositories."""

    @abstractmethod
    def __init__(self, collection: str, model: type[T]):
        """Initialize the repository with a collection name and model type."""
        pass

    @abstractmethod
    def create(self, data: T | dict, options: dict = {}) -> T | None:
        """Create a new document/record in the database."""
        pass

    @abstractmethod
    def find(self, query: dict, options: dict = {}) -> list[T]:
        """Find documents/records matching the query."""
        pass

    @abstractmethod
    def find_one(self, query: dict, options: dict = {}) -> T | None:
        """Find a single document/record matching the query."""
        pass

    @abstractmethod
    def update(
        self, query: dict, data: T | dict, options: dict = {}
    ) -> T | None:
        """Update documents/records matching the query."""
        pass

    @abstractmethod
    def delete(self, query: dict = {}) -> Any:
        """Delete a document/record matching the query."""
        pass

    @abstractmethod
    def count(self, query: dict = {}) -> int:
        """Count documents/records matching the query."""
        pass
