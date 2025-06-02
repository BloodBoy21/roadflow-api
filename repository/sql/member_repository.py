from .base import SQLRepository
from models.member import MemberRead


class MemberRepository(SQLRepository[MemberRead]):
    """Repository for managing member in SQL."""

    def __init__(self):
        super().__init__(model=MemberRead,collection="Member")
