"""CRUD functions for records in the PostgreSQL ``students`` table."""

from datetime import date
from typing import Any

from app.db import db_connection

Student = dict[str, Any]


def getAllStudents() -> list[Student]:
    """Retrieve all students in primary-key order and display each record."""
    with db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT student_id, first_name, last_name, email, enrollment_date
                FROM students
                ORDER BY student_id;
                """
            )
            students = list(cursor.fetchall())

    # Displaying records here satisfies the assignment's required function behavior.
    if not students:
        print("No students found.")
    else:
        for student in students:
            print(_format_student(student))
    return students


def addStudent(
    first_name: str,
    last_name: str,
    email: str,
    enrollment_date: date,
) -> Student:
    """Insert a student with parameterized SQL and return the created record."""
    _require_text(first_name, "first_name")
    _require_text(last_name, "last_name")
    _require_text(email, "email")

    with db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO students (first_name, last_name, email, enrollment_date)
                VALUES (%s, %s, %s, %s)
                RETURNING student_id, first_name, last_name, email, enrollment_date;
                """,
                (first_name.strip(), last_name.strip(), email.strip(), enrollment_date),
            )
            student = cursor.fetchone()

    if student is None:  # Defensive check: INSERT ... RETURNING should always return one row.
        raise RuntimeError("PostgreSQL did not return the inserted student.")
    print(f"Added: {_format_student(student)}")
    return student


def updateStudentEmail(student_id: int, new_email: str) -> Student | None:
    """Update one student's email and return it, or return None if the ID is absent."""
    _require_positive_id(student_id)
    _require_text(new_email, "new_email")

    with db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE students
                SET email = %s
                WHERE student_id = %s
                RETURNING student_id, first_name, last_name, email, enrollment_date;
                """,
                (new_email.strip(), student_id),
            )
            student = cursor.fetchone()

    if student is None:
        print(f"No student found with ID {student_id}; nothing was updated.")
    else:
        print(f"Updated: {_format_student(student)}")
    return student


def deleteStudent(student_id: int) -> Student | None:
    """Delete one student and return it, or return None if the ID is absent."""
    _require_positive_id(student_id)

    with db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM students
                WHERE student_id = %s
                RETURNING student_id, first_name, last_name, email, enrollment_date;
                """,
                (student_id,),
            )
            student = cursor.fetchone()

    if student is None:
        print(f"No student found with ID {student_id}; nothing was deleted.")
    else:
        print(f"Deleted: {_format_student(student)}")
    return student


def _require_text(value: str, field_name: str) -> None:
    """Reject empty strings before they reach PostgreSQL."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


def _require_positive_id(student_id: int) -> None:
    """Reject invalid primary-key values with a clear application error."""
    if not isinstance(student_id, int) or isinstance(student_id, bool) or student_id <= 0:
        raise ValueError("student_id must be a positive integer.")


def _format_student(student: Student) -> str:
    """Build a compact, readable representation for terminal demonstrations."""
    return (
        f"ID={student['student_id']} | "
        f"{student['first_name']} {student['last_name']} | "
        f"{student['email']} | enrolled {student['enrollment_date']}"
    )

