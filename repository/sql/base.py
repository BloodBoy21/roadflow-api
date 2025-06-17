# repository/sql_repository.py
from typing import Any, TypeVar

from pydantic import BaseModel

from lib.prisma import prisma
from repository.base_repository import BaseRepository

T = TypeVar("T", bound=BaseModel)


class SQLRepository(BaseRepository[T]):
    """SQL repository implementation using Prisma."""

    _instances = {}  # Class-level dictionary to store instances

    def __new__(cls, *args, **kwargs):
        # Use the class name as part of the key to allow different subclasses to have their own instances
        key = f"{cls.__name__}"
        if key not in cls._instances:
            cls._instances[key] = super(SQLRepository, cls).__new__(cls)
            cls._instances[key]._initialized = False
        return cls._instances[key]

    def __init__(self, collection: str, model: type[T]):
        if hasattr(self, "_initialized") and self._initialized:
            return
        self.db = prisma
        self.collection = getattr(self.db, collection.lower())
        self.model = model
        self._initialized = True

    async def create(self, data: T | dict, options: dict = {}) -> T | None:
        """Create a new record in the database."""
        if not data:
            return None
        if isinstance(data, BaseModel):
            record = await self.collection.create(
                data=data.model_dump(**options, exclude={"id"})
            )
            return self.__parse_to_model(record)
        record = await self.collection.create(data=data)
        return self.__parse_to_model(record)

    async def find(self, query: dict = {}, options: dict = {}) -> list[T]:
        """Find records matching the query."""
        data = await self.collection.find_many(where=query, **options)
        return [self.__parse_to_model(d) for d in data]

    async def find_one(self, query: dict, options: dict = {}) -> T | None:
        """Find a single record matching the query."""
        data = await self.collection.find_first(where=query, **options)
        return self.__parse_to_model(data)

    async def find_unique(self, query: dict, options: dict = {}) -> T | None:
        """Find a unique record matching the query."""
        data = await self.collection.find_unique(where=query, **options)
        return self.__parse_to_model(data)

    async def get_by_id(
        self, id: int, options: dict = {}, key: str = "id"
    ) -> T | None:
        """Get a record by its ID."""
        data = await self.collection.find_unique(where={key: id}, **options)
        return self.__parse_to_model(data)

    async def update(
        self, query: dict, data: T | dict, options: dict = {}
    ) -> T | None:
        """Update records matching the query."""
        if not data:
            return None
        if isinstance(data, BaseModel):
            updated = await self.collection.update(
                where=query,
                data=data.model_dump(**options, exclude={"id"}),
            )
            return self.__parse_to_model(updated)
        updated = await self.collection.update(where=query, data=data)
        return self.__parse_to_model(updated)

    async def update_by_id(
        self, id: int, data: T | dict, options: dict = {}
    ) -> T | None:
        """Update a record by its ID."""
        if not data:
            return None
        if isinstance(data, BaseModel):
            updated = await self.collection.update(
                where={"id": id},
                data=data.model_dump(**options, exclude={"id"}),
            )
            return self.__parse_to_model(updated)
        updated = await self.collection.update(where={"id": id}, data=data)
        return self.__parse_to_model(updated)

    async def delete(self, query: dict) -> Any:
        """Delete a record matching the query."""
        return await self.collection.delete(where=query)

    async def delete_many(self, query: dict) -> Any:
        """Delete multiple records matching the query."""
        return await self.collection.delete_many(where=query)

    async def count(self, query: dict = {}) -> int:
        """Count records matching the query."""
        return await self.collection.count(where=query)

    async def exists(self, **kwargs) -> bool:
        """Check if a record exists matching the given criteria."""
        data = await self.collection.find_first(where=kwargs)
        return data is not None

    def __parse_to_model(self, data: Any) -> T | None:
        """Convert a database record to a model instance."""
        if not data:
            return None
        return self.model(**data.model_dump())
