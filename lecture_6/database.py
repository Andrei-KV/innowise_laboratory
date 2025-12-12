"""
This module sets up the database connection
and session management for the Book API application.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database connection URI
SQL_URI = "sqlite+pysqlite:///./books.db"

# Create the SQLAlchemy engine -
# this manages the connection to the database
engine = create_engine(SQL_URI, connect_args={"check_same_thread": False}, echo=True)

# Create a configured "Session" class,
# which will be used to create session objects
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
