from .base import SQLRepository
from models.user import UserRead


class UserRepository(SQLRepository[UserRead]):
    """Repository for managing user in SQL."""

    def __init__(self):
        super().__init__(model=UserRead,collection="User")
