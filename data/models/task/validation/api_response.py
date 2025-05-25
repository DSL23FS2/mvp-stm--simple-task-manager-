from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")

class APIResponse(BaseModel, Generic[T]):
    status: str  # "success" / "error"
    data: Optional[T]
    message: Optional[str] = None