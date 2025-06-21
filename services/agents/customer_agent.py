from .base import AgentBase
from .tools import changelog


class CustomerAgent(AgentBase):
    def __init__(self, org_id: int = None):
        super().__init__(
            name="CustomerAgent",
            description="An agent that can perform customer service tasks using tools.",
            instructions="You are a customer service agent. Use your tools to solve customer problems efficiently. You should handle customer inquiries, support ticket management, customer feedback analysis, knowledge base management, and customer communication documentation for the organization.",
            org_id=org_id,
        )
        self.tools = [
            {
                "build": True,
                "callback": changelog.save_changelog,
            },
            {
                "build": True,
                "callback": changelog.get_changelog,
            },
            {
                "build": True,
                "callback": changelog.delete_changelog,
            },
            {
                "build": True,
                "callback": changelog.sort_changelog,
            },
        ]
