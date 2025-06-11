from pydantic import BaseModel, Field


class ContentConfig(BaseModel):
    """
    Configuration for content generation.
    """

    temperature: float = Field(
        default=0.7, description="Controls the randomness of the output."
    )
    top_p: float = Field(
        default=0.9, description="Controls the diversity of the output."
    )
    top_k: int = Field(
        default=30,
        description="Limits the number of highest probability vocabulary tokens to consider.",
    )


class AgentProcess(BaseModel):
    org_id: int
    agent: str = "multi"
    text: str
