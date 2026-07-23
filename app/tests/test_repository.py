import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import Author, Book
from app.repository import BookRepository

TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_repository_add_and_get(db_session):
    repo = BookRepository(db_session)
    
    author = Author(name="Тестовый Автор")
    db_session.add(author)
    db_session.commit()
    
    book = Book(title="Тестовая Книга", author_id=author.id)
    saved_book = repo.add(book)
    
    assert saved_book.id is not None
    assert saved_book.title == "Тестовая Книга"
    
    books = repo.get_by_author_id(author.id)
    assert len(books) == 1
    assert books[0].title == "Тестовая Книга"

def test_repository_delete(db_session):
    repo = BookRepository(db_session)
    
    author = Author(name="Автор для удаления")
    db_session.add(author)
    db_session.commit()
    
    book = Book(title="Книга для удаления", author_id=author.id)
    saved_book = repo.add(book)
    
    result = repo.delete_by_id(saved_book.id)
    assert result is True
    assert repo.get_by_author_id(author.id) == []
