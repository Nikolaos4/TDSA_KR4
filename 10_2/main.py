from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, conint, constr, EmailStr
from typing import Optional

app = FastAPI(title="User Registration with Custom Validation Error Handling")

class User(BaseModel):
    username: str
    age: conint(gt=18)                    
    email: EmailStr                        
    password: constr(min_length=8, max_length=16)  
    phone: Optional[str] = 'Unknown'      


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    body = await request.body()
    try:
        import json
        body_data = json.loads(body) if body else {}
    except:
        body_data = None

    formatted_errors = []
    for error in exc.errors():
        field = error["loc"][-1] if error["loc"] else "unknown"
        formatted_errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"]
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({
            "error": "Validation error",
            "details": formatted_errors,
            "received_body": body_data
        })
    )

@app.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    return user

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc) if app.debug else "An unexpected error occurred."
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)