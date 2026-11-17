-- Create the required table using PostgreSQL's standards-compliant identity column.
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    enrollment_date DATE
);

-- Add the exact three initial records. ON CONFLICT makes setup safe to rerun.
INSERT INTO students (first_name, last_name, email, enrollment_date)
VALUES
    ('John', 'Doe', 'john.doe@example.com', DATE '2023-09-01'),
    ('Jane', 'Smith', 'jane.smith@example.com', DATE '2023-09-01'),
    ('Jim', 'Beam', 'jim.beam@example.com', DATE '2023-09-02')
ON CONFLICT (email) DO NOTHING;

-- Display the initialized table so setup can be verified in pgAdmin or psql.
SELECT student_id, first_name, last_name, email, enrollment_date
FROM students
ORDER BY student_id;

