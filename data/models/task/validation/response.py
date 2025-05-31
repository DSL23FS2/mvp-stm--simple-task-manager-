# data/models/task/validation/api_response.py
from typing import Generic, TypeVar, Optional
from typing import List
from pydantic import BaseModel

T = TypeVar("T")
class APIResponse(BaseModel, Generic[T]):
    """Общая модель ответа API."""
    status: str  # "success" / "error"
    data: List[Optional[T]]
    message: Optional[str] = None