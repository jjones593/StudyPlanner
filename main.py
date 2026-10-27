import tkinter as tk
from tkinter import ttk, messagebox

courses = []
notes = []


def refresh_lists():
    course_list.delete(0, tk.END)
    note_list.delete(0, tk.END)

    for course in courses:
        course_list.insert(tk.END, course["code"] + " - " + course["name"])

    for note in notes:
        note_list.insert(tk.END, note["title"])


def feature_message(feature):
    messagebox.showinfo(feature, "This feature is not connected yet.")


# Course functions

def add_course():
    # US-01
    feature_message("Add Course")

def edit_course():
    # US-02
    feature_message("Edit Course")

def delete_course():
    # US-02
    feature_message("Delete Course")

# Note functions

def add_note():
    # US-10
    feature_message("Add Note")

def edit_note():
    # US-11
    feature_message("Edit Note")

def delete_note():
    # US-11
    feature_message("Delete Note")


# Main window
if __name__ == "__main__":
    window = tk.Tk()
    window.title("Student Study Planner")
    window.geometry("750x550")

    main_frame = ttk.Frame(window, padding=20)
    main_frame.pack(fill="both", expand=True)

    title = ttk.Label(main_frame, text="Student Study Planner", font=("Arial", 20))
    title.pack(pady=10)

    # Tabs
    tabs = ttk.Notebook(main_frame)
    tabs.pack(fill="both", expand=True)

    course_tab = ttk.Frame(tabs, padding=15)
    note_tab = ttk.Frame(tabs, padding=15)

    tabs.add(course_tab, text="Courses")
    tabs.add(note_tab, text="Notes")

    # Courses tab
    ttk.Label(course_tab, text="My Courses", font=("Arial", 14)).pack(pady=10)

    course_list = tk.Listbox(course_tab, height=10)
    course_list.pack(fill="both", expand=True, pady=10)

    course_buttons = ttk.Frame(course_tab)
    course_buttons.pack(pady=10)

    ttk.Button(course_buttons, text="Add Course", command=add_course).pack(side="left", padx=5)
    ttk.Button(course_buttons, text="Edit Course", command=edit_course).pack(side="left", padx=5)
    ttk.Button(course_buttons, text="Delete Course", command=delete_course).pack(side="left", padx=5)

    # Notes tab
    ttk.Label(note_tab, text="My Notes", font=("Arial", 14)).pack(pady=10)

    note_list = tk.Listbox(note_tab, height=10)
    note_list.pack(fill="both", expand=True, pady=10)

    note_buttons = ttk.Frame(note_tab)
    note_buttons.pack(pady=10)

    ttk.Button(note_buttons, text="Add Note", command=add_note).pack(side="left", padx=5)
    ttk.Button(note_buttons, text="Edit Note", command=edit_note).pack(side="left", padx=5)
    ttk.Button(note_buttons, text="Delete Note", command=delete_note).pack(side="left", padx=5)

    refresh_lists()
    window.mainloop()
