            # Домашнее задание по теме "Модели данных Pydantic"


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr, conint
from typing import List, Optional

app = FastAPI()

# Пустой список для хранения пользователей
users = []

# Определение модели пользователя
class User(BaseModel):
    id: int
    username: constr(min_length=5, max_length=20)
    age: conint(ge=0)

@app.get("/users", response_model=List[User])
def get_users():
    """Возвращает список всех пользователей"""
    return users

@app.post("/user/{username}/{age}", response_model=User)
def create_user(
    username: constr(min_length=5, max_length=20),
    age: conint(ge=0)
):
    """Добавляет нового пользователя и возвращает его"""
    new_id = (users[-1].id + 1) if users else 1  # Максимальный ID + 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put("/user/{user_id}/{username}/{age}", response_model=User)
def update_user(
    user_id: int,
    username: constr(min_length=5, max_length=20),
    age: conint(ge=0)
):
    """Обновляет существующего пользователя и возвращает его"""
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")

@app.delete("/user/{user_id}", response_model=User)
def delete_user(user_id: int):
    """Удаляет пользователя и возвращает его"""
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User was not found")



