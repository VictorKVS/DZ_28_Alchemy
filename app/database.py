from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import logging

# Бонус: Включаем логирование SQL-запросов для анализа
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Используем SQLite для простоты
DATABASE_URL = "sqlite:///./app.db"

# echo=True дублирует логи в консоль для наглядности сравнения N+1 и joinedload
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_session():
    """Фабрика сессий (паттерн Dependency Injection)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
