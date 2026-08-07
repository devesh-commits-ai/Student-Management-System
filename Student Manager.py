
import customtkinter as ctk
import tkinter.ttk as ttk
from tkinter import messagebox
import csv
import os

# -------------------------------
# App Settings
# -------------------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Student Management System")
app.geometry("800x600")
app.resizable(False, False)

# Safe icon loading
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(BASE_DIR, "graduated.ico")

if os.path.exists(icon_path):
    try:
        app.iconbitmap(icon_path)
    except Exception:
        pass

# -------------------------------
# Functions
# -------------------------------

def add_student(file_name, student, age, course):
    if not file_name or not student or not age or not course:
        messagebox.showwarning("Input Error", "Please fill all fields!")
        return False

    data = file_name + ".csv"
    file_exist = os.path.exists(data)

    with open(data, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exist:
            writer.writerow(["Name", "Age", "Course"])

        writer.writerow([student, age, course])

    messagebox.showinfo("Success", "Student Added Successfully!")
    return True


def view_student(file_name):
    data = file_name + ".csv"

    try:
        students = []

        with open(data, "r") as f:
            read = csv.reader(f)

            next(read, None)

            for row in read:
                students.append(row)

        return students

    except FileNotFoundError:
        return None


def search_student(file_name, name):
    data = file_name + ".csv"

    try:
        with open(data, "r") as f:
            read = csv.reader(f)

            next(read, None)

            for row in read:
                if row[0].lower() == name.lower():
                    return row

        return None

    except FileNotFoundError:
        return "File Not Found"


def delete_student(file_name, name):
    data = file_name + ".csv"
    updated = []
    found = False

    try:
        with open(data, "r") as f:
            reader = csv.reader(f)

            header = next(reader, None)

            if header:
                updated.append(header)

            for row in reader:
                if row[0].lower() != name.lower():
                    updated.append(row)
                else:
                    found = True

        with open(data, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(updated)

        return found

    except FileNotFoundError:
        return None


# -------------------------------
# Add Student Popup
# -------------------------------

def gui_add():
    window = ctk.CTkToplevel(app)
    window.title("Add Student")
    window.geometry("400x350")

    file_entry = ctk.CTkEntry(window, placeholder_text="File Name")
    file_entry.pack(pady=10)

    name_entry = ctk.CTkEntry(window, placeholder_text="Student Name")
    name_entry.pack(pady=10)

    age_entry = ctk.CTkEntry(window, placeholder_text="Age")
    age_entry.pack(pady=10)

    course_entry = ctk.CTkEntry(window, placeholder_text="Course")
    course_entry.pack(pady=10)

    def save():
        success = add_student(
            file_entry.get(),
            name_entry.get(),
            age_entry.get(),
            course_entry.get()
        )

        if success:
            window.destroy()

    ctk.CTkButton(window, text="Save Student", command=save).pack(pady=20)


# -------------------------------
# View Students Popup
# -------------------------------

def gui_view():
    window = ctk.CTkToplevel(app)
    window.title("View Students")
    window.geometry("650x450")

    file_entry = ctk.CTkEntry(window, placeholder_text="Enter File Name")
    file_entry.pack(pady=10)

    table = ttk.Treeview(
        window,
        columns=("Name", "Age", "Course"),
        show="headings",
        height=10
    )

    table.heading("Name", text="Name")
    table.heading("Age", text="Age")
    table.heading("Course", text="Course")

    table.column("Name", width=220)
    table.column("Age", width=100, anchor="center")
    table.column("Course", width=220)

    table.pack(pady=20, fill="both", expand=True)

    def show_students():
        for row in table.get_children():
            table.delete(row)

        students = view_student(file_entry.get())

        if students is None:
            messagebox.showerror("Error", "File Not Found")
            return

        if not students:
            messagebox.showinfo("Information", "No Students Found")
            return

        for student in students:
            table.insert("", "end", values=student)

    ctk.CTkButton(
        window,
        text="View Students",
        command=show_students
    ).pack(pady=10)


# -------------------------------
# Search Student Popup
# -------------------------------

def gui_search():
    window = ctk.CTkToplevel(app)
    window.title("Search Student")
    window.geometry("650x400")

    file_entry = ctk.CTkEntry(window, placeholder_text="File Name")
    file_entry.pack(pady=10)

    name_entry = ctk.CTkEntry(window, placeholder_text="Student Name")
    name_entry.pack(pady=10)

    table = ttk.Treeview(
        window,
        columns=("Name", "Age", "Course"),
        show="headings",
        height=5
    )

    table.heading("Name", text="Name")
    table.heading("Age", text="Age")
    table.heading("Course", text="Course")

    table.pack(fill="both", expand=True, pady=20)

    def search():
        for row in table.get_children():
            table.delete(row)

        result = search_student(
            file_entry.get(),
            name_entry.get()
        )

        if result == "File Not Found":
            messagebox.showerror("Error", "File Not Found")

        elif result is None:
            messagebox.showinfo("Search", "Student Not Found")

        else:
            table.insert("", "end", values=result)

    ctk.CTkButton(
        window,
        text="Search Student",
        command=search
    ).pack(pady=10)


# -------------------------------
# Delete Student Popup
# -------------------------------

def gui_delete():
    window = ctk.CTkToplevel(app)
    window.title("Delete Student")
    window.geometry("400x250")

    title = ctk.CTkLabel(
        window,
        text="Delete Student",
        font=("Segoe UI", 20, "bold")
    )
    title.pack(pady=15)

    file_entry = ctk.CTkEntry(
        window,
        placeholder_text="File Name"
    )
    file_entry.pack(pady=10)

    name_entry = ctk.CTkEntry(
        window,
        placeholder_text="Student Name"
    )
    name_entry.pack(pady=10)

    def delete():
        confirm = messagebox.askyesno(
            "Delete Student",
            "Are you sure you want to delete this student?"
        )

        if not confirm:
            return

        result = delete_student(
            file_entry.get(),
            name_entry.get()
        )

        if result is None:
            messagebox.showerror(
                "Error",
                "File Not Found"
            )

        elif result:
            messagebox.showinfo(
                "Success",
                "Student Deleted Successfully"
            )
            window.destroy()

        else:
            messagebox.showwarning(
                "Not Found",
                "Student Not Found"
            )

    ctk.CTkButton(
        window,
        text="🗑 Delete Student",
        fg_color="#D32F2F",
        hover_color="#B71C1C",
        command=delete
    ).pack(pady=20)


# -------------------------------
# Main UI
# -------------------------------

title = ctk.CTkLabel(
    app,
    text="📚 Student Management System",
    font=("Segoe UI", 28, "bold")
)
title.pack(pady=30)

subtitle = ctk.CTkLabel(
    app,
    text="Manage Student Records Easily",
    font=("Segoe UI", 15)
)
subtitle.pack(pady=(0, 25))

frame = ctk.CTkFrame(app, width=400, height=300)
frame.pack(pady=20)
frame.pack_propagate(False)

buttons = [
    ("➕ Add Student", gui_add, None),
    ("📄 View Students", gui_view, None),
    ("🔍 Search Student", gui_search, None),
    ("🗑 Delete Student", gui_delete, ("#D32F2F", "#B71C1C")),
]

for text, cmd, colors in buttons:
    kwargs = {}
    if colors:
        kwargs["fg_color"] = colors[0]
        kwargs["hover_color"] = colors[1]

    ctk.CTkButton(
        frame,
        text=text,
        command=cmd,
        width=250,
        height=45,
        font=("Segoe UI", 16),
        **kwargs
    ).pack(pady=10)

footer = ctk.CTkLabel(
    app,
    text="Made with ❤️ using Python & CustomTkinter",
    font=("Segoe UI", 12)
)
footer.pack(side="bottom", pady=15)

app.mainloop()
