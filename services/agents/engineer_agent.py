from .base import AgentBase


class EngineerAgent(AgentBase):
    def __init__(self, org_id: int = None):
        super().__init__(
            name="EngineerAgent",
            description="An agent that can perform engineering tasks using tools.",
            instructions="You are an engineer agent. Use your tools to solve engineering problems efficiently.",
            org_id=org_id,
        )
