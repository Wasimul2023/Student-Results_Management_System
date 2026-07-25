import json
import numpy as np 
from student import Student
class StudentManager:
    def __init__(self):
        self.students =[]
    def add_student(self,student):
       for s in self.students:
          if s.student_id == student.student_id:
             print("Student Id Already Exists.")
             return False
          
       self.students.append(student)
       print("Stdent Added Successfully")
       return True
   
   
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
           self.save_students()
           print("Student Updated Successfully")
           return True
        

       print("Student Not Found")
       return False

    def delete_student(self,student_id):
        for student in self.students:
           if student.student_id == student_id:
             self.students.remove(student)
             print("Student Deleted Successfully")
             return True
           
        print("Student Not Found")
        return False
         



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
         
        except FileNotFoundError:
           print("No saved file found.")


    def sort_students(self, key="name", reverse=False):
        if not self.students:
            return []

        def get_attr(student):
            if isinstance(student, dict):
                val = student.get(key, 0 if key in ['marks', 'gpa', 'score'] else "")
            else:
                val = getattr(student, key, 0 if key in ['marks', 'gpa', 'score'] else "")
            return val if val is not None else ""

        return sorted(self.students, key=get_attr, reverse=reverse)

    def filter_students(self, status_filter="all"):
        if status_filter == "all":
            return self.students

        filtered = []
        for student in self.students:
            marks = getattr(student, "marks", getattr(student, "score", 0))
            
            try:
                marks = float(marks)
            except ValueError:
                marks = 0

            if status_filter == "pass" and marks >= 70:
                filtered.append(student)
            elif status_filter == "fail" and marks < 70:
                filtered.append(student)

        return filtered
    
    def show_statistics(self):
       if len(self.students) == 0:
         return None 
          

       marks = np.array([student.marks for student in self.students])

       average = np.mean(marks)
       highest = np.max(marks)
       lowest = np.min(marks)
       total  = len(marks)

       return average, highest, lowest, total
    



      
