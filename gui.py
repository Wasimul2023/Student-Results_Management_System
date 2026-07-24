import tkinter as tk
from student import Student 
from manager import StudentManager
from tkinter import messagebox
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
    try:
      student_id = id_entry.get()
      name = name_entry.get()
      marks = int(marks_entry.get())
      student = Student(student_id, name, marks)
      if manager.add_student(student):
         manager.save_students()
         messagebox.showinfo("Success","Student Added Successfully")

         id_entry.delete(0,tk.END)
         name_entry.delete(0,tk.END)
         marks_entry.delete(0,tk.END)
    except ValueError:
       messagebox.showerror("Error","Please Enter Valid Numeric Number")
  

def search_student():
   student_id = id_entry.get()

   for student in manager.students:
      if student.student_id == student_id:
         name_entry.delete(0, tk.END)
         name_entry.insert(0, student.name)


         marks_entry.delete(0, tk.END)
         marks_entry.insert(0, student.marks)


         messagebox.showinfo("Found","Student Found")
         return student
         
                     
   messagebox.showerror("Error","Student Not Found")
   return None
        

def update_student():
   student_id= id_entry.get()
   name = name_entry.get()
   try:
         marks = int(marks_entry.get())
   except ValueError:
         print("Please enter valid numeric number.")
         return
   manager.update_student(student_id, name, marks)
   manager.save_students()
   show_students()
   messagebox.showinfo("success ", "Updated Successfully")

def delete_student():
    student_id =  id_entry.get()
    
    if manager.delete_student(student_id):
        manager.save_students()
        show_students()

        id_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        marks_entry.delete(0, tk.END)
        messagebox.showinfo("Successful","Student deleted Sucessfully")

listbox = tk.Listbox(window, width=50, height=8)
listbox.pack(pady=10)         
      
def show_students():
    listbox.delete(0, tk.END)
    for student in manager.students:
        text =f"{student.student_id} | {student.name} | {student.marks} | {student.calculate_grade()}"
        listbox.insert(tk.END, text)        


def clear_fields():
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)



def show_statistics():
    results = manager.show_statistics()

    if results is None:
        messagebox.showerror("Error","No Student Data Found")
        return 
       
    average, highest, lowest, total = results
    messagebox.showinfo("Stiudent Statistic", f"Total Students : {total}\n"

        f"Average Marks : {average:.2f}\n"

        f"Highest Marks : {highest}\n"

        f"Lowest Marks : {lowest}"
 )

       
add_button = tk.Button(

    window,

    text="Add Student",

    command=add_student

)

add_button.pack(pady=10)

search_button = tk.Button(
   window,
   text="Serach Student",
   command=search_student

)

search_button.pack(pady=5)

update_button =tk.Button(
    window,
    text="Update Student",
    command=update_student
)

update_button.pack(pady=5)



delete_button =tk.Button(
    window,
    text="Delete Student",
    command=delete_student,
)

delete_button.pack(pady=5)

show_button = tk.Button(
    window,
    text="Show Student",
    command=show_students
)
show_button.pack()

clear_button = tk.Button(
    window,
    text="clear",
    command=clear_fields
)
clear_button.pack()

statistics_button = tk.Button(
    window,
    text="Show statistics",
    command=show_statistics
)
statistics_button.pack(pady=5)


window.mainloop()