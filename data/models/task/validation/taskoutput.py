# data/models/task/validation/taskoutput.py
from pydantic import Field

from .taskbase import TaskBase
class TaskOutput(TaskBase):
    """Модель для вывода задачи."""
    id: int = Field(..., description="ID задачи (обязательно)")
    
    model_config = {
        "from_attributes": True,
    }