from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Импортируем наши модули.
# Если возникнут желтые подчеркивания, PyCharm сам предложит скорректировать пути через Alt+Enter
from . import models, schemas, crud, database
from .database import engine, get_db

# Автоматически создаем таблицы в базе данных при запуске приложения
# (для SQLite/PostgreSQL на старте, пока не используем сложные миграции Alembic)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Habit Tracker API")


# === ЭНДПОИНТЫ ДЛЯ ПОЛЬЗОВАТЕЛЕЙ ===

@app.post("/users/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user.id)
    if db_user:
        return db_user  # Если уже создан, просто возвращаем его
    return crud.create_user(db=db, user=user)


@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# === ЭНДПОИНТЫ ДЛЯ ПРИВЫЧЕК ===

@app.post("/habits/", response_model=schemas.HabitResponse, status_code=status.HTTP_201_CREATED)
def create_habit(habit: schemas.HabitCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли пользователь, для которого создается привычка
    db_user = crud.get_user(db, user_id=habit.user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found. Register user first.")
    return crud.create_habit(db=db, habit=habit)


@app.get("/users/{user_id}/habits/", response_model=List[schemas.HabitResponse])
def read_user_habits(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user_habits(db, user_id=user_id)


@app.delete("/habits/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    success = crud.delete_habit(db, habit_id=habit_id)
    if not success:
        raise HTTPException(status_code=404, detail="Habit not found")
    return None


# === ЭНДПОИНТЫ ДЛЯ ОТМЕТОК (ЛОГОВ) ===

@app.post("/habits/{habit_id}/log/", response_model=schemas.HabitLogResponse)
def log_habit_execution(habit_id: int, log_data: schemas.HabitLogCreate, db: Session = Depends(get_db)):
    db_habit = crud.get_habit(db, habit_id=habit_id)
    if not db_habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return crud.log_habit(db, habit_id=habit_id, is_completed=log_data.is_completed)
