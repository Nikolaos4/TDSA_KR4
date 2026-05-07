from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI(title="User API for Testing")

fake_db: Dict[int, dict] = {}
current_id = 1

class UserCreate(BaseModel):
    name: str
    email: str
    age: int

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int


@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    global current_id
    user_id = current_id
    fake_db[user_id] = user.model_dump()
    current_id += 1
    return {"id": user_id, **user.dict()}


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user_id, **fake_db[user_id]}


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")
    del fake_db[user_id]
    return  # No content


@app.get("/users/", response_model=List[UserResponse])
def list_users():
    return [{"id": uid, **data} for uid, data in fake_db.items()]