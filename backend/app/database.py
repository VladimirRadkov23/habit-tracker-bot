import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Получаем URL базы из переменных окружения Docker.
# Если запускаем локально без Docker, будет использоваться SQLite файл 'habits.db' для удобства тестов.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./habits.db")

# Для SQLite нужен специальный аргумент check_same_thread. Для PostgreSQL он роли не играет.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Функция-генератор для получения сессии базы данных в эндпоинтах FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
