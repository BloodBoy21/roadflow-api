# repository/mongo_repository.py
import os
from datetime import datetime
from typing import Any, TypeVar
from zoneinfo import ZoneInfo

from loguru import logger
from pydantic import BaseModel

from lib.mongo import db
from repository.base_repository import BaseRepository
from utils.object_id import ObjectId

TZ = os.getenv("TZ", "America/Mexico_City")
tz_zone = ZoneInfo(TZ)

T = TypeVar("T", bound=BaseModel)


class MongoRepository(BaseRepository[T]):
    """MongoDB repository implementation."""

    def __init__(self, collection: str, model: type[T]):
        self.db = db
        self.collection = collection
        self.collection_db = getattr(self.db, collection)
        self.model = model

    def create(self, data: T | dict, options: dict = None) -> T | None:
        """Create a new document in the MongoDB collection."""
        if options is None:
            options = {}
        if not data:
            return None
        if isinstance(data, BaseModel):
            data = data.model_dump(**options, exclude={"_id"})
        _date = datetime.now(tz_zone)
        data["createdAt"] = _date
        data["updatedAt"] = _date

        inserted = self.collection_db.insert_one(data)
        return self.find_by_id(ObjectId(inserted.inserted_id))

    def find(self, query: dict, options: dict = None) -> list[T]:
        """Find documents matching the query."""
        if options is None:
            options = {}
        cursor = self.collection_db.find(query, options.get("projection", {}))
        cursor = self.apply_actions(cursor, options)
        return [self.__return_model(data) for data in cursor]

    def find_one(self, query: dict, options: dict = None) -> T | None:
        """Find a single document matching the query."""
        if options is None:
            options = {}
        try:
            return self.__return_model(self.collection_db.find_one(query))
        except (ConnectionError, TimeoutError) as e:
            logger.error(f"Database connection error in find_one: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in find_one: {e}")
            return None

    def update(
        self,
        query: dict,
        data: T | dict,
        options: dict = None,
    ) -> T | None:
        """Update documents matching the query."""
        if options is None:
            options = {"exclude_none": True}
        if not data:
            return None
        document = self.collection_db.find_one(query)
        if not document:
            raise ValueError("Document not found")
        if isinstance(data, BaseModel):
            self.collection_db.update_one(
                query,
                {"$set": data.model_dump(**options)},
            )
            return self.find_one(query)
        data["updatedAt"] = datetime.now(tz_zone)
        self.collection_db.update_one(
            query,
            {"$set": data},
        )
        return self.find_one(query)

    def update_by_id(
        self,
        id: ObjectId | str,
        data: T | dict,
        options: dict = None,
    ) -> T | None:
        """Update a document by its ID."""
        if options is None:
            options = {"exclude_none": True}
        if isinstance(id, str):
            id = ObjectId(id)
        if not data:
            return None
        self.update({"_id": id}, data, options)
        return self.find_by_id(id)

    def delete(self, query: dict = None) -> Any:
        """Delete a document matching the query."""
        if query is None:
            query = {}
        return self.collection_db.delete_one(query)

    def delete_many(self, query: dict = None) -> Any:
        """Delete multiple documents matching the query."""
        if query is None:
            query = {}
        return self.collection_db.delete_many(query)

    def count(self, query: dict = None) -> int:
        """Count documents matching the query."""
        if query is None:
            query = {}
        return self.collection_db.count_documents(query)

    def find_by_id(self, id: ObjectId | str, options: dict = None) -> T | None:
        """Find a document by its ID."""
        if options is None:
            options = {}
        if isinstance(id, str):
            id = ObjectId(id)
        return self.__return_model(self.collection_db.find_one({"_id": id}))

    def delete_by_id(self, id: ObjectId | str) -> Any:
        """Delete a document by its ID."""
        if isinstance(id, str):
            id = ObjectId(id)
        return self.collection_db.delete_one({"_id": id})

    def apply_actions(self, cursor, options: dict = None) -> Any:
        """Apply cursor actions based on the options."""
        if options is None:
            options = {}
        for action in options:
            cursor = self.cursor_actions(cursor, action, options)
        return cursor

    def cursor_actions(self, cursor, action: str, options: dict = None) -> Any:
        """Apply specific cursor actions."""
        if options is None:
            options = {}
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
        self, query: dict, page: int = 1, limit: int = 20, options: dict = None
    ) -> tuple[list[T], int, int]:
        """Paginate documents matching the query."""
        if options is None:
            options = {}
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
