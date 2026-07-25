import tkinter as tk
from tkinter import ttk
from student import Student 
from manager import StudentManager
from tkinter import messagebox
manager = StudentManager()
manager.load_students()
window = tk.Tk()
window.title("Student Results Management System")
window.geometry("650x900")
window.resizable(False, False)
window.configure(bg="#F5F7FA")
title = tk.Label(
   window,
   text="Student Results Management System",
   font=("Arial", 16, "bold"),
   bg="#F5F7FA"
)

title.pack(pady=20)
tk.Label(window, text="Student ID", bg= "#F5F7FA").pack()
id_entry = tk.Entry(window, width=30)
id_entry.pack()
tk.Label(window, text="Name").pack()
name_entry = tk.Entry(window, width=30)
name_entry.pack()
tk.Label(window, text="Marks").pack()
marks_entry = tk.Entry(window, width=30)
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

listbox = tk.Listbox(
    window,
    width=60, 
    height=10,
    font=("Times New Roman",10)
    )
listbox.pack(pady=10)  

button_frame = tk.Frame(window)
button_frame.pack(pady=5)
      
def show_students(records=None):
    listbox.delete(0, tk.END)
    student_data = records if records is not None else manager.students
    for student in student_data:
        s_id = getattr(student, "student_id", getattr(student, "id", ""))
        s_name = getattr(student, "name", "")
        s_marks = getattr(student, "marks", "")
        s_grade = student.calculate_grade() if hasattr(student, "calculate_grade") else getattr(student, "grade", "")
        
        text = f"{s_id} | {s_name} | {s_marks} | {s_grade}"
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
def setup_filter_sort_ui(parent_frame):
    filter_sort_frame = tk.Frame(parent_frame, bg="#F5F7FA")
    filter_sort_frame.pack(pady=5)

    tk.Label(filter_sort_frame, text="Status:", bg="#F5F7FA").grid(row=0, column=0, padx=2, pady=2)
    
    global filter_type, sort_key, sort_order
    filter_type = ttk.Combobox(filter_sort_frame, values=["all", "pass", "fail"], state="readonly", width=6)
    filter_type.set("all")
    filter_type.grid(row=0, column=1, padx=2, pady=2)

    btn_filter = tk.Button(
        filter_sort_frame,
        text="Filter",
        width=8,
        bg="#2196F3",
        fg="white",
        cursor="hand2",
        command=on_filter
    )
    btn_filter.grid(row=0, column=2, padx=2, pady=2)

    sort_key = ttk.Combobox(filter_sort_frame, values=["name", "id", "marks"], state="readonly", width=6)
    sort_key.set("name")
    sort_key.grid(row=1, column=0, padx=2, pady=2)

    sort_order = tk.BooleanVar(value=False)
    chk_desc = tk.Checkbutton(filter_sort_frame, text="Desc", variable=sort_order, bg="#F5F7FA")
    chk_desc.grid(row=1, column=1, padx=2, pady=2)

    btn_sort = tk.Button(
        filter_sort_frame,
        text="Sort",
        width=8,
        bg="#9C27B0",
        fg="white",
        cursor="hand2",
        command=on_sort
    )
    btn_sort.grid(row=1, column=2, padx=2, pady=2)

def on_filter():
    status = filter_type.get()
    filtered_results = manager.filter_students(status_filter=status)
    show_students(filtered_results)

def on_sort():
    key = sort_key.get()
    reverse = sort_order.get()
    sorted_results = manager.sort_students(key=key, reverse=reverse)
    show_students(sorted_results)


add_button = tk.Button(

    button_frame,

    text="Add Student",
    width=18,
    height=2,
    bg="#4CAF50",
    fg="White",
    cursor= "hand2",

    command=add_student

)

add_button.grid(row=0, column=0)

search_button = tk.Button(
   button_frame,
   text="Serach Student",
   width=18,
   height=2,
   bg="#007BFF",
   fg="White",
   activebackground="#0069D9",
   cursor= "hand2",
   command=search_student

)

search_button.grid(row=0, column=1)

update_button =tk.Button(
    button_frame,
    text="Update Student",
    width=18,
    height=2,
    bg="#FD7E14",
    fg="White",
    activebackground="#E96B09",
    cursor= "hand2",
    command=update_student
)

update_button.grid(row=1, column=0)



delete_button =tk.Button(
    button_frame,
    text="Delete Student",
    width=18,
    height=2,
    bg="#DC3545",
   fg="White",
   activebackground="#C82333",
   cursor= "hand2",
    command=delete_student,
)

delete_button.grid(row=1, column=1)
show_button = tk.Button(
    button_frame,
    text="Show Student",
    width=18,
    height=2,
    bg="#6F42C1",
   fg="White",
   activebackground="#5A32A3",
   cursor= "hand2",
    command=show_students
)
show_button.grid(row=2, column=0)

clear_button = tk.Button(
    button_frame,
    text="clear",
    width=18,
    height=2,
    bg="#6C757D",
   fg="White",
   activebackground="#5A6268",
   cursor= "hand2",
    command=clear_fields
)
clear_button.grid(row=2, column=1)

statistics_button = tk.Button(
    button_frame,
    text="Show statistics",
    width=18,
    height=2,
    bg="#20C997",
   fg="White",
   activebackground="#17A589",
   cursor= "hand2",
    command=show_statistics
)
statistics_button.grid(row=3, column=0, columnspan=2, pady=10)

show_students()
setup_filter_sort_ui(window)
window.mainloop()