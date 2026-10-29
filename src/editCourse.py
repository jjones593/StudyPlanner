import tkinter as tk
import json
from pathlib import Path

def editSchoolCourse(mainwindow, schoolcourses_list):
    selectedschoolcourse = schoolcourses_list.curselection()

    if not selectedschoolcourse:
        return

    datafile = Path(__file__).with_name("data.json")
    with open(datafile, "r") as file:
        data = json.load(file)
    courseindex = selectedschoolcourse[0]
    course = data["courses"][courseindex]

    ##this is the edit course window
    editschoolcoursewindow = tk.Toplevel(mainwindow)
    editschoolcoursewindow.title("Edit")
    editschoolcoursewindow.geometry("350x250")
    editschoolcoursewindow.resizable(False, False)

    #name input
    schoolcoursename_label = tk.Label(editschoolcoursewindow, text = "Course Name")
    schoolcoursename_label.pack(pady = (15,5))
    schoolcoursename_entry = tk.Entry(editschoolcoursewindow, width = 30)
    schoolcoursename_entry.pack()
    schoolcoursename_entry.insert(0, course["name"])

    #code input
    schoolcoursecode_label = tk.Label(editschoolcoursewindow, text = "course code")
    schoolcoursecode_label.pack(pady = (15, 5))
    schoolcoursecode_entry = tk.Entry(editschoolcoursewindow, width = 30)
    schoolcoursecode_entry.pack()
    schoolcoursecode_entry.insert(0, course["code"])

    ## save and cancel
    schoolcourse_buttons = tk.Frame(editschoolcoursewindow)
    schoolcourse_buttons.pack(pady = 20)
    saveschoolcourse_button = tk.Button(schoolcourse_buttons, text = "Save", width = 10)
    saveschoolcourse_button.pack(side = "left", padx = 5)
    cancelschoolcourse_button = tk.Button(schoolcourse_buttons, text = "Cancel", width = 10, command = editschoolcoursewindow.destroy)
    cancelschoolcourse_button.pack(side = "left", padx = 5)

    def saveEditedSchoolCourse():
        schoolcoursename = schoolcoursename_entry.get()
        schoolcoursecode = schoolcoursecode_entry.get()

        data["courses"][courseindex]["name"] = schoolcoursename
        data["courses"][courseindex]["code"] = schoolcoursecode

        with open(datafile, "w") as file:
           json.dump(data, file, indent = 5)

           schoolcourses_list.delete(courseindex)
           schoolcourses_list.insert(courseindex, schoolcoursename + schoolcoursecode)
           editschoolcoursewindow.destroy()
        
    saveschoolcourse_button.config(command = saveEditedSchoolCourse)



















