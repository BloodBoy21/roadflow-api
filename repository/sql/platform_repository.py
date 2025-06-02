from .base import SQLRepository
from models.platform import PlatformRead


class PlatformRepository(SQLRepository[PlatformRead]):
    """Repository for managing platform in SQL."""

    def __init__(self):
        super().__init__(model=PlatformRead,collection="Platform")
