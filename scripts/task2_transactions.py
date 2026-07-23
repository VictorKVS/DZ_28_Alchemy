import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.exc import IntegrityError
from app.database import engine, SessionLocal, Base
from app.models import User

Base.metadata.create_all(bind=engine)

def demo_transaction_rollback():
    print("\n" + "="*50)
    print("ДЕМОНСТРАЦИЯ ТРАНЗАКЦИИ И ОТКАТА (ROLLBACK)")
    print("="*50)
    
    with SessionLocal() as session:
        session.query(User).delete()
        session.commit()

    with SessionLocal() as session:
        try:
            print("➕ Добавляем 2-х валидных пользователей...")
            session.add(User(username="user1", email="user1@test.com"))
            session.add(User(username="user2", email="user2@test.com"))
            
            print("❌ Имитируем ошибку: нарушаем UNIQUE constraint на email...")
            session.add(User(username="user3", email="user1@test.com"))
            
            session.commit()
            print("✅ Транзакция успешно завершена (этого не должно произойти)")
            
        except IntegrityError as e:
            print(f"⚠️ Перехвачена ошибка: {e.orig}")
            print("🔄 Выполняем session.rollback()...")
            session.rollback()
            
    with SessionLocal() as session:
        count = session.query(User).count()
        print(f"📊 Пользователей в базе после отката: {count} (Ожидалось: 0)")

if __name__ == "__main__":
    demo_transaction_rollback()
