import tkinter as tk
from tkinter import messagebox
import json
from pathlib import Path

def deleteCalendarEvent(selecteddate, calendareventlist, showCalendar):
    selected = calendareventlist.curselection()

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

    confirmdelete = messagebox.askyesno("Delete?")
    if confirmdelete:
            data["events"].remove(event)
            with open(datafile, "w") as file:
                json.dump(data, file, indent = 5)

            calendareventlist.delete(selected[0])
            showCalendar()