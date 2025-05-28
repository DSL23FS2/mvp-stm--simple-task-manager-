# data/models/task/validation/taskcreate.py
from pydantic import Field

from .taskbase import TaskBase
class TaskCreate(TaskBase):
    """Модель для создания задачи."""
    name: str = Field(..., max_length=255, description="Название задачи (обязательно)")