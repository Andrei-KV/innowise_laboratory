CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL UNIQUE,
    birth_year INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    grade INTEGER NOT NULL CHECK(grade >= 1 AND grade <= 100),
    UNIQUE(student_id, subject),
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_students_name ON students(full_name);

CREATE INDEX IF NOT EXISTS idx_grades_student_id ON grades(student_id);

CREATE INDEX IF NOT EXISTS idx_students_birth_year ON students(birth_year);

CREATE INDEX IF NOT EXISTS idx_grades_grade ON grades(grade);

CREATE INDEX IF NOT EXISTS idx_grades_subject ON grades(subject);

INSERT OR IGNORE INTO students (full_name, birth_year) VALUES
    ('Alice Johnson', 2005),
    ('Brian Smith', 2004),
    ('Carla Reyes', 2006),
    ('Daniel Kim', 2005),
    ('Eva Thompson', 2003),
    ('Felix Nguyen', 2007),
    ('Grace Patel', 2005),
    ('Henry Lopez', 2004),
    ('Isabella Martinez', 2006);

INSERT OR IGNORE INTO grades (student_id, subject, grade) VALUES
    (1, 'Math', 88),
    (1, 'English', 92),
    (1, 'Science', 85),
    (2, 'Math', 75),
    (2, 'History', 83),
    (2, 'English', 79),
    (3, 'Science', 95),
    (3, 'Math', 91),
    (3, 'Art', 89),
    (4, 'Math', 84),
    (4, 'Science', 88),
    (4, 'Physical Education', 93),
    (5, 'English', 90),
    (5, 'History', 85),
    (5, 'Math', 88),
    (6, 'Science', 72),
    (6, 'Math', 78),
    (6, 'English', 81),
    (7, 'Art', 94),
    (7, 'Science', 87),
    (7, 'Math', 90),
    (8, 'History', 77),
    (8, 'Math', 83),
    (8, 'Science', 80),
    (9, 'English', 96),
    (9, 'Math', 89),
    (9, 'Art', 92);

SELECT g.subject AS subject, g.grade AS grade
FROM grades g
JOIN students s ON g.student_id = s.id
WHERE s.full_name = 'Alice Johnson';

SELECT '';

SELECT s.full_name AS full_name, ROUND(AVG(g.grade), 1) as average_grade
FROM students AS s
JOIN grades AS g ON s.id = g.student_id
GROUP BY s.id
ORDER BY average_grade DESC;

SELECT '';

SELECT full_name
FROM students
WHERE birth_year > 2004
ORDER BY full_name ASC;

SELECT '';

SELECT subject, ROUND(AVG(grade), 1) as average_grade
FROM grades
GROUP BY subject
ORDER BY subject ASC;

SELECT '';

SELECT s.full_name AS full_name, ROUND(AVG(g.grade), 1) as average_grade
FROM students AS s
JOIN grades AS g ON s.id = g.student_id
GROUP BY s.id
ORDER BY average_grade DESC
LIMIT 3;

SELECT '';

SELECT DISTINCT s.full_name AS full_name
FROM students AS s
JOIN grades AS g ON s.id = g.student_id
WHERE g.grade < 80
ORDER BY s.full_name ASC;
