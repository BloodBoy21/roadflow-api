from models.user import UserRead

from .base import SQLRepository


class UserRepository(SQLRepository[UserRead]):
    """Repository for managing user in SQL."""

    def __init__(self):
        super().__init__(model=UserRead, collection="User")

    async def get_by_email(self, email: str) -> UserRead | None:
        """Get a user by email."""
        return await self.find_one({"email": email})
