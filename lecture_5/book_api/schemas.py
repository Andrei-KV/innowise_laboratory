"""
Script defining Pydantic schemas for the Book API.
It is used for data validation and serialization.
"""

from typing_extensions import Self
from pydantic import BaseModel, ConfigDict, model_validator, field_validator
from datetime import date


# Base schema for book
class BookBase(BaseModel):
    title: str | None = None
    author: str | None = None
    year: int | None = None

    # Validator to ensure year is between 0 and current year
    @field_validator("year")
    @classmethod
    def validate_year(cls, val: int | None) -> int | None:
        if val is not None:
            current_year = date.today().year
            if val < 0 or val > current_year:
                raise ValueError(f"Year must be between 0 and {current_year}.")
        return val

    # Validator to ensure title and author are not empty strings
    @field_validator("title", "author")
    @classmethod
    def validate_non_empty_string(cls, val: str | None) -> str | None:
        if val is not None and isinstance(val, str) and val.strip() == "":
            raise ValueError("Field cannot be empty string")
        return val


# Schema for book response
class BookResponse(BookBase):
    id: int

    # Enable ORM mode
    # This is instructing Pydantic to read data
    # even if it is not a dict, but an ORM model
    model_config = ConfigDict(from_attributes=True)


# Schema for adding a new book
class BookAdd(BookBase):
    title: str
    author: str

    @model_validator(mode="before")
    @classmethod
    def check_required_fields(cls, data: dict) -> dict:
        """Validate that required fields are provided with custom error messages"""
        errors = []

        # Check if title is missing or None
        if not data.get("title"):
            errors.append("Field 'title' is required")

        # Check if author is missing or None
        if not data.get("author"):
            errors.append("Field 'author' is required")

        if errors:
            # Combine all error messages
            error_message = ". ".join(errors) + "."
            raise ValueError(error_message)

        return data


# Schema for updating a book
class BookUpdate(BookBase):
    # Validator to ensure at least one field is provided
    @model_validator(mode="after")
    def at_least_one_field(self) -> Self:
        if not any([self.title, self.author, self.year]):
            raise ValueError("At least one update criterion must be provided.")
        return self


# Schema for searching books
class BookSearch(BookBase):
    # Validator to ensure at least one field is provided
    @model_validator(mode="after")
    def at_least_one_field(self) -> Self:
        if not any([self.title, self.author, self.year]):
            raise ValueError("At least one search criterion must be provided.")
        return self
