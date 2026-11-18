import tkinter as tk
import json
from pathlib import Path

def addEvent(mainwindow, selecteddate, showCalendar):
    calendareventwindow = tk.Toplevel(mainwindow)
    calendareventwindow.title("Add Event to Calender")
    calendareventwindow.geometry("450x450")

    calendareventsubject = tk.Label(calendareventwindow, text = "Event Subject")
    calendareventsubject.pack(pady = (15, 5))
    calendarevententry = tk.Entry(calendareventwindow, width = 30)
    calendarevententry.pack() 

    calendareventdate = tk.Label(calendareventwindow, text = "Date" + selecteddate)
    calendareventdate.pack(pady = 5)

    calendareventtime = tk.Label(calendareventwindow, text = "Time")
    calendareventtime.pack(pady = 5)

    calendareventtimeentry = tk.Entry(calendareventwindow, width = 30)
    calendareventtimeentry.pack()

    calendarcourse = tk.Label(calendareventwindow, text = "Course")
    calendarcourse.pack(pady = 5)

    calendarcourseentry = tk.Entry(calendareventwindow, width = 30)
    calendarcourseentry.pack()

    def saveCalendarEvent():
        datafile = Path(__file__).with_name("data.json")
        with open(datafile, "r") as file:
            data = json.load(file)

            newcalendarevent = {
                "title": calendarevententry.get(), "date": selecteddate, "time": calendareventtimeentry.get(), "course": calendarcourseentry.get()
                
            }
            data["events"].append(newcalendarevent)
            with open(datafile, "w") as file:
                json.dump(data, file)

                showCalendar()
                calendareventwindow.destroy()



    savebutton = tk.Button(calendareventwindow, text = "Save", command = saveCalendarEvent)
    savebutton.pack(pady = 15)

    cancelbutton = tk.Button(calendareventwindow, text = "Cancel", command = calendareventwindow.destroy)
    cancelbutton.pack()




