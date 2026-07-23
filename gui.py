import tkinter as tk
from student import Student 
from manager import StudentManager
manager = StudentManager()
manager.load_students()
window = tk.Tk()
window.title("Student Results Management System")
window.geometry("600x500")
title = tk.Label(
   window,
   text="Student Results Management System",
   font=("Arial", 16, "bold")
)

title.pack(pady=20)
tk.Label(window, text="Student ID").pack()
id_entry = tk.Entry(window)
id_entry.pack()
tk.Label(window, text="Name").pack()
name_entry = tk.Entry(window)
name_entry.pack()
tk.Label(window, text="Marks").pack()
marks_entry = tk.Entry(window)
marks_entry.pack()
def add_student():
   student_id = id_entry.get()
   name = name_entry.get()
   marks = int(marks_entry.get())
   student = Student(student_id, name, marks)
   if manager.add_student(student):
     manager.save_students()
  

 


add_button = tk.Button(

    window,

    text="Add Student",

    command=add_student

)

add_button.pack(pady=10)
 
window.mainloop()