"""This script creates a SQLite database for a school system,
creates tables for students and their grades, inserts sample data,
and performs various queries to retrieve and display information."""

import sqlite3

# Define the database name
DB_NAME = "school.db"

# Define SQL queries for creating tables and performing operations
# 1. Create table for students and birth years
table_students_query = """
CREATE TABLE IF NOT EXISTS students (
id INTEGER PRIMARY KEY,
full_name TEXT NOT NULL UNIQUE,
birth_year INTEGER NOT NULL
)
"""
# 2. Create table for grades with foreign key reference to students
table_grades_query = """
CREATE TABLE IF NOT EXISTS grades (
id INTEGER PRIMARY KEY,
student_id INTEGER NOT NULL,
subject TEXT NOT NULL,
grade INTEGER NOT NULL CHECK(grade >= 1 AND grade <= 100),
FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
)
"""

# 2.1 Create index on full_name in students table
index_students_name_query = """
CREATE INDEX IF NOT EXISTS idx_students_name ON students(full_name)
"""

# 2.2 Create index on student_id in grades table
index_grades_student_id_query = """
CREATE INDEX IF NOT EXISTS idx_grades_student_id ON grades(student_id)
"""

# 3. Query to get all grades for a specific student
grade_alice_query = """
SELECT g.subject, g.grade FROM grades AS g
JOIN students AS s ON g.student_id = s.id
WHERE s.full_name = 'Alice Johnson'
"""
# 4. Query to calculate the average grade per student
avg_grade_query = """
SELECT s.full_name as student_name, ROUND(AVG(g.grade), 1) as average_grade
FROM students AS s
JOIN grades AS g ON s.id = g.student_id
GROUP BY s.id
ORDER BY average_grade DESC
"""
# 5. Query to get list all students born after 2004
students_after_2004_query = """
SELECT full_name FROM students
WHERE birth_year > 2004
"""
# 6. Query to get list of subjects and their average grades
grades_avg_query = """
SELECT subject, ROUND(AVG(grade), 1) as average_grade
FROM grades
GROUP BY subject
ORDER BY subject ASC
"""
# 7. Query to find the top 3 students with the highest average grades
top_3_students_query = """
SELECT s.full_name as student_name, ROUND(AVG(g.grade), 1) as average_grade
FROM students AS s
JOIN grades AS g ON s.id = g.student_id
GROUP BY s.id
ORDER BY average_grade DESC
LIMIT 3
"""

# 8. Query to show all students who have scored below 80 in any subject
below_80_query = """
SELECT DISTINCT s.full_name AS full_name
FROM students AS s
JOIN grades AS g ON s.id = g.student_id
WHERE g.grade < 80
ORDER BY s.full_name ASC
"""

# Sample data to be inserted into the tables
students_data = [
    ("Alice Johnson", 2005),
    ("Brian Smith", 2004),
    ("Carla Reyes", 2006),
    ("Daniel Kim", 2005),
    ("Eva Thompson", 2003),
    ("Felix Nguyen", 2007),
    ("Grace Patel", 2005),
    ("Henry Lopez", 2004),
    ("Isabella Martinez", 2006),
]

grades_data = [
    (1, "Math", 88),
    (1, "English", 92),
    (1, "Science", 85),
    (2, "Math", 75),
    (2, "History", 83),
    (2, "English", 79),
    (3, "Science", 95),
    (3, "Math", 91),
    (3, "Art", 89),
    (4, "Math", 84),
    (4, "Science", 88),
    (4, "Physical Education", 93),
    (5, "English", 90),
    (5, "History", 85),
    (5, "Math", 88),
    (6, "Science", 72),
    (6, "Math", 78),
    (6, "English", 81),
    (7, "Art", 94),
    (7, "Science", 87),
    (7, "Math", 90),
    (8, "History", 77),
    (8, "Math", 83),
    (8, "Science", 80),
    (9, "English", 96),
    (9, "Math", 89),
    (9, "Art", 92),
]


def main() -> None:
    # Establish a connection to the SQLite database
    with sqlite3.connect(DB_NAME) as connection:
        # Execute the queries and handle exceptions
        try:
            cursor = connection.cursor()
            cursor.execute(table_students_query)
            cursor.execute(table_grades_query)
            connection.commit()
            print("Tables created successfully.")

            cursor.executemany(
                "INSERT INTO students (full_name, birth_year) VALUES (?, ?)",
                students_data,
            )
            cursor.executemany(
                "INSERT INTO grades (student_id, subject, grade) VALUES (?, ?, ?)",
                grades_data,
            )
            connection.commit()
            print("Data inserted successfully.")

            cursor.execute(grade_alice_query)
            alice_grades = cursor.fetchall()
            print("\nAlice Johnson grades:")
            for subject, grade in alice_grades:
                print(f"{subject} {grade}")

            cursor.execute(avg_grade_query)
            avg_grades = cursor.fetchall()
            print("\nAverage grades per student:")
            for student_name, average_grade in avg_grades:
                print(f"{student_name} {average_grade}")

            cursor.execute(students_after_2004_query)
            students_after_2004 = cursor.fetchall()
            print("\nStudents born after 2004:")
            for (full_name,) in students_after_2004:
                print(f"{full_name}")

            cursor.execute(grades_avg_query)
            grades_avg = cursor.fetchall()
            print("\nAverage grades per subject:")
            for subject, average_grade in grades_avg:
                print(f"{subject} {average_grade}")

            cursor.execute(top_3_students_query)
            top_3_students = cursor.fetchall()
            print("\nTop 3 students with highest average grades:")
            for student_name, average_grade in top_3_students:
                print(f"{student_name} {average_grade}")

            cursor.execute(below_80_query)
            below_80_students = cursor.fetchall()
            print("\nStudents who scored below 80 in any subject:")
            for (full_name,) in below_80_students:
                print(f"{full_name}")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
