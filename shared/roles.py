from enum import Enum


class RoleEnum(str, Enum):
    ADMIN = "admin"
    MEMBER = "member"
    OWNER = "owner"
