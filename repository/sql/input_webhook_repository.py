from .base import SQLRepository
from models.input_webhook import InputWebhookRead


class InputWebhookRepository(SQLRepository[InputWebhookRead]):
    """Repository for managing input webhook in SQL."""

    def __init__(self):
        super().__init__(model=InputWebhookRead, collection="InputWebhook")

    async def get_by_key(self, webhook_key: str) -> InputWebhookRead | None:
        """
        Retrieve an InputWebhook by its webhook ID.

        Args:
            webhook_id (str): The ID of the webhook.

        Returns:
            InputWebhookRead | None: The InputWebhook if found, otherwise None.
        """
        return await self.find_one({"key": webhook_key})
