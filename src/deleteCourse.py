import tkinter as tk
from tkinter import messagebox
import json
from pathlib import Path

def deleteSchoolCourse(mainwindow, schoolcourses_list):
    selectedschoolcourse = schoolcourses_list.curselection()

    if not selectedschoolcourse:
        return

    confirmdeletecourse = messagebox.askyesno("Delete Course?", "Are you Sure?", parent = mainwindow)
    if not confirmdeletecourse:
        return

    datafile = Path(__file__).with_name("data.json")
    with open(datafile, "r") as file:
        data = json.load(file)
        courseindex = selectedschoolcourse[0]

        data["courses"].pop(courseindex)
        with open(datafile, "w") as file:
            json.dump(data, file, indent = 5)
            schoolcourses_list.delete(courseindex)
