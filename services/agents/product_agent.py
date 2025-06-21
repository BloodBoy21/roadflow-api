from .base import AgentBase
from .tools import changelog


class ProductAgent(AgentBase):
    def __init__(self, org_id: int = None):
        super().__init__(
            name="ProductAgent",
            description="An agent that can perform product management tasks using tools.",
            instructions="You are a product agent. Use your tools to solve product management problems efficiently. You should manage product roadmaps, feature specifications, user feedback analysis, and product documentation for the organization.",
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