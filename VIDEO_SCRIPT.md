# Demonstration Video Script (Maximum 5 Minutes)

Use this script while recording. The rubric says the video is the primary grading
evidence, so keep the terminal and pgAdmin text large and readable. Record the
entire screen, but hide passwords, notifications, and unrelated windows.

## Before recording

1. Complete the database and application setup in `README.md`.
2. Run `python main.py demo` once without recording to confirm the connection.
3. Rerun `database/schema.sql` if necessary so the three required initial records
   are present.
4. Open two windows side by side:
   - pgAdmin Query Tool connected to the `student_crud` database.
   - A terminal in the project directory with the virtual environment active.
5. Put this query in pgAdmin and keep it ready to execute:

   ```sql
   SELECT student_id, first_name, last_name, email, enrollment_date
   FROM students
   ORDER BY student_id;
   ```

## Timed recording script

### 0:00-0:15 - Introduction

**Show:** The GitHub repository or the project folder.

**Say:**

> This project is a Python application connected to PostgreSQL. It implements
> the required students table and the four CRUD functions: getAllStudents,
> addStudent, updateStudentEmail, and deleteStudent.

### 0:15-0:50 - Database schema and constraints

**Show:** In pgAdmin, expand `student_crud > Schemas > public > Tables > students`
and show the columns and constraints. If the constraints are easier to read in
the Query Tool, briefly open `database/schema.sql`.

**Say:**

> The students table uses an auto-incrementing integer primary key. First name,
> last name, and email are not null. Email is unique, and enrollment date uses
> the date type. These match the provided schema.

Make sure the screen visibly shows:

- `student_id` as the primary key and identity/auto-increment column.
- `first_name`, `last_name`, and `email` as `NOT NULL`.
- The unique constraint on `email`.
- `enrollment_date` as `DATE`.

### 0:50-1:10 - Initial data

**Show:** Execute the prepared `SELECT` query in pgAdmin.

**Say:**

> The table contains the exact initial data: John Doe and Jane Smith enrolled on
> September 1, 2023, and Jim Beam enrolled on September 2, 2023.

Keep all three rows visible long enough to read.

### 1:10-1:35 - Start the application and demonstrate READ

**Show:** In the terminal run:

```bash
python main.py demo --pause
```

**Say:**

> The application first calls getAllStudents. It executes a SELECT query and
> displays every student ordered by student ID. The three initial rows are shown
> in the terminal.

### 1:35-2:15 - Demonstrate CREATE

The application calls `addStudent`, displays the inserted record, lists all
students, and pauses.

**Say:**

> Next, addStudent inserts a temporary student using parameterized SQL. PostgreSQL
> generates the new student ID, and the application returns and displays the
> complete inserted row.

**While paused:** Switch to pgAdmin and execute the prepared `SELECT` query.

**Say:**

> Refreshing the database confirms that the new Video Student row was actually
> inserted.

Keep the new row visible, then return to the terminal and press Enter.

### 2:15-2:55 - Demonstrate UPDATE

The application calls `updateStudentEmail`, lists all students, and pauses.

**Say:**

> updateStudentEmail targets the generated student ID and changes only that
> student's email. The function returns and displays the updated row.

**While paused:** Execute the same pgAdmin `SELECT` query again.

**Say:**

> The pgAdmin result now shows the updated email, proving the database update.

Keep the changed email visible, then return to the terminal and press Enter.

### 2:55-3:35 - Demonstrate DELETE

The application calls `deleteStudent`, lists all students, and pauses.

**Say:**

> deleteStudent removes the temporary row using its primary key and returns the
> deleted record. The final read shows that only the original three students
> remain.

**While paused:** Execute the pgAdmin `SELECT` query one final time.

**Say:**

> pgAdmin confirms that the temporary student has been deleted and the table is
> back to the three required initial records.

Return to the terminal, press Enter, and show the successful completion message.

### 3:35-4:10 - Code quality and conclusion

**Show:** Briefly show `app/student_repository.py`, `database/schema.sql`, and
`README.md`. Do not scroll too quickly.

**Say:**

> The project keeps the database scripts, application code, and tests organized
> in separate directories. The CRUD functions use parameterized SQL, connection
> cleanup, transaction rollback on errors, input validation, and clear comments.
> The README contains complete database setup, application setup, testing, and
> troubleshooting instructions. This completes all required CRUD operations.

Stop the recording. The planned duration is approximately four minutes.

## After recording

1. Upload the video to YouTube as **Unlisted**, Vimeo, or accessible cloud storage.
2. Open the video link in a private/incognito browser to confirm the instructor
   can view it without requesting access.
3. Replace the video placeholder in `README.md` with the working URL.
4. Commit and push the README update to GitHub.
5. Submit the public GitHub repository URL through Brightspace.

