# data/models/task/validation/taskquery.py

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"

class TaskQueryParams(BaseModel):
    name: Optional[str] = Field(None, description="Фильтр по имени (подстрока)")
    is_completed: Optional[bool] = Field(None, description="Фильтр по статусу")
    sort_by: Optional[str] = Field("created_at", description="Поле сортировки")
    order: SortOrder = Field(SortOrder.asc, description="Направление сортировки")
    skip: int = Field(0, ge=0, description="Смещение")
    limit: int = Field(100, gt=0, le=100, description="Максимум результатов")
