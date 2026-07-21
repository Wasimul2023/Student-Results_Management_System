import json
from student import Student
class StudentManager:
    def __init__(self):
        self.students =[]
    def add_student(self,student):
       for s in self.students:
          if s.student_id == student.student_id:
             print("Student Id Already Exists.")
             return
          
       self.students.append(student)
       print("Stdent Added Successfully")
   
   
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

    def delete_student(self,student_id):
        for student in self.students:
           if student.student_id == student_id:
             self.students.remove(student)
             print("Student Deleted")


    print("Student Not Found")

    def save_students(self):
       data = []
       for student in self.students:
           data.append(student.to_dict())
       with open("students.json","w") as file:
           json.dump(data,file,indent=4)

     
       print("Students Saved Successfully")   
    
    
    def load_students(self):
        try:
           with open("students.json","r") as file:
              data = json.load(file)
           self.students =[]

           for student_data in data:
              student = Student(

    student_data["student_id"],

    student_data["name"],

    student_data["marks"]

)
              self.students.append(student)
 
           print("Students Loaded Successfully")
         
        except FileExistsError:
           print("No saved file found.")

  




