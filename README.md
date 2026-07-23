# 🐘 DZ28 — Продвинутая Алхимия (Advanced SQLAlchemy)

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-green.svg)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/Alembic-1.18+-orange.svg)](https://alembic.sqlalchemy.org/)
[![Pytest](https://img.shields.io/badge/Pytest-9.1+-purple.svg)](https://pytest.org/)
[![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)]()

**Автор:** Виктор Куличенко  
**Занятие:** #28 — Алхимия: Оптимизация, транзакции, миграции  
**Статус:** ✅ Завершено

---

## 📌 О проекте

Проект демонстрирует **продвинутое использование SQLAlchemy** для работы с базами данных в Python-приложениях. Освоены сложные аспекты ORM: оптимизация запросов (решение проблемы N+1), управление транзакциями, паттерн Repository и миграции через Alembic.

### 🎯 Ключевые возможности:
- ✅ Оптимизация загрузки данных (Lazy vs Eager Loading)
- ✅ Управление транзакциями и откаты (Rollback)
- ✅ Паттерн проектирования Repository
- ✅ Миграции базы данных через Alembic
- ✅ Объединение SQLAlchemy ORM и Core
- ✅ Автоматическое логирование SQL-запросов
- ✅ Юнит-тесты с pytest и изолированной БД

---

## 🚀 Быстрый старт

### 1. Клонирование и настройка окружения
``` bash
git clone https://github.com/VictorKVS/DZ_28_Alchemy.git
cd DZ_28_Alchemy
python -m venv venv
venv\\Scripts\\activate  # Windows
# source venv/bin/activate  # Linux/macOS
pip install sqlalchemy alembic pytest
```

### 2. Запуск демонстраций

#### Задача 1: Оптимизация N+1 и SQLAlchemy Core
``` bash
python scripts/task1_optimization.py
```
**Ожидаемый результат:**
- Ленивая загрузка: 2+ SQL-запросов (проблема N+1)
- Жадная загрузка (joinedload): 1 SQL-запрос с JOIN
- Core агрегация: быстрый COUNT через func.count()

#### Задача 2: Транзакции и Rollback
``` bash
python scripts/task2_transactions.py
```
**Ожидаемый результат:**
- Добавление 2 валидных пользователей
- Имитация ошибки (UNIQUE constraint violation)
- Автоматический rollback — в БД остается 0 записей

#### Задача 4: Тесты Repository
``` bash
pytest app/tests/test_repository.py -v
```
**Ожидаемый результат:**
```
test_repository_add_and_get PASSED  [ 50%]
test_repository_delete PASSED        [100%]
============================== 2 passed ===============================
```

### 3. Работа с миграциями (Alembic)
``` bash
# Создание миграции
alembic revision --autogenerate -m "описание изменений"

# Применение миграций
alembic upgrade head

# Откат последней миграции
alembic downgrade -1

# Просмотр истории
alembic history
```

---

## 📋 Выполненные задачи

### ✅ Задача 1: Оптимизация загрузки данных (N+1 Problem)

**Проблема:** При ленивой загрузке (lazy="select") SQLAlchemy генерирует отдельный SQL-запрос для каждого связанного объекта.

**Решение:** Использование \joinedload\ для жадной загрузки через SQL JOIN.

``` python
# ❌ Ленивая загрузка (N+1 запросов)
authors = session.query(Author).all()
for author in authors:
    for book in author.books:  # Отдельный SELECT для каждого автора!
        print(book.title)

# ✅ Жадная загрузка (1 запрос с JOIN)
from sqlalchemy.orm import joinedload
authors = session.query(Author).options(joinedload(Author.books)).all()
for author in authors:
    for book in author.books:  # Данные уже в памяти!
        print(book.title)
```

**SQL-логи:**
``` sql
-- Ленивая загрузка (3 запроса):
SELECT * FROM authors;
SELECT * FROM books WHERE author_id = 1;
SELECT * FROM books WHERE author_id = 2;

-- Жадная загрузка (1 запрос):
SELECT authors.*, books.* 
FROM authors 
LEFT OUTER JOIN books ON authors.id = books.author_id;
```

---

### ✅ Задача 2: Транзакции и Rollback

**Сценарий:** Добавление нескольких записей с имитацией ошибки и автоматическим откатом.

``` python
from sqlalchemy.exc import IntegrityError

with SessionLocal() as session:
    try:
        session.add(User(username="user1", email="user1@test.com"))
        session.add(User(username="user2", email="user2@test.com"))
        session.add(User(username="user3", email="user1@test.com"))  # Дубликат!
        session.commit()
    except IntegrityError as e:
        print(f"Ошибка: {e.orig}")
        session.rollback()  # Откат ВСЕХ изменений в сессии
```
**Результат:**
```
➕ Добавляем 2-х валидных пользователей...
❌ Имитируем ошибку: нарушаем UNIQUE constraint на email...
⚠️ Перехвачена ошибка: UNIQUE constraint failed: users.email
🔄 Выполняем session.rollback()...
📊 Пользователей в базе после отката: 0 (Ожидалось: 0)
```

---

### ✅ Задача 3: Миграции через Alembic

**Шаги:**
1. Инициализация Alembic
2. Создание первой миграции (все таблицы)
3. Изменение модели (добавление \price\, удаление \created_at\)
4. Создание второй миграции
5. Применение и откат миграций

**История миграций:**
```
47e7d83e37be -> d247a0c757a1 (head), add price and remove created_at from order
<base> -> 47e7d83e37be, initial tables: authors, books, users, orders
```

**Команды:**
``` bash
alembic revision --autogenerate -m "initial tables"
alembic upgrade head
alembic downgrade -1
alembic history
```
---

### ✅ Задача 4: Паттерн Repository

**Класс BookRepository:**
``` python
class BookRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def add(self, book: Book) -> Book:
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def get_by_author_id(self, author_id: int) -> list[Book]:
        return self.db.query(Book).filter(Book.author_id == author_id).all()

    def delete_by_id(self, book_id: int) -> bool:
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if book:
            self.db.delete(book)
            self.db.commit()
            return True
        return False
```

**Тесты (pytest):**
``` python
def test_repository_add_and_get(db_session):
    repo = BookRepository(db_session)
    book = Book(title="Тестовая Книга", author_id=1)
    saved_book = repo.add(book)
    assert saved_book.id is not None
    books = repo.get_by_author_id(1)
    assert len(books) == 1
```

---

## 🎁 Бонусные задания

### ✅ Бонус 1: Логирование SQL-запросов

**Настройка:**
``` python
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

engine = create_engine(DATABASE_URL, echo=True)
```

**Результат:** Все SQL-запросы выводятся в консоль с параметрами и временем выполнения.

---

### ✅ Бонус 2: Объединение ORM и Core

**Пример:** Использование SQLAlchemy Core для агрегирующих запросов.

``` python
from sqlalchemy import select, func

# Быстрый подсчет без загрузки объектов ORM
stmt = select(func.count(Book.id))
total_books = session.execute(stmt).scalar()
print(f"Общее количество книг: {total_books}")
```

**Преимущество:** Core-запросы выполняются быстрее, так как не создают Python-объекты.

---

## 🏗️ Архитектура проекта

### Модель данных (UML)

``` mermaid

classDiagram
    %% === ИНФРАСТРУКТУРА ===
    class Base {
        <<Declarative Base>>
        +metadata: MetaData
    }
    
    class Session {
        <<SQLAlchemy>>
        +add()
        +commit()
        +rollback()
        +flush()
        +query()
    }

    %% === МОДЕЛИ ДАННЫХ ===
    class Author {
        +int id
        +string name
        +list~Book~ books
    }
    
    class Book {
        +int id
        +string title
        +int author_id
        +Author author
    }
    
    class User {
        +int id
        +string username
        +string email
        <<Изолирована: демо транзакций>>
    }
    
    class Order {
        +int id
        +string product_name
        +int quantity
        +datetime created_at
        <<Изолирована: демо Alembic>>
    }

    %% === ПАТТЕРНЫ ===
    class BookRepository {
        +add(book) Book
        +get_by_author_id(id) List~Book~
        +delete_by_id(id) bool
    }

    %% === РЕАЛЬНЫЕ СВЯЗИ ===
    Author "1" *-- "0..*" Book : пишет (One-to-Many)
    Book "0..*" --> "1" Author : принадлежит (ForeignKey)
    
    %% === ИСПОЛЬЗОВАНИЕ ===
    BookRepository ..> Session : использует
    BookRepository ..> Book : управляет
    Base <|-- Author : наследует
    Base <|-- Book : наследует
    Base <|-- User : наследует
    Base <|-- Order : наследует
---

### Поток данных: Оптимизация N+1

``` mermaid
sequenceDiagram
    participant App as Приложение
    participant ORM as SQLAlchemy ORM
    participant DB as База данных
    
    Note over App,DB: Ленивая загрузка (N+1)
    App->>ORM: query(Author).all()
    ORM->>DB: SELECT * FROM authors
    DB-->>ORM: [Author1, Author2]
    App->>ORM: author1.books
    ORM->>DB: SELECT * FROM books WHERE author_id=1
    App->>ORM: author2.books
    ORM->>DB: SELECT * FROM books WHERE author_id=2
    Note over App,DB: 3 запроса!
    
    Note over App,DB: Жадная загрузка (joinedload)
    App->>ORM: query(Author).options(joinedload(Author.books)).all()
    ORM->>DB: SELECT authors.*, books.* FROM authors LEFT JOIN books
    DB-->>ORM: Все данные одним запросом
    Note over App,DB: 1 запрос!
```

---

## 📂 Структура проекта

```text
DZ_28_Alchemy/
├── app/
│   ├── database.py              # Настройка engine, sessionmaker, Base
│   ├── models.py                # SQLAlchemy модели (Author, Book, User, Order)
│   ├── repository.py            # Паттерн Repository (BookRepository)
│   └── tests/
│       └── test_repository.py   # pytest тесты для Repository
├── scripts/
│   ├── task1_optimization.py    # Демонстрация N+1 и joinedload
│   └── task2_transactions.py    # Демонстрация транзакций и rollback
├── alembic/                     # Миграции базы данных
│   ├── versions/                # Файлы миграций
│   └── env.py                   # Конфигурация Alembic
├── alembic.ini                  # Настройки Alembic
├── app.db                       # SQLite база данных
└── README.md                    # Этот файл
```

---

## 🔐 Модель безопасности

### Управление сессиями
| Метод | Назначение | Когда использовать |
|-------|------------|-------------------|
| \session.add()\ | Добавление объекта в сессию | Перед commit |
| \session.commit()\ | Фиксация транзакции | После успешных операций |
| \session.rollback()\ | Откат транзакции | При ошибках (IntegrityError) |
| \session.flush()\ | Применение изменений без commit | Для получения ID до commit |
| \session.close()\ | Закрытие сессии | В конце работы (finally) |

### Best Practices
✅ **Реализовано:**
- Использование context manager (\with SessionLocal() as session\) для автоматического закрытия
- Обработка \IntegrityError\ с автоматическим rollback
- Паттерн Repository для изоляции логики доступа к данным
- Изолированные тесты с in-memory SQLite базой

---

## 🛠️ Стек технологий

| Категория | Технология | Версия / Назначение |
|-----------|------------|---------------------|
| **ORM** | SQLAlchemy | 2.0.51 |
| **Миграции** | Alembic | 1.18.5 |
| **Тестирование** | pytest | 9.1.1 |
| **База данных** | SQLite | Встроенная |
| **Python** | Python | 3.10+ |

---

## 📊 Статистика проекта

| Показатель | Количество | Детали |
|------------|------------|--------|
| 🗄️ **Моделей данных** | 4 | Author, Book, User, Order |
| 📝 **Скриптов демонстрации** | 2 | Оптимизация, Транзакции |
| 🧪 **Unit-тестов** | 2 | Repository add/get/delete |
| 🔄 **Миграций** | 2 | Initial + Schema change |
| 📚 **Паттернов** | 1 | Repository Pattern |

---

## 👤 Тестовые данные

После запуска скриптов в базе создаются:

| Таблица | Записи | Описание |
|---------|--------|----------|
| **authors** | 1 | Фрэнк Герберт |
| **books** | 2 | Дюна, Мессия Дюны |
| **users** | 0 | Очищается после rollback |
| **orders** | 0 | Таблица для демонстрации миграций |

---

## 🎯 Ключевые выводы

### 1. Оптимизация запросов
- **Lazy loading** приводит к проблеме N+1 (много мелких запросов)
- **Eager loading** (joinedload) решает проблему одним JOIN-запросом
- Используйте \echo=True\ для анализа генерируемого SQL

### 2. Транзакции
- Всегда оборачивайте операции в \	ry/except\
- При ошибках вызывайте \session.rollback()\
- Используйте context manager для автоматического \close()\

### 3. Миграции
- Alembic автоматически отслеживает изменения моделей
- Миграции версионируются и могут быть откачены
- Используйте \--autogenerate\ для создания миграций

### 4. Паттерн Repository
- Изолирует логику доступа к данным
- Упрощает тестирование (mock сессий)
- Следует принципу единственной ответственности (SRP)

---

## 👤 Автор

**Viktor Kulichenko**  
*Software Engineer / Information Security Specialist*  
[GitHub](https://github.com/VictorKVS)

---

*© 2026 Виктор Куличенко. Проект выполнен в рамках курса "Python-разработчик I".*
