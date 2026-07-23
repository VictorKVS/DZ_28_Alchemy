from sqlalchemy.exc import IntegrityError
from app.database import engine, SessionLocal, Base
from app.models import User

Base.metadata.create_all(bind=engine)

def demo_transaction_rollback():
    print("\n" + "="*50)
    print("ДЕМОНСТРАЦИЯ ТРАНЗАКЦИИ И ОТКАТА (ROLLBACK)")
    print("="*50)
    
    # Очищаем таблицу перед тестом
    with SessionLocal() as session:
        session.query(User).delete()
        session.commit()

    with SessionLocal() as session:
        try:
            print("➕ Добавляем 2-х валидных пользователей...")
            session.add(User(username="user1", email="user1@test.com"))
            session.add(User(username="user2", email="user2@test.com"))
            
            print("❌ Имитируем ошибку: нарушаем UNIQUE constraint на email...")
            session.add(User(username="user3", email="user1@test.com")) # Дубликат!
            
            session.commit()
            print("✅ Транзакция успешно завершена (этого не должно произойти)")
            
        except IntegrityError as e:
            print(f"⚠️ Перехвачена ошибка: {e.orig}")
            print("🔄 Выполняем session.rollback()...")
            session.rollback() # Откатываем ВСЕ изменения в этой сессии
            
    # Проверка
    with SessionLocal() as session:
        count = session.query(User).count()
        print(f"📊 Пользователей в базе после отката: {count} (Ожидалось: 0)")

if __name__ == "__main__":
    demo_transaction_rollback()