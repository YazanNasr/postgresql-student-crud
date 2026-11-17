"""Database connection configuration for the application."""

import os
from contextlib import contextmanager
from typing import Iterator

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

# Load local settings from .env while allowing real environment variables to win.
load_dotenv()


def get_connection() -> psycopg.Connection:
    """Create a PostgreSQL connection using environment-based configuration."""
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "student_crud"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),
        row_factory=dict_row,
    )


@contextmanager
def db_connection() -> Iterator[psycopg.Connection]:
    """Open a connection and guarantee that it is closed after an operation.

    Psycopg's connection context commits successful work and rolls back when an
    exception occurs. The outer ``closing`` behavior is made explicit here so
    every CRUD function follows the same safe resource-management pattern.
    """
    connection = get_connection()
    try:
        with connection:
            yield connection
    finally:
        connection.close()

