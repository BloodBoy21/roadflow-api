from bson.objectid import ObjectId as BsonObjectId
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema


class ObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, config):
        if not isinstance(v, BsonObjectId) and not isinstance(v, str):
            raise TypeError("ObjectId required")
        if isinstance(v, str):
            try:
                v = BsonObjectId(v)
            except Exception:
                raise ValueError("Invalid ObjectId")
        return v

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type, _handler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_wrap_validator_function(
            cls.validate,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema, handler) -> JsonSchemaValue:
        return handler(core_schema.str_schema())


def sanitize_object_id(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, BsonObjectId):
                obj[key] = str(value)
            elif isinstance(value, dict):
                sanitize_object_id(value)
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            if isinstance(value, BsonObjectId):
                obj[i] = str(value)
            elif isinstance(value, dict):
                sanitize_object_id(value)
    return obj
