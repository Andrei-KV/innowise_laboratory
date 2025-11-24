"""This script manages student records,
including adding students, recording their grades,
and generating reports on their performance."""

import statistics
from typing import List, Optional, TypedDict


MENU_TEXT = """ --- Student Grade Analyzer ---
1. Add a new Student
2. Add grades for student
3. Show report (all students)
4. Find top performer
5. Exit
"""


class Student(TypedDict):
    name: str
    grades: List[int]


def get_student_by_name(students: List[Student], name: str) -> Optional[Student]:
    """
    Retrieve a student record by name.
    Args:
        students (list): List of student records.
        name (str): Name of the student to find.
    Returns:
        dict: The student record if found, else None."""
    for student in students:
        if student["name"] == name:
            return student
    return None


def add_new_student(students: List[Student]) -> None:
    """
    Add a new student to the records.
    Args:
        students (list): List of student records.
    """
    name = input("Enter student name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    if get_student_by_name(students, name):
        print("Student already exists.")
    else:
        students.append({"name": name, "grades": []})


def add_grades_for_student(students: List[Student]) -> None:
    """
    Add grades for an existing student.
    Args:
        students (list): List of student records.
    """
    name = input("Enter student name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    student = get_student_by_name(students, name)
    if not student:
        print("Student not found.")
        return

    while True:
        grade = input("Enter a grade (or 'done' to finish): ").strip()
        if grade.lower() == "done":
            break
        try:
            grade_val = int(grade)
            if grade_val < 0 or grade_val > 100:
                print("Grade must be between 0 and 100.")
                continue
            student["grades"].append(grade_val)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue


def show_report_all_students(students: List[Student]) -> None:
    """
    Generate and display a report for all students.
    Args:
        students (list): List of student records.
    """
    print("--- Student Report ---")
    if not students:
        print("No students are in list.")
        return

    students_avg_list = []
    for student in students:
        avg: float | str = "N/A"
        try:
            avg = sum(student["grades"]) / len(student["grades"])
            students_avg_list.append(avg)
            print(f"{student['name']}'s average grade is {avg:.1f}")
        except ZeroDivisionError:
            avg = "N/A"
            print(f"{student['name']}'s average grade is {avg}")
        except Exception:
            avg = "N/A"
            print(f"{student['name']}'s average grade is {avg}")

    if students_avg_list:
        max_avg = max(students_avg_list)
        min_avg = min(students_avg_list)
        overall_avg = statistics.mean(students_avg_list)
        print("-" * 26, end="\n")
        print(f"""
Max Average: {max_avg:.1f}
Min Average: {min_avg:.1f}
Overall Average: {overall_avg:.1f}
        """)
    else:
        print("There are no grades in the list.")


def find_top_performer(students: List[Student]) -> None:
    """
    Search for the student with the highest average grade.
    Args:
        students (list): List of student records.
    """
    if not students:
        print("No students are in list.")
        return

    students_with_grades = [s for s in students if s["grades"]]

    if not students_with_grades:
        print("There are no grades in the list.")
        return

    max_avg_grade = max(
        students_with_grades, key=lambda n: sum(n["grades"]) / len(n["grades"])
    )

    avg_grade = statistics.mean(max_avg_grade["grades"])
    name = max_avg_grade["name"]
    print(
        f"The student with the highest average is {name} with a grade of {avg_grade:.1f}."
    )


def main():
    students = []
    valid_choices = {"1", "2", "3", "4", "5"}

    while True:
        print(MENU_TEXT)

        try:
            choice = input("Enter your choice (1-5): ").strip()
            if choice not in valid_choices:
                print("Invalid choice. Please enter a number between 1 and 5.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")
            continue

        if choice == "1":
            add_new_student(students)

        elif choice == "2":
            add_grades_for_student(students)

        elif choice == "3":
            show_report_all_students(students)

        elif choice == "4":
            find_top_performer(students)

        else:
            print("Exiting program.")
            break


if __name__ == "__main__":
    main()
