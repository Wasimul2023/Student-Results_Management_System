class StudentManager:
    def __init__(self):
        self.students =[]
    def add_student(self,student):
       self.students.append(student)
    def show_students(self):
        for student in self.students:
           print("_____________")
           print("ID:", student.student_id)
           print("Name:",student.name)
           print("Marks:",student.marks)
           print("Grade:",student.calculate_grade())


    def search_student(self, student_id):
       for student in self.students:
           if student.student_id == student_id:
               print("Student Found")
               print("ID:", student.student_id)
               print("Name:", student.name)
               print("Marks:", student.marks)
               print("Grade:", student.calculate_grade())
               return
               
       print("\nStudent Not Found\n")


    def update_student(self, student_id, new_name, new_marks):
       for student in self.students:
        if student.student_id == student_id:
           student.name = new_name
           student.marks = new_marks
           print("Student Updated Successfully")
           return
   
print("Student Not Found")


