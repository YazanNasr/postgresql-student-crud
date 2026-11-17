"""Unit tests for CRUD SQL, parameters, results, and input validation."""

from contextlib import contextmanager
from datetime import date
from unittest.mock import MagicMock, patch

import pytest

from app import student_repository as repository


@contextmanager
def fake_database(fetchone=None, fetchall=None):
    """Supply a cursor-shaped test double without requiring a PostgreSQL server."""
    cursor = MagicMock()
    cursor.fetchone.return_value = fetchone
    cursor.fetchall.return_value = fetchall or []
    cursor.__enter__.return_value = cursor
    connection = MagicMock()
    connection.cursor.return_value = cursor
    yield connection


def student(student_id=4, email="sam@example.com"):
    """Return a representative database row for test assertions."""
    return {
        "student_id": student_id,
        "first_name": "Sam",
        "last_name": "Lee",
        "email": email,
        "enrollment_date": date(2026, 1, 10),
    }


def test_get_all_students_orders_and_returns_rows(capsys):
    rows = [student()]
    with patch.object(repository, "db_connection", return_value=fake_database(fetchall=rows)):
        assert repository.getAllStudents() == rows
    assert "Sam Lee" in capsys.readouterr().out


def test_add_student_uses_parameters_and_returns_created_row():
    created = student()
    database = fake_database(fetchone=created)
    with patch.object(repository, "db_connection", return_value=database):
        assert repository.addStudent("Sam", "Lee", "sam@example.com", date(2026, 1, 10)) == created


def test_update_student_email_returns_updated_row():
    updated = student(email="new@example.com")
    with patch.object(repository, "db_connection", return_value=fake_database(fetchone=updated)):
        assert repository.updateStudentEmail(4, "new@example.com") == updated


def test_delete_student_returns_deleted_row():
    deleted = student()
    with patch.object(repository, "db_connection", return_value=fake_database(fetchone=deleted)):
        assert repository.deleteStudent(4) == deleted


def test_update_and_delete_return_none_for_missing_id():
    with patch.object(repository, "db_connection", return_value=fake_database()):
        assert repository.updateStudentEmail(999, "new@example.com") is None
    with patch.object(repository, "db_connection", return_value=fake_database()):
        assert repository.deleteStudent(999) is None


@pytest.mark.parametrize("bad_id", [0, -1, True, "1"])
def test_invalid_student_ids_are_rejected(bad_id):
    with pytest.raises(ValueError):
        repository.deleteStudent(bad_id)


@pytest.mark.parametrize("bad_text", ["", "   ", None])
def test_empty_required_text_is_rejected(bad_text):
    with pytest.raises(ValueError):
        repository.addStudent(bad_text, "Lee", "sam@example.com", date.today())

