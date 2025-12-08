"""
Script defining SQLAlchemy models for the Book API.
"""

from typing import Optional
from sqlalchemy import UniqueConstraint, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


# Base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass


# Book model representing the "books" table
class Book(Base):
    __tablename__ = "books"

    # Unique constraint to ensure no duplicate books
    # uix_title_author is the name of the unique constraint
    __table_args__ = (UniqueConstraint("title", "author", name="uix_title_author"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    author: Mapped[str] = mapped_column(String(250), nullable=False, index=True)
    year: Mapped[Optional[int]] = mapped_column(index=True)

    # String representation of the Book model,
    # for easier debugging and logging
    def __repr__(self) -> str:
        return (
            f"Book(id={self.id!r}, title={self.title!r}, "
            f"author={self.author!r}, year={self.year!r})"
        )
