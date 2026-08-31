from pydantic import BaseModel, ConfigDict
from datetime import datetime, time
from typing import Optional, List


# --- Схемы для Логов привычек ---
class HabitLogBase(BaseModel):
    is_completed: bool


class HabitLogCreate(HabitLogBase):
    pass


class HabitLogResponse(HabitLogBase):
    id: int
    habit_id: int
    date: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Схемы для Привычек ---
class HabitBase(BaseModel):
    title: str
    description: Optional[str] = None
    time_to_remind: Optional[time] = None


class HabitCreate(HabitBase):
    user_id: int  # Передаем, какому Telegram ID принадлежит привычка


class HabitResponse(HabitBase):
    id: int
    user_id: int
    created_at: datetime
    logs: List[HabitLogResponse] = []  # Сразу сможем подтягивать историю выполнения

    model_config = ConfigDict(from_attributes=True)


# --- Схемы для Пользователей ---
class UserBase(BaseModel):
    id: int  # Telegram ID
    username: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    registered_at: datetime
    habits: List[HabitResponse] = []

    model_config = ConfigDict(from_attributes=True)
