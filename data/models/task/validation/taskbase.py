# data/models/task/validation/taskbase.py
from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime

class TaskBase(BaseModel):
    """Базовая модель задачи."""
    name: Optional[str] = Field(None, max_length=255, description="Название задачи")
    description: Optional[str] = Field(None, description="Описание задачи")
    created_at: Optional[datetime] = Field(None, description="Дата создания, начала задачи (в формате YYYY-MM-DD)")
    updated_at: Optional[datetime] = Field(None, description="Дата окончания, начала задачи (в формате YYYY-MM-DD)")
    is_completed: Optional[bool] = Field(default=False, description="Статус выполнения задачи (True - выполнена, False - не выполнена)")