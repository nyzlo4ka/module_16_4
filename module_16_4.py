from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()
users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/users')
async def read_users() -> list[User]:
    return users


@app.post('/user/{username}/{age}')
async def create_user(username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username')],
                      age: int = Path(ge=18, le=120, description='Enter age')) -> dict:
    if users:
        user_id = max(user.id for user in users) + 1
    else:
        user_id = 1
    users.append(User(id=user_id, username=username, age=age))
    return {"message": f"User {user_id} is registered"}


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int, username: Annotated[str, Path(min_length=5, max_length=20,
                                                                  description='Enter username')],
                      age: int = Path(ge=18, le=120, description='Enter age')) -> dict:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return {"message": f"User {user_id} is updated"}
        else:
            raise HTTPException(status_code=404, detail="User was not found")


@app.delete('/user/{user_id}')
async def delete_user(user_id: int) -> dict:
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return {"message": f"User {user_id} has been deleted"}
    raise HTTPException(status_code=404, detail="User was not found")
