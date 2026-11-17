"""Command-line entry point and complete CRUD demonstration."""

import argparse
import sys
from datetime import date
from uuid import uuid4

import psycopg

from app.student_repository import (
    addStudent,
    deleteStudent,
    getAllStudents,
    updateStudentEmail,
)


def run_demo(pause: bool = False) -> None:
    """Run all required functions in a visible create/read/update/delete sequence.

    The optional pauses give the presenter time to refresh pgAdmin and visibly
    prove each database change, as required by the grading rubric.
    """
    unique_suffix = uuid4().hex[:8]
    original_email = f"video.student.{unique_suffix}@example.com"
    updated_email = f"video.student.updated.{unique_suffix}@example.com"

    print("\n1) READ: initial records")
    getAllStudents()

    print("\n2) CREATE: add one temporary student")
    created = addStudent("Video", "Student", original_email, date.today())
    print("\nRecords after CREATE:")
    getAllStudents()
    _pause_for_pgadmin(pause, "CREATE")

    print("\n3) UPDATE: change the temporary student's email")
    updateStudentEmail(created["student_id"], updated_email)
    print("\nRecords after UPDATE:")
    getAllStudents()
    _pause_for_pgadmin(pause, "UPDATE")

    print("\n4) DELETE: remove the temporary student")
    deleteStudent(created["student_id"])
    print("\nRecords after DELETE (back to the initial data):")
    getAllStudents()
    _pause_for_pgadmin(pause, "DELETE")

    print("\nCRUD demonstration completed successfully.")


def build_parser() -> argparse.ArgumentParser:
    """Define commands so every CRUD function can also be run independently."""
    parser = argparse.ArgumentParser(description="PostgreSQL student CRUD application")
    commands = parser.add_subparsers(dest="command", required=True)
    demo = commands.add_parser("demo", help="run a complete CRUD demonstration")
    demo.add_argument(
        "--pause",
        action="store_true",
        help="pause after each write so its effect can be shown in pgAdmin",
    )
    commands.add_parser("list", help="display all students")

    add = commands.add_parser("add", help="add a student")
    add.add_argument("first_name")
    add.add_argument("last_name")
    add.add_argument("email")
    add.add_argument("enrollment_date", type=date.fromisoformat, help="YYYY-MM-DD")

    update = commands.add_parser("update-email", help="update a student's email")
    update.add_argument("student_id", type=int)
    update.add_argument("new_email")

    delete = commands.add_parser("delete", help="delete a student")
    delete.add_argument("student_id", type=int)
    return parser


def main() -> int:
    """Parse the selected command and report database errors cleanly."""
    args = build_parser().parse_args()
    try:
        if args.command == "demo":
            run_demo(args.pause)
        elif args.command == "list":
            getAllStudents()
        elif args.command == "add":
            addStudent(args.first_name, args.last_name, args.email, args.enrollment_date)
        elif args.command == "update-email":
            updateStudentEmail(args.student_id, args.new_email)
        elif args.command == "delete":
            deleteStudent(args.student_id)
        return 0
    except (psycopg.Error, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


def _pause_for_pgadmin(enabled: bool, operation: str) -> None:
    """Pause a recorded demo while the presenter verifies a write in pgAdmin."""
    if enabled:
        input(
            f"\nRefresh the students table in pgAdmin to show the {operation} effect, "
            "then press Enter to continue..."
        )


if __name__ == "__main__":
    raise SystemExit(main())
