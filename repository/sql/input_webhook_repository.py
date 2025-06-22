from models.input_webhook import InputWebhookRead

from .base import SQLRepository


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

    async def get_by_organization_id(
        self, organization_id: int, page: int = 1, limit: int = 20
    ) -> list[InputWebhookRead]:
        """
        Retrieve all InputWebhooks for a given organization ID.

        Args:
            org_id (int): The ID of the organization.

        Returns:
            list[InputWebhookRead]: A list of InputWebhooks associated with the organization.
        """
        query = {"org_id": organization_id}
        return await self.paginate(query=query, page=page, limit=limit)