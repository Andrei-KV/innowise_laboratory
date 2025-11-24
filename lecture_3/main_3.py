"""This script manages student records,
including adding students, recording their grades,
and generating reports on their performance."""

import statistics


MENU_TEXT = """ --- Student Grade Analyzer ---
1. Add a new Student
2. Add grades for student
3. Show report (all students)
4. Find top performer
5. Exit
"""


def get_student_by_name(students, name):
    """Retrieve a student record by name."""
    for student in students:
        if student["name"] == name:
            return student
    return None


def add_new_student(students):
    """Add a new student to the records."""
    name = input("Enter student name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    if get_student_by_name(students, name):
        print("Student already exists.")
    else:
        students.append({"name": name, "grades": []})


def add_grades_for_student(students):
    """Add grades for an existing student."""
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
            grade = int(grade)
            if grade < 0 or grade > 100:
                print("Grade must be between 0 and 100.")
                continue
            student["grades"].append(grade)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue


def show_report_all_students(students):
    """Generate and display a report for all students."""
    print("--- Student Report ---")
    if not students:
        print("No students are in list.")
        return

    students_avg_list = []
    for student in students:
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


def find_top_performer(students):
    """Search for the student with the highest average grade."""
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
