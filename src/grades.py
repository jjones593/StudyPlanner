ort tkinter as tk
from tkinter import ttk, messagebox
import json
from pathlib import Path

datafile = Path(__file__).with_name("data.json")

def loadData():
    with open(datafile, "r") as file:
        return json.load(file)

def saveData(data):
    with open(datafile, "w") as file:
        json.dump(data, file)

def formatGrade(entry):
    text = entry["course"]
    if entry["assessment"]:
        text += "  -  " + entry["assessment"]
    text += "  :  " + format(entry["grade"], "g") + "%"
    return text

def refreshGrades(grades_list):
    data = loadData()
    grades_list.delete(0, tk.END)
    for entry in data.get("grades", []):
        grades_list.insert(tk.END, formatGrade(entry))

def gradeWindow(parent, grades_list, heading, entry=None, index=None):
    ##Pop-up used for both adding and editing a grade
    window = tk.Toplevel(parent)
    window.title(heading)
    window.geometry("350x300")
    window.transient(parent.winfo_toplevel())
    window.grab_set()

    ##Course list comes from the courses already added (you can also type a new one)
    courses = [c["name"] for c in loadData().get("courses", [])]

    tk.Label(window, text="Course:", font=("Arial", 12)).pack(anchor="w", padx=20, pady=(15, 0))
    course_box = ttk.Combobox(window, font=("Arial", 12), values=courses)
    if entry:
        course_box.set(entry["course"])
    course_box.pack(fill="x", padx=20, pady=5)

    tk.Label(window, text="Assessment (optional, e.g. Midterm):", font=("Arial", 12)).pack(anchor="w", padx=20, pady=(10, 0))
    assessment_entry = tk.Entry(window, font=("Arial", 12))
    if entry:
        assessment_entry.insert(0, entry["assessment"])
    assessment_entry.pack(fill="x", padx=20, pady=5)

    tk.Label(window, text="Grade (%):", font=("Arial", 12)).pack(anchor="w", padx=20, pady=(10, 0))
    grade_entry = tk.Entry(window, font=("Arial", 12))
    if entry:
        grade_entry.insert(0, format(entry["grade"], "g"))
    grade_entry.pack(fill="x", padx=20, pady=5)

    def save():
        course = course_box.get().strip()
        assessment = assessment_entry.get().strip()
        grade_text = grade_entry.get().strip().replace("%", "")

        if not course:
            messagebox.showwarning("Missing course", "Please enter or choose a course.", parent=window)
            return
        try:
            grade = float(grade_text)
        except ValueError:
            messagebox.showwarning("Invalid grade", "Enter the grade as a number, like 85.", parent=window)
            return
        if grade < 0 or grade > 100:
            messagebox.showwarning("Invalid grade", "The grade must be between 0 and 100.", parent=window)
            return

        data = loadData()
        grades = data.setdefault("grades", [])
        newEntry = {"course": course, "assessment": assessment, "grade": grade}
        if index is None:
            grades.append(newEntry)
        else:
            grades[index] = newEntry
        saveData(data)

        refreshGrades(grades_list)
        window.destroy()

    buttons = tk.Frame(window)
    buttons.pack(pady=15)
    tk.Button(buttons, text="Save", width=10, command=save).pack(side="left", padx=5)
    tk.Button(buttons, text="Cancel", width=10, command=window.destroy).pack(side="left", padx=5)

def viewGrades(grades_tab):
    ##Builds everything on the Grades tab: heading, list, and Add/Edit/Delete buttons
    tk.Label(grades_tab, text="grades", font=("Arial", 12, "bold")).pack(pady=15)

    grades_list = tk.Listbox(grades_tab, font=("Arial", 12), selectmode=tk.SINGLE, exportselection=False)
    grades_list.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    refreshGrades(grades_list)

    def addGrade():
        gradeWindow(grades_tab, grades_list, "Add Grade")

    def editGrade():
        selection = grades_list.curselection()
        if not selection:
            messagebox.showwarning("No grade selected", "Please select a grade to edit.", parent=grades_tab)
            return
        index = selection[0]
        entry = loadData()["grades"][index]
        gradeWindow(grades_tab, grades_list, "Edit Grade", entry, index)

    def deleteGrade():
        selection = grades_list.curselection()
        if not selection:
            messagebox.showwarning("No grade selected", "Please select a grade to delete.", parent=grades_tab)
            return
        index = selection[0]
        if not messagebox.askyesno("Delete grade", "Are you sure you want to delete this grade?", parent=grades_tab):
            return
        data = loadData()
        data["grades"].pop(index)
        saveData(data)
        refreshGrades(grades_list)

    buttons = tk.Frame(grades_tab)
    buttons.pack(pady=10)
    tk.Button(buttons, text="Add", width=10, command=addGrade).pack(side="left", padx=5)
    tk.Button(buttons, text="Edit", width=10, command=editGrade).pack(side="left", padx=5)
    tk.Button(buttons, text="Delete", width=10, command=deleteGrade).pack(side="left", padx=5)
    