from pydantic import BaseModel


class TaskResponse(BaseModel):
    success: bool = True
    message: str = "Task completed successfully"
    payload: dict = {}
