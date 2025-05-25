from fastapi.responses import JSONResponse
from typing import Any

def format_response(
    success: bool = True,
    data: Any = None,
    message: str = "",
    status_code: int = None
) -> JSONResponse:
    if status_code is None:
        status_code = 200 if success else 400

    return JSONResponse(
        status_code=status_code,
        content={
            "status": "success" if success else "error",
            "data": data,
            "message": message
        }
    )
