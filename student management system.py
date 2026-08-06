import customtkinter as ctk
import tkinter.ttk as ttk
from tkinter import messagebox
import os
import csv

update = []



def add_student(file, student, age, course):
    data = file + ".csv"
    file_exist = os.path.exists(data)
    with open(data, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exist:
            writer.writerow(["Name", "Age", "Course"])
            file_entry = ctk.CTkEntry(app)

            name_entry = ctk.CTkEntry(app)

            age_entry = ctk.CTkEntry(app)

        course_entry = ctk.CTkEntry(app)
        
        writer.writerow([student, age, course])
        messagebox.showinfo(
                "Success",
                "Student Added Successfully!")
        

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
        add_student(
            file_entry.get(),
            name_entry.get(),
            age_entry.get(),
            course_entry.get()
        )
        window.destroy()

    ctk.CTkButton(window, text="Save", command=save).pack(pady=20)
   

def view_student(file):
    try:
        data = file + ".csv"
        with open(data, "r") as f:
            read = csv.reader(f)
            students = []
            for row in read:
                students.append(row)

        return students

    except FileNotFoundError:
        messagebox.showerror(
    "Error",
    "File Not Found!"
)

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

    

    table.column("Name", width=220)
    table.column("Age", width=100, anchor="center")
    table.column("Course", width=220)

    table.pack(pady=20, fill="both", expand=True)

    def show_students():

        # Purani rows delete karo
        for row in table.get_children():
            table.delete(row)

        students = view_student(file_entry.get())

        if students is None:
            messagebox.showerror("Error", "File Not Found")
            return

        for student in students:
            table.insert("", "end", values=student)

    ctk.CTkButton(
        window,
        text="View Students",
        command=show_students
    ).pack(pady=10)


def search_student(file, name):
    try:
        data = file + ".csv"
        with open(data, "r") as f:
            read = csv.reader(f)
            found = False
            next(read)
            for row in read:
                if row[0] == name:
                    found = True
                    return None
            if found:
                print(row)
            else:
                print("File Not Found")

    except FileExistsError:
        messagebox.ERROR(
    "Error",
    "File Not Found!"
)
            
       


def gui_search():

    window = ctk.CTkToplevel(app)
    window.title("Search Student")
    window.geometry("650x400")

    # File Name
    file_entry = ctk.CTkEntry(window, placeholder_text="File Name")
    file_entry.pack(pady=10)

    # Student Name
    name_entry = ctk.CTkEntry(window, placeholder_text="Student Name")
    name_entry.pack(pady=10)

    # Table
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

        # Purani row delete karo
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
def delete_student(file, name):

    data = file + ".csv"
    updated = []
    found = False

    try:
        with open(data, "r") as f:
            reader = csv.reader(f)

            header = next(reader)
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

def gui_delete():

    window = ctk.CTkToplevel(app)
    window.title("Delete Student")
    window.geometry("400x250")

    title = ctk.CTkLabel(
        window,
        text="Delete Student",
        font=("Segoe UI",20,"bold")
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
        fg_color="red",
        hover_color="darkred",
        command=delete
    ).pack(pady=20)

            



ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Student Management System")
app.geometry("700x500")
app.resizable(False, False)

import customtkinter as ctk

app = ctk.CTk()
app.title("Student Management System")
app.geometry("700x500")
app.resizable(False, False)
app.iconbitmap("graduated.ico")


# -------------------------------
# TITLE
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
subtitle.pack(pady=(0,25))


# -------------------------------
# BUTTON FRAME
# -------------------------------

frame = ctk.CTkFrame(app, width=400, height=300)
frame.pack(pady=20)

frame.pack_propagate(False)


# -------------------------------
# BUTTONS
# -------------------------------

btn1 = ctk.CTkButton(
    frame,
    text="➕ Add Student",
    command=gui_add,
    width=250,
    height=45,
    font=("Segoe UI",16)
)
btn1.pack(pady=10)


btn2 = ctk.CTkButton(
    frame,
    text="📄 View Students",
    command=gui_view,
    width=250,
    height=45,
    font=("Segoe UI",16)
)
btn2.pack(pady=10)


btn3 = ctk.CTkButton(
    frame,
    text="🔍 Search Student",
    command=gui_search,
    width=250,
    height=45,
    font=("Segoe UI",16)
)
btn3.pack(pady=10)


btn4 = ctk.CTkButton(
    frame,
    text="🗑 Delete Student",
    command=gui_delete,
    fg_color="#D32F2F",
    hover_color="#B71C1C",
    width=250,
    height=45,
    font=("Segoe UI",16)
)
btn4.pack(pady=10)


# -------------------------------
# FOOTER
# -------------------------------

footer = ctk.CTkLabel(
    app,
    text="Made with ❤️ using Python & CustomTkinter",
    font=("Segoe UI",12)
)

footer.pack(side="bottom", pady=15)

app.mainloop()  