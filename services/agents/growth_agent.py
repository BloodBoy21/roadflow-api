from .base import AgentBase
from .tools import changelog


class GrowthAgent(AgentBase):
    def __init__(self, org_id: int = None):
        super().__init__(
            name="GrowthAgent",
            description="An agent that can perform growth and marketing tasks using tools.",
            instructions="You are a growth agent. Use your tools to solve growth and marketing problems efficiently. You should manage marketing campaigns, user acquisition strategies, conversion optimization, market analysis, growth metrics tracking, and growth documentation for the organization.",
            org_id=org_id,
        )
