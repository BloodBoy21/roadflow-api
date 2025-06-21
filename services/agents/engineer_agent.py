from .base import AgentBase
from .tools import changelog


class EngineerAgent(AgentBase):
    def __init__(self, org_id: int = None):
        super().__init__(
            name="EngineerAgent",
            description="An agent that can perform engineering tasks using tools.",
            instructions="You are an engineer agent. Use your tools to solve engineering problems efficiently.You should create the changelog for the organization and manage it effectively. Also you should create documentation for the organization.",
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
