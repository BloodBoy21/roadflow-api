from .base import AgentBase
from .tools import changelog


class OperationsAgent(AgentBase):
    def __init__(self, org_id: int = None):
        super().__init__(
            name="OperationsAgent",
            description="An agent that can perform operations management tasks using tools.",
            instructions="You are an operations agent. Use your tools to solve operational problems efficiently. You should manage system monitoring, process optimization, resource allocation, incident response, and operational documentation for the organization.",
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
