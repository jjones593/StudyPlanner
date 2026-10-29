import tkinter as tk

def addSchoolCourse(mainwindow, schoolcourses_list):
    schoolcoursewindow = tk.Toplevel(mainwindow)
    schoolcoursewindow.title("Add a Course")
    schoolcoursewindow.geometry("350x250")
    schoolcoursewindow.resizable(False, False)
    
    ## course name input
    schoolcoursename_label = tk.Label(schoolcoursewindow, text = "Course Name")
    schoolcoursename_label.pack(pady = (15, 5))
    schoolcoursename_entry = tk.Entry(schoolcoursewindow, width = 30)
    schoolcoursename_entry.pack()

    ## course code input
    schoolcoursecode_label = tk.Label(schoolcoursewindow, text = "Course code")
    schoolcoursecode_label.pack(pady = (15, 5))
    schoolcoursecode_entry = tk.Entry(schoolcoursewindow, width = 30)
    schoolcoursecode_entry.pack()

    ##save and cancel buttons
    schoolcoursebuttons = tk.Frame(schoolcoursewindow)
    schoolcoursebuttons.pack(pady = 20)
    saveschoolcourse_button = tk.Button(schoolcoursebuttons, text = "Save", width = 10)
    saveschoolcourse_button.pack(side = "left", padx = 5)
    cancelschoolcourse_button = tk.Button(schoolcoursebuttons, text = "Cancel", width = 10, command = schoolcoursewindow.destroy)
    cancelschoolcourse_button.pack(side = "left", padx = 5)
    ## allows courses to be actually saved
    def saveSchoolCourse():
        schoolcoursename = schoolcoursename_entry.get()
        schoolcoursecode = schoolcoursecode_entry.get()

        schoolcourses_list.insert(tk.END, schoolcoursename + schoolcoursecode)
        schoolcoursewindow.destroy()

    saveschoolcourse_button.config(command = saveSchoolCourse)









