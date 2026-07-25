import math
import tkinter as tk
from tkinter import messagebox, ttk

from manager import StudentManager
from student import Student


LIGHT_THEME = {
    "background": "#F4F7FB",
    "surface": "#FFFFFF",
    "surface_alt": "#E9EEF6",
    "text": "#172033",
    "muted": "#667085",
    "border": "#CBD5E1",
    "primary": "#2563EB",
    "success": "#16A34A",
    "danger": "#DC2626",
    "warning": "#EA580C",
    "accent": "#7C3AED",
    "grid": "#D7DEE8",
}

DARK_THEME = {
    "background": "#0F172A",
    "surface": "#182235",
    "surface_alt": "#243047",
    "text": "#F8FAFC",
    "muted": "#A8B3C7",
    "border": "#3B4960",
    "primary": "#60A5FA",
    "success": "#4ADE80",
    "danger": "#F87171",
    "warning": "#FB923C",
    "accent": "#A78BFA",
    "grid": "#3B4960",
}


class StudentResultsApp:
    def __init__(self, root):
        self.root = root
        self.manager = StudentManager()
        self.manager.load_students()

        self.dark_mode = False
        self.theme = LIGHT_THEME
        self.sort_descending = tk.BooleanVar(value=False)
        self.statistics_windows = []

        self.root.title("Student Results Management System")
        self.root.geometry("820x780")
        self.root.minsize(760, 700)

        self.style = ttk.Style(self.root)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.build_interface()
        self.apply_theme()
        self.show_students()

    def build_interface(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)

        self.header_frame = tk.Frame(self.root)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=22, pady=(18, 10))
        self.header_frame.columnconfigure(0, weight=1)

        self.title_label = tk.Label(
            self.header_frame,
            text="Student Results Management System",
            font=("Segoe UI", 20, "bold"),
        )
        self.title_label.grid(row=0, column=0, sticky="w")

        self.theme_button = tk.Button(
            self.header_frame,
            text="Dark Mode",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            command=self.toggle_theme,
            padx=16,
            pady=8,
        )
        self.theme_button.grid(row=0, column=1, sticky="e")

        self.form_frame = tk.Frame(self.root, highlightthickness=1)
        self.form_frame.grid(row=1, column=0, sticky="ew", padx=22, pady=(0, 12))
        for column in range(6):
            self.form_frame.columnconfigure(column, weight=1)

        self.id_label = tk.Label(self.form_frame, text="Student ID", font=("Segoe UI", 9, "bold"))
        self.id_label.grid(row=0, column=0, sticky="w", padx=(16, 6), pady=(14, 4))
        self.name_label = tk.Label(self.form_frame, text="Name", font=("Segoe UI", 9, "bold"))
        self.name_label.grid(row=0, column=2, sticky="w", padx=6, pady=(14, 4))
        self.marks_label = tk.Label(self.form_frame, text="Marks", font=("Segoe UI", 9, "bold"))
        self.marks_label.grid(row=0, column=4, sticky="w", padx=6, pady=(14, 4))

        self.id_entry = tk.Entry(self.form_frame, font=("Segoe UI", 10), relief="flat", highlightthickness=1)
        self.id_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(16, 6), ipady=6)
        self.name_entry = tk.Entry(self.form_frame, font=("Segoe UI", 10), relief="flat", highlightthickness=1)
        self.name_entry.grid(row=1, column=2, columnspan=2, sticky="ew", padx=6, ipady=6)
        self.marks_entry = tk.Entry(self.form_frame, font=("Segoe UI", 10), relief="flat", highlightthickness=1)
        self.marks_entry.grid(row=1, column=4, columnspan=2, sticky="ew", padx=(6, 16), ipady=6)

        self.button_frame = tk.Frame(self.form_frame)
        self.button_frame.grid(row=2, column=0, columnspan=6, sticky="ew", padx=12, pady=12)
        for column in range(7):
            self.button_frame.columnconfigure(column, weight=1)

        self.add_button = self.create_button("Add", self.add_student, 0)
        self.search_button = self.create_button("Search", self.search_student, 1)
        self.update_button = self.create_button("Update", self.update_student, 2)
        self.delete_button = self.create_button("Delete", self.delete_student, 3)
        self.show_button = self.create_button("Show All", self.show_students, 4)
        self.clear_button = self.create_button("Clear", self.clear_fields, 5)
        self.statistics_button = self.create_button("Statistics Graph", self.show_statistics_dashboard, 6)

        self.records_frame = tk.Frame(self.root, highlightthickness=1)
        self.records_frame.grid(row=2, column=0, sticky="nsew", padx=22, pady=(0, 18))
        self.records_frame.columnconfigure(0, weight=1)
        self.records_frame.rowconfigure(2, weight=1)

        self.filter_frame = tk.Frame(self.records_frame)
        self.filter_frame.grid(row=0, column=0, sticky="ew", padx=14, pady=(12, 8))

        self.filter_label = tk.Label(self.filter_frame, text="Status:", font=("Segoe UI", 9, "bold"))
        self.filter_label.grid(row=0, column=0, padx=(0, 6))
        self.filter_type = ttk.Combobox(
            self.filter_frame,
            values=["all", "pass", "fail"],
            state="readonly",
            width=8,
        )
        self.filter_type.set("all")
        self.filter_type.grid(row=0, column=1, padx=(0, 14))

        self.filter_button = tk.Button(
            self.filter_frame,
            text="Filter",
            relief="flat",
            cursor="hand2",
            command=self.on_filter,
            padx=12,
            pady=5,
        )
        self.filter_button.grid(row=0, column=2, padx=(0, 18))

        self.sort_label = tk.Label(self.filter_frame, text="Sort by:", font=("Segoe UI", 9, "bold"))
        self.sort_label.grid(row=0, column=3, padx=(0, 6))
        self.sort_key = ttk.Combobox(
            self.filter_frame,
            values=["name", "id", "marks"],
            state="readonly",
            width=9,
        )
        self.sort_key.set("name")
        self.sort_key.grid(row=0, column=4, padx=(0, 8))

        self.desc_check = tk.Checkbutton(
            self.filter_frame,
            text="Descending",
            variable=self.sort_descending,
            font=("Segoe UI", 9),
        )
        self.desc_check.grid(row=0, column=5, padx=(0, 8))

        self.sort_button = tk.Button(
            self.filter_frame,
            text="Sort",
            relief="flat",
            cursor="hand2",
            command=self.on_sort,
            padx=12,
            pady=5,
        )
        self.sort_button.grid(row=0, column=6)

        self.listbox = tk.Listbox(
            self.records_frame,
            font=("Consolas", 11),
            relief="flat",
            highlightthickness=1,
            activestyle="none",
        )
        self.listbox.grid(row=2, column=0, sticky="nsew", padx=14, pady=(0, 14))
        self.listbox.bind("<<ListboxSelect>>", self.load_selected_student)

        self.scrollbar = ttk.Scrollbar(self.records_frame, orient="vertical", command=self.listbox.yview)
        self.scrollbar.grid(row=2, column=1, sticky="ns", pady=(0, 14), padx=(0, 14))
        self.listbox.configure(yscrollcommand=self.scrollbar.set)

    def create_button(self, text, command, column):
        button = tk.Button(
            self.button_frame,
            text=text,
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            command=command,
            pady=7,
        )
        button.grid(row=0, column=column, sticky="ew", padx=3)
        return button

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.theme = DARK_THEME if self.dark_mode else LIGHT_THEME
        self.theme_button.configure(text="Light Mode" if self.dark_mode else "Dark Mode")
        self.apply_theme()

        for window in list(self.statistics_windows):
            if window.winfo_exists():
                window.destroy()
        self.statistics_windows.clear()

    def apply_theme(self):
        theme = self.theme
        self.root.configure(bg=theme["background"])

        for frame in (self.header_frame, self.button_frame, self.filter_frame):
            frame.configure(bg=theme["background"] if frame is self.header_frame else theme["surface"])

        for frame in (self.form_frame, self.records_frame):
            frame.configure(
                bg=theme["surface"],
                highlightbackground=theme["border"],
                highlightcolor=theme["border"],
            )

        for label in (
            self.title_label,
            self.id_label,
            self.name_label,
            self.marks_label,
            self.filter_label,
            self.sort_label,
        ):
            label.configure(
                bg=theme["background"] if label is self.title_label else theme["surface"],
                fg=theme["text"],
            )

        for entry in (self.id_entry, self.name_entry, self.marks_entry):
            entry.configure(
                bg=theme["surface_alt"],
                fg=theme["text"],
                insertbackground=theme["text"],
                highlightbackground=theme["border"],
                highlightcolor=theme["primary"],
            )

        self.listbox.configure(
            bg=theme["surface_alt"],
            fg=theme["text"],
            selectbackground=theme["primary"],
            selectforeground="#FFFFFF",
            highlightbackground=theme["border"],
        )

        self.desc_check.configure(
            bg=theme["surface"],
            fg=theme["text"],
            activebackground=theme["surface"],
            activeforeground=theme["text"],
            selectcolor=theme["surface_alt"],
        )

        self.theme_button.configure(bg=theme["accent"], fg="#FFFFFF", activebackground=theme["accent"])
        self.add_button.configure(bg=theme["success"], fg="#FFFFFF", activebackground=theme["success"])
        self.search_button.configure(bg=theme["primary"], fg="#FFFFFF", activebackground=theme["primary"])
        self.update_button.configure(bg=theme["warning"], fg="#FFFFFF", activebackground=theme["warning"])
        self.delete_button.configure(bg=theme["danger"], fg="#FFFFFF", activebackground=theme["danger"])
        self.show_button.configure(bg=theme["accent"], fg="#FFFFFF", activebackground=theme["accent"])
        self.clear_button.configure(bg=theme["muted"], fg="#FFFFFF", activebackground=theme["muted"])
        self.statistics_button.configure(bg=theme["primary"], fg="#FFFFFF", activebackground=theme["primary"])
        self.filter_button.configure(bg=theme["primary"], fg="#FFFFFF", activebackground=theme["primary"])
        self.sort_button.configure(bg=theme["accent"], fg="#FFFFFF", activebackground=theme["accent"])

        self.style.configure(
            "TCombobox",
            fieldbackground=theme["surface_alt"],
            background=theme["surface_alt"],
            foreground=theme["text"],
            arrowcolor=theme["text"],
        )
        self.style.map(
            "TCombobox",
            fieldbackground=[("readonly", theme["surface_alt"])],
            foreground=[("readonly", theme["text"])],
            selectbackground=[("readonly", theme["surface_alt"])],
            selectforeground=[("readonly", theme["text"])],
        )

    def read_form(self):
        student_id = self.id_entry.get().strip()
        name = self.name_entry.get().strip()
        marks_text = self.marks_entry.get().strip()

        if not student_id or not name or not marks_text:
            messagebox.showerror("Error", "Please fill in Student ID, Name and Marks.")
            return None

        try:
            marks = int(marks_text)
        except ValueError:
            messagebox.showerror("Error", "Marks must be a valid number.")
            return None

        if not 0 <= marks <= 100:
            messagebox.showerror("Error", "Marks must be between 0 and 100.")
            return None

        return student_id, name, marks

    def add_student(self):
        form_data = self.read_form()
        if form_data is None:
            return

        student_id, name, marks = form_data
        student = Student(student_id, name, marks)
        if not self.manager.add_student(student):
            messagebox.showerror("Error", "Student ID already exists.")
            return

        self.manager.save_students()
        self.show_students()
        self.clear_fields()
        messagebox.showinfo("Success", "Student added successfully.")

    def search_student(self):
        student_id = self.id_entry.get().strip()
        if not student_id:
            messagebox.showerror("Error", "Enter a Student ID first.")
            return

        student = self.manager.search_student(student_id)
        if student is None:
            messagebox.showerror("Error", "Student not found.")
            return

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, student.name)
        self.marks_entry.delete(0, tk.END)
        self.marks_entry.insert(0, student.marks)
        messagebox.showinfo("Found", "Student found.")

    def update_student(self):
        form_data = self.read_form()
        if form_data is None:
            return

        student_id, name, marks = form_data
        if not self.manager.update_student(student_id, name, marks):
            messagebox.showerror("Error", "Student not found.")
            return

        self.manager.save_students()
        self.show_students()
        messagebox.showinfo("Success", "Student updated successfully.")

    def delete_student(self):
        student_id = self.id_entry.get().strip()
        if not student_id:
            messagebox.showerror("Error", "Enter a Student ID first.")
            return

        if not self.manager.delete_student(student_id):
            messagebox.showerror("Error", "Student not found.")
            return

        self.manager.save_students()
        self.show_students()
        self.clear_fields()
        messagebox.showinfo("Success", "Student deleted successfully.")

    def show_students(self, records=None):
        self.listbox.delete(0, tk.END)
        student_data = self.manager.students if records is None else records
        for student in student_data:
            status = "Pass" if student.marks >= 50 else "Fail"
            text = (
                f"ID: {student.student_id:<10} | "
                f"Name: {student.name:<22} | "
                f"Marks: {student.marks:<3} | "
                f"Grade: {student.calculate_grade():<2} | {status}"
            )
            self.listbox.insert(tk.END, text)

    def clear_fields(self):
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.marks_entry.delete(0, tk.END)

    def load_selected_student(self, _event=None):
        selection = self.listbox.curselection()
        if not selection:
            return

        displayed_text = self.listbox.get(selection[0])
        student_id = displayed_text.split("|")[0].replace("ID:", "").strip()
        student = self.manager.search_student(student_id)
        if student is None:
            return

        self.clear_fields()
        self.id_entry.insert(0, student.student_id)
        self.name_entry.insert(0, student.name)
        self.marks_entry.insert(0, student.marks)

    def on_filter(self):
        filtered_records = self.manager.filter_students(self.filter_type.get())
        self.show_students(filtered_records)

    def on_sort(self):
        sorted_records = self.manager.sort_students(
            key=self.sort_key.get(),
            reverse=self.sort_descending.get(),
        )
        self.show_students(sorted_records)

    def show_statistics_dashboard(self):
        results = self.manager.show_statistics()
        if results is None:
            messagebox.showerror("Error", "No student data found.")
            return

        average, highest, lowest, total, passed, failed = results
        median = self.manager.calculate_median()
        standard_deviation = self.manager.calculate_standard_deviation()

        window = tk.Toplevel(self.root)
        window.title("Student Statistics")
        window.geometry("940x660")
        window.minsize(820, 580)
        window.configure(bg=self.theme["background"])
        self.statistics_windows.append(window)
        window.protocol("WM_DELETE_WINDOW", lambda: self.close_statistics_window(window))

        title = tk.Label(
            window,
            text="Student Statistics Dashboard",
            font=("Segoe UI", 20, "bold"),
            bg=self.theme["background"],
            fg=self.theme["text"],
        )
        title.pack(pady=(18, 12))

        summary_frame = tk.Frame(window, bg=self.theme["background"])
        summary_frame.pack(fill="x", padx=24)
        summary_values = [
            ("Total", total),
            ("Average", f"{average:.2f}"),
            ("Median", f"{median:.2f}"),
            ("Std. Deviation", f"{standard_deviation:.2f}"),
            ("Highest", f"{highest:.0f}"),
            ("Lowest", f"{lowest:.0f}"),
        ]

        for index, (label_text, value_text) in enumerate(summary_values):
            summary_frame.columnconfigure(index, weight=1)
            card = tk.Frame(
                summary_frame,
                bg=self.theme["surface"],
                highlightthickness=1,
                highlightbackground=self.theme["border"],
            )
            card.grid(row=0, column=index, sticky="ew", padx=4)
            tk.Label(
                card,
                text=label_text,
                font=("Segoe UI", 9),
                bg=self.theme["surface"],
                fg=self.theme["muted"],
            ).pack(pady=(10, 2))
            tk.Label(
                card,
                text=value_text,
                font=("Segoe UI", 16, "bold"),
                bg=self.theme["surface"],
                fg=self.theme["text"],
            ).pack(pady=(0, 10))

        graph_frame = tk.Frame(window, bg=self.theme["background"])
        graph_frame.pack(fill="both", expand=True, padx=24, pady=18)
        graph_frame.columnconfigure(0, weight=2)
        graph_frame.columnconfigure(1, weight=1)
        graph_frame.rowconfigure(0, weight=1)

        marks_canvas = tk.Canvas(
            graph_frame,
            bg=self.theme["surface"],
            highlightthickness=1,
            highlightbackground=self.theme["border"],
        )
        marks_canvas.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        pass_fail_canvas = tk.Canvas(
            graph_frame,
            bg=self.theme["surface"],
            highlightthickness=1,
            highlightbackground=self.theme["border"],
        )
        pass_fail_canvas.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        marks_canvas.bind("<Configure>", lambda event: self.draw_marks_graph(marks_canvas))
        pass_fail_canvas.bind(
            "<Configure>",
            lambda event: self.draw_pass_fail_graph(pass_fail_canvas, passed, failed),
        )

    def close_statistics_window(self, window):
        if window in self.statistics_windows:
            self.statistics_windows.remove(window)
        window.destroy()

    def draw_marks_graph(self, canvas):
        canvas.delete("all")
        width = max(canvas.winfo_width(), 420)
        height = max(canvas.winfo_height(), 360)
        theme = self.theme

        canvas.create_text(
            width / 2,
            28,
            text="Student Marks Bar Graph",
            fill=theme["text"],
            font=("Segoe UI", 13, "bold"),
        )

        students = self.manager.students[:12]
        if not students:
            canvas.create_text(width / 2, height / 2, text="No data", fill=theme["muted"])
            return

        left = 52
        right = width - 22
        top = 62
        bottom = height - 62
        chart_height = bottom - top
        chart_width = right - left

        for value in range(0, 101, 20):
            y = bottom - (value / 100) * chart_height
            canvas.create_line(left, y, right, y, fill=theme["grid"])
            canvas.create_text(left - 10, y, text=str(value), fill=theme["muted"], anchor="e")

        bar_space = chart_width / len(students)
        bar_width = min(38, bar_space * 0.58)

        for index, student in enumerate(students):
            x_center = left + bar_space * index + bar_space / 2
            bar_height = (student.marks / 100) * chart_height
            x1 = x_center - bar_width / 2
            x2 = x_center + bar_width / 2
            y1 = bottom - bar_height

            canvas.create_rectangle(x1, y1, x2, bottom, fill=theme["primary"], outline="")
            canvas.create_text(x_center, y1 - 10, text=str(student.marks), fill=theme["text"], font=("Segoe UI", 8, "bold"))
            short_name = student.name[:8]
            canvas.create_text(x_center, bottom + 18, text=short_name, fill=theme["muted"], font=("Segoe UI", 8))

        canvas.create_line(left, top, left, bottom, fill=theme["text"], width=2)
        canvas.create_line(left, bottom, right, bottom, fill=theme["text"], width=2)

    def draw_pass_fail_graph(self, canvas, passed, failed):
        canvas.delete("all")
        width = max(canvas.winfo_width(), 280)
        height = max(canvas.winfo_height(), 360)
        theme = self.theme

        canvas.create_text(
            width / 2,
            28,
            text="Pass / Fail Donut Graph",
            fill=theme["text"],
            font=("Segoe UI", 13, "bold"),
        )

        total = passed + failed
        if total == 0:
            canvas.create_text(width / 2, height / 2, text="No data", fill=theme["muted"])
            return

        size = min(width - 70, height - 150)
        x1 = (width - size) / 2
        y1 = 75
        x2 = x1 + size
        y2 = y1 + size

        passed_angle = (passed / total) * 360
        canvas.create_arc(
            x1,
            y1,
            x2,
            y2,
            start=90,
            extent=-passed_angle,
            fill=theme["success"],
            outline=theme["surface"],
            width=2,
        )
        canvas.create_arc(
            x1,
            y1,
            x2,
            y2,
            start=90 - passed_angle,
            extent=-(360 - passed_angle),
            fill=theme["danger"],
            outline=theme["surface"],
            width=2,
        )

        hole_margin = size * 0.28
        canvas.create_oval(
            x1 + hole_margin,
            y1 + hole_margin,
            x2 - hole_margin,
            y2 - hole_margin,
            fill=theme["surface"],
            outline=theme["surface"],
        )
        canvas.create_text(
            width / 2,
            y1 + size / 2 - 8,
            text=str(total),
            fill=theme["text"],
            font=("Segoe UI", 22, "bold"),
        )
        canvas.create_text(
            width / 2,
            y1 + size / 2 + 18,
            text="Students",
            fill=theme["muted"],
            font=("Segoe UI", 9),
        )

        legend_y = y2 + 28
        canvas.create_rectangle(35, legend_y - 7, 49, legend_y + 7, fill=theme["success"], outline="")
        canvas.create_text(58, legend_y, text=f"Pass: {passed}", fill=theme["text"], anchor="w")
        canvas.create_rectangle(145, legend_y - 7, 159, legend_y + 7, fill=theme["danger"], outline="")
        canvas.create_text(168, legend_y, text=f"Fail: {failed}", fill=theme["text"], anchor="w")


if __name__ == "__main__":
    main_window = tk.Tk()
    app = StudentResultsApp(main_window)
    main_window.mainloop()
