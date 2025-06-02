from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Union, Dict, Type, Optional, Any
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T], ABC):
    """Abstract base repository that defines the common interface for all repositories."""

    @abstractmethod
    def __init__(self, collection: str, model: Type[T]):
        """Initialize the repository with a collection name and model type."""
        pass

    @abstractmethod
    def create(self, data: Union[T, Dict], options: Dict = {}) -> Optional[T]:
        """Create a new document/record in the database."""
        pass

    @abstractmethod
    def find(self, query: Dict, options: Dict = {}) -> List[T]:
        """Find documents/records matching the query."""
        pass

    @abstractmethod
    def find_one(self, query: Dict, options: Dict = {}) -> Optional[T]:
        """Find a single document/record matching the query."""
        pass

    @abstractmethod
    def update(
        self, query: Dict, data: Union[T, Dict], options: Dict = {}
    ) -> Optional[T]:
        """Update documents/records matching the query."""
        pass

    @abstractmethod
    def delete(self, query: Dict = {}) -> Any:
        """Delete a document/record matching the query."""
        pass

    @abstractmethod
    def count(self, query: Dict = {}) -> int:
        """Count documents/records matching the query."""
        pass
