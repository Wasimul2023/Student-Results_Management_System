import json
import numpy as np

from student import Student


class StudentManager:
    def __init__(self):
        self.students = []

    def add_student(self, student):
        for existing_student in self.students:
            if existing_student.student_id == student.student_id:
                print("Student ID already exists.")
                return False

        self.students.append(student)
        print("Student added successfully.")
        return True

    def show_students(self):
        for student in self.students:
            print("_____________")
            print("ID:", student.student_id)
            print("Name:", student.name)
            print("Marks:", student.marks)
            print("Grade:", student.calculate_grade())

    def search_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def update_student(self, student_id, new_name, new_marks):
        student = self.search_student(student_id)
        if student is None:
            print("Student not found.")
            return False

        student.name = new_name
        student.marks = new_marks
        self.save_students()
        print("Student updated successfully.")
        return True

    def delete_student(self, student_id):
        student = self.search_student(student_id)
        if student is None:
            print("Student not found.")
            return False

        self.students.remove(student)
        print("Student deleted successfully.")
        return True

    def save_students(self):
        data = [student.to_dict() for student in self.students]
        with open("students.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def load_students(self):
        try:
            with open("students.json", "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.students = []
            return

        self.students = []
        for student_data in data:
            try:
                student = Student(
                    student_data["student_id"],
                    student_data["name"],
                    student_data["marks"],
                )
                self.students.append(student)
            except (KeyError, TypeError, ValueError):
                continue

    def sort_students(self, key="name", reverse=False):
        if not self.students:
            return []

        def get_value(student):
            if key == "id":
                return student.student_id
            return getattr(student, key, "")

        return sorted(self.students, key=get_value, reverse=reverse)

    def filter_students(self, status_filter="all"):
        if status_filter == "all":
            return list(self.students)
        if status_filter == "pass":
            return [student for student in self.students if student.marks >= 50]
        if status_filter == "fail":
            return [student for student in self.students if student.marks < 50]
        return list(self.students)

    def show_statistics(self):
        if not self.students:
            return None

        marks = np.array([student.marks for student in self.students], dtype=float)
        average = float(np.mean(marks))
        highest = float(np.max(marks))
        lowest = float(np.min(marks))
        total = len(marks)
        passed = int(np.sum(marks >= 50))
        failed = total - passed

        return average, highest, lowest, total, passed, failed

    # New function 1: calculate the middle value of all student marks.
    def calculate_median(self):
        if not self.students:
            return 0.0

        marks = [student.marks for student in self.students]
        return float(np.median(marks))

    # New function 2: calculate how spread out the student marks are.
    def calculate_standard_deviation(self):
        if not self.students:
            return 0.0

        marks = [student.marks for student in self.students]
        return float(np.std(marks))
