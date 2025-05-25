from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime

class TaskBase(BaseModel):
    """Базовая модель задачи."""
    name: Optional[str] = Field(None, max_length=255, description="Название задачи")
    description: Optional[str] = Field(None, description="Описание задачи")
    created_at: Optional[datetime] = Field(None, description="Дата создания, начала задачи (в формате YYYY-MM-DD)")
    updated_at: Optional[datetime] = Field(None, description="Дата окончания, начала задачи (в формате YYYY-MM-DD)")
    is_completed: Optional[bool] = Field(None, description="Статус выполнения задачи (True - выполнена, False - не выполнена)")

    
class TaskCreate(TaskBase):
    """Модель для создания задачи."""
    name: str = Field(..., max_length=255, description="Название задачи (обязательно)")

class TaskUpdate(TaskBase):
    """Модель для обновления задачи."""
    id: int = Field(..., description="ID задачи (обязательно)")

class TaskDelete(BaseModel):
    """Модель для удаления задачи."""
    id: int = Field(..., description="ID задачи (обязательно)")

class TaskFilter(BaseModel):
    """Модель для фильтрации задач."""
    filters: List[Any] = Field(..., description="Список условий для фильтрации")
    
class TaskOutput(TaskBase):
    """Модель для вывода задачи."""
    id: int = Field(..., description="ID задачи (обязательно)")
    
    model_config = {
        "from_attributes": True,
    }