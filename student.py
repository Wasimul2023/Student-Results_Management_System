class Student:
   def __init__(self, student_id, name, marks):
       self.student_id = student_id
       self.name = name
       self.marks = marks
   def calculate_grade(self):
            if self.marks>=90:
                return "A+"
            elif self.marks>=85:
                return "A"
            elif self.marks>=80:
                return "B+"
            elif self.marks>=75:
                return "B"
            elif self.marks>=70:
                return "C+"
            elif self.marks>=65:
                return "C"
            elif self.marks>=60:
                return "D+"
            elif self.marks>=50:
                return "D"
            else :
              return "F"
   def to_dict(self):
       return{
           "student_id":self.student_id,
           "name":self.name,
           "marks":self.marks
       }
   
               