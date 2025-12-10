"""
Main application file for Book API using FastAPI.
"""

from typing import Annotated, Any, List
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query, Depends, status, HTTPException
import models
import schemas
from database import engine, SessionLocal
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete


# Function to create database tables
def create_db() -> None:
    models.Base.metadata.create_all(bind=engine)


# Database context manager
class DataBaseContextManager:
    def __init__(self):
        self.db = SessionLocal()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()


# Dependency to get DB session
def get_session():
    with DataBaseContextManager() as db:
        yield db


# Type alias for session dependency
SessionDep = Annotated[Any, Depends(get_session)]


# Lifespan event handler
# How does it work:
# 1. Code before yield runs on startup
# 2. Code after yield runs on shutdown
# 3. If no code after yield, just startup code runs
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    create_db()
    yield
    # Shutdown code
    engine.dispose()


# Create FastAPI app instance
app = FastAPI(lifespan=lifespan)

"""
API endpoint definitions for Book API.
"""


# Endpoint to add a new book
@app.post(
    "/books/",
    response_model=schemas.BookResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["books"],
    summary="Add new book",
    response_description="Yes, it's done",
)
def add_book(book: schemas.BookAdd, session: SessionDep) -> schemas.BookResponse:
    """
    Add new book: \n
    **title**: str (required) \n
    **author**: str (required) \n
    **year**: int (optional)
    """
    new_book = models.Book(**book.model_dump())
    session.add(new_book)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Book with the title {book.title} and author {book.author} already exists.",
        )

    # To receive the generated ID
    session.refresh(new_book)
    return new_book


# Endpoint to get all books with pagination
@app.get(
    "/books/",
    response_model=List[schemas.BookResponse],
    status_code=status.HTTP_200_OK,
    tags=["books"],
    summary="Get all books with pagination",
    response_description="Yes, it's done",
)
def read_books(
    session: SessionDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
) -> List[schemas.BookResponse]:
    """
    Get all books with pagination
    """
    stmt = select(models.Book).offset(skip).limit(limit)
    books = session.execute(stmt).scalars().all()
    return books


# Endpoint to search books
@app.get(
    "/books/search/",
    response_model=List[schemas.BookResponse],
    status_code=status.HTTP_200_OK,
    tags=["books"],
    summary="Search books by title, or author, or year",
    response_description="Yes, it's done",
)
def search_books(
    session: SessionDep,
    title: str | None = Query(None),
    author: str | None = Query(None),
    year: int | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
) -> List[schemas.BookResponse]:
    """
    Search books by title, or author, or year
    """
    # Validation - at least one search criterion must be provided
    if not any([title, author, year]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one search criterion must be provided.",
        )

    stmt = select(models.Book)
    if title:
        stmt = stmt.where(models.Book.title.ilike(f"%{title}%"))
    if author:
        stmt = stmt.where(models.Book.author.ilike(f"%{author}%"))
    if year:
        stmt = stmt.where(models.Book.year == year)
    stmt = stmt.offset(skip).limit(limit)
    books = session.execute(stmt).scalars().all()
    # Tips:
    # .scalars().all() to get list of Book objects
    # just .all() would return list of tuples (Raw results)
    return books


# Endpoint to delete a book by ID
@app.delete(
    "/books/{book_id}",
    status_code=status.HTTP_200_OK,
    tags=["books"],
    summary="Delete book by ID",
    response_description="Yes, it's done",
)
def delete_book(book_id: int, session: SessionDep):
    """
    Delete book by ID
    """
    stmt = select(models.Book).where(models.Book.id == book_id)
    existing_book = session.execute(stmt).scalars().first()
    if not existing_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found.",
        )
    stmt = delete(models.Book).where(models.Book.id == book_id)
    session.execute(stmt)
    session.commit()
    return {"message": f"Book with id {book_id} deleted."}


# Endpoint to update a book by ID
@app.put(
    "/books/{book_id}",
    response_model=schemas.BookResponse,
    status_code=status.HTTP_200_OK,
    tags=["books"],
    summary="Update book by ID",
    response_description="Yes, it's done",
)
def update_book(
    book_id: int, book: schemas.BookUpdate, session: SessionDep
) -> schemas.BookResponse:
    """
    Update book by ID
    """
    stmt = select(models.Book).where(models.Book.id == book_id)
    existing_book = session.execute(stmt).scalars().first()
    if not existing_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found.",
        )
    update_data = book.model_dump(exclude_unset=True)
    # Tip: exclude_unset=True to get only provided fields
    # Tip: model_dump() to convert Pydantic model to dict

    for key, value in update_data.items():
        setattr(existing_book, key, value)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Book with the title {book.title} and author {book.author} already exists.",
        )
    # To receive the generated ID
    session.refresh(existing_book)
    return existing_book
