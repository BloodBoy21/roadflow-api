import os
from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field, PrivateAttr

from lib.mongo import db
from utils.object_id import ObjectId

TZ = os.getenv("TZ", "America/Mexico_City")

tz_zone = ZoneInfo(TZ)


class MongoModel(BaseModel):
    id: ObjectId | None = Field(default=None, alias="_id")
    createdAt: datetime | None = Field(default_factory=lambda: datetime.now(tz_zone))
    updatedAt: datetime | None = Field(default_factory=lambda: datetime.now(tz_zone))
    _collection_name: str = PrivateAttr()

    def __init__(self, **data):
        """
        Ensure that `_collection_name` is set when initializing the model.
        """
        super().__init__(**data)
        if not getattr(self, "_collection_name", None):
            raise ValueError("You must define `_collection_name` in the subclass.")

    @classmethod
    def get_collection(cls):
        """
        Return the MongoDB collection for this model.
        """
        if not cls._collection_name:
            raise ValueError("Collection name is not defined.")
        return db[cls._collection_name]

    @classmethod
    def find(cls, filter: dict):
        """
        Query the collection with a filter.
        """
        return cls.get_collection().find(filter)

    def save(self):
        """
        Save the current instance to the database.
        If `id` exists, it performs an update; otherwise, it inserts a new document.
        """
        collection = self.get_collection()
        if self.id:
            # Update existing document
            result = collection.update_one(
                {"_id": self.id},
                {"$set": self.model_dump(by_alias=True, exclude={"id"})},
            )
            return result.modified_count
        else:
            # Insert new document
            result = collection.insert_one(
                self.model_dump(by_alias=True, exclude={"id"})
            )
            self.id = result.inserted_id
            return result.inserted_id
