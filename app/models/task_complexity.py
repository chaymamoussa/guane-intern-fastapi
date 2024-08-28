from pydantic import BaseModel

class TaskRequestBody(BaseModel):
    task_complexity: int
