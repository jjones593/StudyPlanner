import tkinter as tk
import json
from pathlib import Path

def editCalendarEvent(mainwindow, selecteddate, eventlist, showCalendar):
    selected = eventlist.curselection()

    if not selected:
        return

    datafile = Path(__file__).with_name("data.json")

    with open(datafile, "r") as file:
        data = json.load(file)

    events = []
    for event in data["events"]:
        if event["date"] == selecteddate:
            events.append(event)

    event = events[selected[0]]

    calendareditwindow = tk.Toplevel(mainwindow)
    calendareditwindow.title("Edit Calendar Event")
    calendareditwindow.geometry("450x450")

    tk.Label(calendareditwindow, text = "Event Subject").pack(pady = 5)
    calendarevententry = tk.Entry(calendareditwindow, width = 30)
    calendarevententry.pack()
    calendarevententry.insert(0, event["title"])

    tk.Label(calendareditwindow, text = "Time").pack(pady = 5)
    calendareventtimeentry = tk.Entry(calendareditwindow, width = 30)
    calendareventtimeentry.pack()
    calendareventtimeentry.insert(0, event["time"])

    tk.Label(calendareditwindow, text = "Course").pack(pady = 5)
    calendarcourseentry = tk.Entry(calendareditwindow, width = 30)
    calendarcourseentry.pack()
    calendarcourseentry.insert(0, event["course"])

    def saveCalendarEvent():
        event["title"] = calendarevententry.get()
        event["time"] = calendareventtimeentry.get()
        event["course"] = calendarcourseentry.get()

        with open(datafile, "w") as file:
            json.dump(data, file, indent = 4)

        eventlist.delete(selected[0])
        eventlist.insert(selected[0], event["title"])

        showCalendar()
        calendareditwindow.destroy()

    savebutton = tk.Button(calendareditwindow, text = "Save", command = saveCalendarEvent)
    savebutton.pack(pady = 15)

    cancelbutton = tk.Button(calendareditwindow, text = "Cancel", command = calendareditwindow.destroy)
    cancelbutton.pack()


