from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Time, Boolean
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # Это будет Telegram ID пользователя
    username = Column(String, nullable=True)
    registered_at = Column(DateTime, default=datetime.utcnow)

    # Связь: у одного пользователя может быть много привычек
    habits = relationship("Habit", back_populates="owner", cascade="all, delete-orphan")


class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    time_to_remind = Column(Time, nullable=True)  # Время, когда бот должен прислать пуш
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связи
    owner = relationship("User", back_populates="habits")
    logs = relationship("HabitLog", back_populates="habit", cascade="all, delete-orphan")


class HabitLog(Base):
    __tablename__ = "habit_logs"

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id", ondelete="CASCADE"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)  # День, за который делается отметка
    is_completed = Column(Boolean, default=True)  # Выполнено или нет

    habit = relationship("Habit", back_populates="logs")
