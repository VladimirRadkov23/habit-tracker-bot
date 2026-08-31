from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas


# === РАБОТА С ПОЛЬЗОВАТЕЛЯМИ ===

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter_by(id=user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(id=user.id, username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# === РАБОТА С ПРИВЫЧКАМИ ===

def get_user_habits(db: Session, user_id: int):
    return db.query(models.Habit).filter_by(user_id=user_id).all()


def get_habit(db: Session, habit_id: int):
    return db.query(models.Habit).filter_by(id=habit_id).first()


def create_habit(db: Session, habit: schemas.HabitCreate):
    db_habit = models.Habit(
        user_id=habit.user_id,
        title=habit.title,
        description=habit.description,
        time_to_remind=habit.time_to_remind
    )
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit


def delete_habit(db: Session, habit_id: int):
    db_habit = db.query(models.Habit).filter_by(id=habit_id).first()
    if db_habit:
        db.delete(db_habit)
        db.commit()
        return True
    return False


# === ЛОГИРОВАНИЕ (ОТМЕТКИ ВЫПОЛНЕНИЯ) ===

def log_habit(db: Session, habit_id: int, is_completed: bool):
    # Создаем отметку на текущий день
    db_log = models.HabitLog(
        habit_id=habit_id,
        date=datetime.utcnow(),
        is_completed=is_completed
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log
