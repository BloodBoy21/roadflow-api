# repository/mongo_repository.py
from typing import Any, TypeVar

from loguru import logger
from pydantic import BaseModel

from lib.mongo import db
from repository.base_repository import BaseRepository
from utils.object_id import ObjectId

T = TypeVar("T", bound=BaseModel)


class MongoRepository(BaseRepository[T]):
    """MongoDB repository implementation."""

    _instances = {}  # Class-level dictionary to store instances

    def __new__(cls, *args, **kwargs):
        # Use the class name as part of the key to allow different subclasses to have their own instances
        key = f"{cls.__name__}"
        if key not in cls._instances:
            cls._instances[key] = super(MongoRepository, cls).__new__(cls)
            cls._instances[key]._initialized = False
        return cls._instances[key]

    def __init__(self, collection: str, model: type[T]):
        if hasattr(self, "_initialized") and self._initialized:
            return
        self.db = db
        self.collection = collection
        self.collection_db = getattr(self.db, collection)
        self.model = model
        self._initialized = True

    def create(self, data: T | dict, options: dict = {}) -> T | None:
        """Create a new document in the MongoDB collection."""
        if not data:
            return None
        if isinstance(data, BaseModel):
            inserted = self.collection_db.insert_one(
                data.model_dump(**options, exclude={"_id"})
            )
            return self.find_by_id(ObjectId(inserted.inserted_id))
        inserted = self.collection_db.insert_one(data)
        return self.find_by_id(ObjectId(inserted.inserted_id))

    def find(self, query: dict, options: dict = {}) -> list[T]:
        """Find documents matching the query."""
        cursor = self.collection_db.find(query, options.get("projection", {}))
        cursor = self.apply_actions(cursor, options)
        return [self.__return_model(data) for data in cursor]

    def find_one(self, query: dict, options: dict = {}) -> T | None:
        """Find a single document matching the query."""
        try:
            return self.__return_model(self.collection_db.find_one(query))
        except Exception as e:
            logger.error(e)
            return None

    def update(
        self,
        query: dict,
        data: T | dict,
        options: dict = {"exclude_none": True},
    ) -> T | None:
        """Update documents matching the query."""
        if not data:
            return None
        document = self.collection_db.find_one(query)
        if not document:
            raise Exception("Document not found")
        if isinstance(data, BaseModel):
            self.collection_db.update_one(
                query,
                {"$set": data.model_dump(**options)},
            )
            return self.find_one(query)

        self.collection_db.update_one(
            query,
            {"$set": data},
        )
        return self.find_one(query)

    def update_by_id(
        self,
        id: ObjectId | str,
        data: T | dict,
        options: dict = {"exclude_none": True},
    ) -> T | None:
        """Update a document by its ID."""
        if isinstance(id, str):
            id = ObjectId(id)
        if not data:
            return None
        self.update({"_id": id}, data, options)
        return self.find_by_id(id)

    def delete(self, query: dict = {}) -> Any:
        """Delete a document matching the query."""
        return self.collection_db.delete_one(query)

    def delete_many(self, query: dict = {}) -> Any:
        """Delete multiple documents matching the query."""
        return self.collection_db.delete_many(query)

    def count(self, query: dict = {}) -> int:
        """Count documents matching the query."""
        return self.collection_db.count_documents(query)

    def find_by_id(self, id: ObjectId | str, options: dict = {}) -> T | None:
        """Find a document by its ID."""
        if isinstance(id, str):
            id = ObjectId(id)
        return self.__return_model(self.collection_db.find_one({"_id": id}))

    def delete_by_id(self, id: ObjectId | str) -> Any:
        """Delete a document by its ID."""
        if isinstance(id, str):
            id = ObjectId(id)
        return self.collection_db.delete_one({"_id": id})

    def apply_actions(self, cursor, options: dict = {}) -> Any:
        """Apply cursor actions based on the options."""
        for action in options:
            cursor = self.cursor_actions(cursor, action, options)
        return cursor

    def cursor_actions(self, cursor, action: str, options: dict = {}) -> Any:
        """Apply specific cursor actions."""
        match action:
            case "sort":
                key, type = options.get("sort", ("_id", -1))
                return cursor.sort(key, type)
            case "skip":
                return cursor.skip(options.get("skip", 0))
            case "limit":
                return cursor.limit(options.get("limit", 0))
            case _:
                return cursor

    def aggregate(self, pipeline: list) -> list:
        """Perform an aggregation pipeline query."""
        return self.collection_db.aggregate(pipeline)

    def bulk_write(self, operations: list) -> Any:
        """Perform bulk write operations."""
        return self.collection_db.bulk_write(operations)

    def paginate(
        self, query: dict, page: int = 1, limit: int = 20, options: dict = {}
    ) -> tuple[list[T], int, int]:
        """Paginate documents matching the query."""
        if page < 1:
            page = 1
        if limit < 1:
            limit = 20
        skip = (page - 1) * limit
        options["skip"] = skip
        options["limit"] = limit
        options["sort"] = options.get("sort", ("_id", -1))

        cursor = self.collection_db.find(query, options.get("projection", {}))
        cursor = self.apply_actions(cursor, options)

        data = [self.__return_model(doc) for doc in cursor]
        total_count = self.count(query)
        total_pages = (total_count + limit - 1) // limit

        return data, total_pages, total_count

    def __return_model(self, data: dict) -> T | None:
        """Convert a document to a model instance."""
        if not data:
            return None
        data["_collection_name"] = self.collection
        model_instance = self.model(**data)
        return model_instance
