from sqlalchemy.orm import joinedload
from sqlalchemy import select, func
from app.database import engine, SessionLocal, Base
from app.models import Author, Book

# Создаем таблицы перед запуском
Base.metadata.create_all(bind=engine)

def demo_n_plus_one():
    print("\n" + "="*50)
    print("1. ЛЕНИВАЯ ЗАГРУЗКА (Проблема N+1)")
    print("="*50)
    with SessionLocal() as session:
        if session.query(Author).count() == 0:
            author = Author(name="Фрэнк Герберт")
            author.books = [Book(title="Дюна"), Book(title="Мессия Дюны")]
            session.add(author)
            session.commit()

        authors = session.query(Author).all()
        for author in authors:
            print(f"Автор: {author.name}")
            for book in author.books:  # <-- Здесь будет выполнен отдельный SQL-запрос для каждого автора!
                print(f"  - Книга: {book.title}")

def demo_eager_loading():
    print("\n" + "="*50)
    print("2. ЖАДНАЯ ЗАГРУЗКА (Решение через joinedload)")
    print("="*50)
    with SessionLocal() as session:
        # Один запрос с SQL JOIN
        authors = session.query(Author).options(joinedload(Author.books)).all()
        for author in authors:
            print(f"Автор: {author.name}")
            for book in author.books:  # <-- Данные уже в памяти, новых запросов НЕТ!
                print(f"  - Книга: {book.title}")

def demo_core_aggregation():
    print("\n" + "="*50)
    print("3. БОНУС: Агрегирующий запрос через SQLAlchemy Core")
    print("="*50)
    with SessionLocal() as session:
        # Использование Core (func) для быстрого подсчета без загрузки объектов ORM
        stmt = select(func.count(Book.id))
        total_books = session.execute(stmt).scalar()
        print(f"Общее количество книг в БД (через Core): {total_books}")

if __name__ == "__main__":
    demo_n_plus_one()
    demo_eager_loading()
    demo_core_aggregation()