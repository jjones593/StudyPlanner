import tkinter as tk
from tkinter import ttk
from addCourse import addSchoolCourse 
import json
from pathlib import Path

##Code for creating our main window with its title and size 
mainwindow = tk.Tk()
mainwindow.title("Study Planner")
mainwindow.geometry("750x550")
mainwindow.minsize(550, 400)

##Title for our inital page
title = tk.Label (mainwindow, text = "Study Planner", font = ("Arial", 24, "bold"))
title.pack(anchor="w", padx=20, pady=(10,25))

##Creating the seperate tabs for courses and notes 
tab = ttk.Notebook(mainwindow)
tab.pack(fill = "both", expand = True, padx = 20, pady = (0, 20))
schoolcourses_tab = tk.Frame(tab)
customnotes_tab = tk.Frame(tab)
tab.add(schoolcourses_tab, text = "Courses")
tab.add(customnotes_tab, text = "Notes")

##Creating the courses and notes headings within there seperate tabs
schoolcourses_heading = tk.Label(schoolcourses_tab, text = "courses", font = ("Arial", 12, "bold"))
schoolcourses_heading.pack(pady = 15)
customnotes_heading = tk.Label(customnotes_tab, text = "notes", font = ("Arial", 12, "bold"))
customnotes_heading.pack(pady = 15)

##Creating the lists to be able to Display added courses and added notes
schoolcourses_list = tk.Listbox(schoolcourses_tab, font = ("Arial", 12), selectmode = tk.SINGLE, exportselection = False)
schoolcourses_list.pack(fill = "both", expand = True, padx = 20, pady = (0,20))
customnotes_list = tk.Listbox(customnotes_tab, font = ("Arial", 12), selectmode = tk.SINGLE, exportselection = False)
customnotes_list.pack(fill = "both", expand = True, padx = 20, pady = (0,20))

##saved courses from json file
datafile = Path(__file__).with_name("data.json")
with open(datafile, "r") as file:
    data=json.load(file)

for course in data ["courses"]:
    schoolcourses_list.insert(tk.END, course["name"] + course["code"])

##Add edit and delete button on both tabs
schoolcourses_buttons = tk.Frame(schoolcourses_tab)
schoolcourses_buttons.pack(pady = 10) 
customnotes_buttons = tk.Frame(customnotes_tab)
customnotes_buttons.pack(pady = 10)

addschoolcourse_button = tk.Button(schoolcourses_buttons, text = "Add", width = 10, command = lambda: addSchoolCourse(mainwindow, schoolcourses_list))
addschoolcourse_button.pack(side = "left", padx = 5)
addcustomnotes_button = tk.Button(customnotes_buttons, text = "Add", width = 10)
addcustomnotes_button.pack(side = "left", padx = 5)

editschoolcourse_button = tk.Button(schoolcourses_buttons, text = "Edit", width = 10)
editschoolcourse_button.pack(side = "left", padx = 5)
editcustomnotes_button = tk.Button(customnotes_buttons, text = "Edit", width = 10)
editcustomnotes_button.pack(side = "left", padx = 5)

deleteschoolcourse_button = tk.Button(schoolcourses_buttons, text = "Delete", width = 10)
deleteschoolcourse_button.pack(side = "left", padx = 5)
deletecustomnotes_button = tk.Button(customnotes_buttons, text = "Delete", width = 10)
deletecustomnotes_button.pack(side = "left", padx = 5)










mainwindow.mainloop()
