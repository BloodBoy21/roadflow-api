# repository/sql_repository.py
from typing import Union, Dict, List, Type, Optional, Any, TypeVar
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

    def __init__(self, collection: str, model: Type[T]):
        if hasattr(self, "_initialized") and self._initialized:
            return
        self.db = prisma
        self.collection = getattr(self.db, collection.lower())
        self.model = model
        self._initialized = True

    async def create(self, data: Union[T, Dict], options: Dict = {}) -> Optional[T]:
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

    async def find(self, query: Dict = {}, options: Dict = {}) -> List[T]:
        """Find records matching the query."""
        data = await self.collection.find_many(where=query, **options)
        return [self.__parse_to_model(d) for d in data]

    async def find_one(self, query: Dict, options: Dict = {}) -> Optional[T]:
        """Find a single record matching the query."""
        data = await self.collection.find_first(where=query, **options)
        return self.__parse_to_model(data)

    async def find_unique(self, query: Dict, options: Dict = {}) -> Optional[T]:
        """Find a unique record matching the query."""
        data = await self.collection.find_unique(where=query, **options)
        return self.__parse_to_model(data)

    async def update(
        self, query: Dict, data: Union[T, Dict], options: Dict = {}
    ) -> Optional[T]:
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
        self, id: int, data: Union[T, Dict], options: Dict = {}
    ) -> Optional[T]:
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

    async def delete(self, query: Dict) -> Any:
        """Delete a record matching the query."""
        return await self.collection.delete(where=query)

    async def delete_many(self, query: Dict) -> Any:
        """Delete multiple records matching the query."""
        return await self.collection.delete_many(where=query)

    async def count(self, query: Dict = {}) -> int:
        """Count records matching the query."""
        return await self.collection.count(where=query)

    async def exists(self, **kwargs) -> bool:
        """Check if a record exists matching the given criteria."""
        data = await self.collection.find_first(where=kwargs)
        return data is not None

    def __parse_to_model(self, data: Any) -> Optional[T]:
        """Convert a database record to a model instance."""
        if not data:
            return None
        return self.model(**data.model_dump())
