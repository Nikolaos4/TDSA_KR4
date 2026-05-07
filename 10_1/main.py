from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI(title="Custom Error Handling Demo")

class ErrorResponse(BaseModel):
    status_code: int
    error_message: str
    detail: str | None = None   # дополнительные детали (опционально)

class CustomExceptionA(HTTPException):
    def __init__(self, detail: str = "Resource not found", status_code: int = 404):
        super().__init__(status_code=status_code, detail=detail)

class CustomExceptionB(HTTPException):
    def __init__(self, detail: str = "Forbidden access", status_code: int = 403):
        super().__init__(status_code=status_code, detail=detail)


@app.exception_handler(CustomExceptionA)
async def handle_exception_a(request: Request, exc: CustomExceptionA):
    print(f"[ERROR] Exception A: {exc.detail}, status: {exc.status_code}")
    error_content = ErrorResponse(
        status_code=exc.status_code,
        error_message="CustomExceptionA occurred",
        detail=exc.detail
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(error_content)
    )

@app.exception_handler(CustomExceptionB)
async def handle_exception_b(request: Request, exc: CustomExceptionB):
    print(f"[ERROR] Exception B: {exc.detail}, status: {exc.status_code}")
    error_content = ErrorResponse(
        status_code=exc.status_code,
        error_message="CustomExceptionB occurred",
        detail=exc.detail
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(error_content)
    )



@app.get("/items/{item_id}")
async def get_item(item_id: int):
    """Если item_id == 42, бросаем CustomExceptionA (Not Found)"""
    if item_id == 42:
        raise CustomExceptionA(detail=f"Item with id {item_id} does not exist")
    return {"item_id": item_id, "message": "Item found"}

@app.post("/access/{user_role}")
async def check_access(user_role: str):
    """Если роль не 'admin', бросаем CustomExceptionB (Forbidden)"""
    if user_role.lower() != "admin":
        raise CustomExceptionB(detail=f"Role '{user_role}' is not allowed to access this resource")
    return {"message": f"Access granted for {user_role}"}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"[CRITICAL] Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(ErrorResponse(
            status_code=500,
            error_message="Internal Server Error",
            detail="An unexpected error occurred. Please try again later."
        ))
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)