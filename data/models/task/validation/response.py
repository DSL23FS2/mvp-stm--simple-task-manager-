# data/models/task/validation/api_response.py
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")
class APIResponse(BaseModel, Generic[T]):
    """Общая модель ответа API."""
    status: str  # "success" / "error"
    data: Optional[T]
    message: Optional[str] = None