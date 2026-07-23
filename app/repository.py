from sqlalchemy.orm import Session
from app.models import Book

class BookRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def add(self, book: Book) -> Book:
        """Добавление новой книги"""
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def get_by_author_id(self, author_id: int) -> list[Book]:
        """Получение всех книг автора по его id"""
        return self.db.query(Book).filter(Book.author_id == author_id).all()

    def delete_by_id(self, book_id: int) -> bool:
        """Удаление книги по её id"""
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if book:
            self.db.delete(book)
            self.db.commit()
            return True
        return False
