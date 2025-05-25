from pydantic import Field

from .taskbase import TaskBase

class TaskUpdate(TaskBase):
    """Модель для обновления задачи."""
    id: int = Field(..., description="ID задачи (обязательно)")