from models.platform import PlatformRead

from .base import SQLRepository


class PlatformRepository(SQLRepository[PlatformRead]):
    """Repository for managing platform in SQL."""

    def __init__(self):
        super().__init__(model=PlatformRead, collection="Platform")
