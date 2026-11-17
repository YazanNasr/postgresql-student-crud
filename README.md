# PostgreSQL Student CRUD Application

This Python application connects to PostgreSQL and implements the four functions
required by the assignment:

- `getAllStudents()` retrieves and displays every student.
- `addStudent(first_name, last_name, email, enrollment_date)` inserts a student.
- `updateStudentEmail(student_id, new_email)` updates a student's email.
- `deleteStudent(student_id)` deletes a student.

All write operations use parameterized SQL, PostgreSQL transactions, and
`RETURNING` so the affected record can be shown immediately. The database schema
enforces the required primary key, identity/auto-increment behavior, `NOT NULL`
fields, unique email, and date type.

## Project structure

```text
postgresql-student-crud/
├── app/
│   ├── db.py
│   └── student_repository.py
├── database/
│   ├── create_database.sql
│   └── schema.sql
├── tests/
│   └── test_student_repository.py
├── .env.example
├── main.py
├── VIDEO_SCRIPT.md
├── requirements.txt
└── requirements-dev.txt
```

## Requirements

- Python 3.10 or newer
- PostgreSQL and pgAdmin 4
- A terminal opened in this project directory

## Database setup with pgAdmin

1. Open pgAdmin and connect to your PostgreSQL server.
2. Right-click **Databases**, choose **Create > Database**, name it
   `student_crud`, and save it. (Alternatively, run
   `database/create_database.sql` while connected to the default `postgres`
   database.)
3. Select `student_crud`, open **Query Tool**, load `database/schema.sql`, and
   execute it.
4. Confirm that the result grid contains John Doe, Jane Smith, and Jim Beam.

## Application setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, activate it with:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies, create a local configuration file, and enter your real
PostgreSQL password in `.env`:

```bash
python -m pip install -r requirements.txt
cp .env.example .env
```

Windows users can replace the last command with `copy .env.example .env`.
Never commit `.env`; it is excluded by `.gitignore`.

## Run the complete demonstration

```bash
python main.py demo
```

The demo visibly performs READ, CREATE, UPDATE, and DELETE. It uses a unique
temporary email and deletes the temporary row at the end, leaving the three
initial records intact.

For the recorded video, use pause mode:

```bash
python main.py demo --pause
```

After each write, the application waits while you refresh the `students` table
in pgAdmin and show the grader the CREATE, UPDATE, or DELETE effect.

Individual commands are also available:

```bash
python main.py list
python main.py add "Alex" "Taylor" "alex.taylor@example.com" 2026-11-16
python main.py update-email 4 "alex.new@example.com"
python main.py delete 4
```

## Run the tests

The automated tests do not need a live database; they verify function behavior,
result handling, and validation with a controlled database test double.

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

For the final integration check, run `python main.py demo` against the configured
PostgreSQL database and confirm the same changes in pgAdmin.

## Demonstration video

Video link: **REPLACE THIS TEXT WITH THE VIEWABLE VIDEO URL BEFORE SUBMITTING**

Use the complete, timed recording guide in [`VIDEO_SCRIPT.md`](VIDEO_SCRIPT.md).

The recording must be no longer than five minutes. Show, in order:

1. `students` table design in pgAdmin, including columns and constraints.
2. The three provided initial rows in pgAdmin.
3. `python main.py demo --pause` running in the terminal.
4. Refresh/select the table in pgAdmin after CREATE, UPDATE, and DELETE so each
   database effect is visible.
5. The GitHub repository and its README, including the working video link.

## Troubleshooting

- **Connection refused:** start PostgreSQL and verify host/port in `.env`.
- **Password authentication failed:** correct `POSTGRES_USER` and
  `POSTGRES_PASSWORD` in `.env`.
- **Database does not exist:** create `student_crud` before running the schema.
- **Relation `students` does not exist:** run `database/schema.sql` in the
  `student_crud` database, not in the default `postgres` database.
- **Duplicate email:** use a different email; uniqueness is required by the schema.

## Submission checklist

- Public GitHub repository contains the application, SQL scripts, and README.
- `.env` and passwords are not committed.
- Video is at most five minutes and its sharing setting allows the instructor to view it.
- Working video URL replaces the placeholder above.
- GitHub repository URL is submitted through Brightspace.
