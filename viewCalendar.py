import tkinter as tk 
import calendar
from datetime import datetime 
from addEvent import addEvent
import json
from pathlib import Path
from editEvent import editCalendarEvent
from deleteEvent import deleteCalendarEvent

def viewCalendar(calendar_tab):
    today = datetime.now()
    selectedmonth = [today.year, today.month]
##main frame    
    monthlycalendar = tk.Frame(calendar_tab)
    monthlycalendar.pack(fill="both", expand = True, padx = 20, pady = 10)
##month/year title
    monthtitle = tk.Label(monthlycalendar, font = ("Arial", 16, "bold"))
    monthtitle.pack(pady = 10)

##frame for dates    
    calendargrid=tk.Frame(monthlycalendar)
    calendargrid.pack(fill = "both", expand = True)

    def selectEvent(selecteddate):
       calendareventwindow = tk.Toplevel(calendar_tab)
       calendareventwindow.title("Events")
       calendareventwindow.geometry("300x300")

       calendareventlist = tk.Listbox(calendareventwindow, width = 40)
       calendareventlist.pack(pady = 15)

       datafile = Path(__file__).with_name("data.json")
       with open(datafile, "r") as file:
          data = json.load(file)

          for event in data["events"]:
             if event["date"] == selecteddate:
                calendareventlist.insert(tk.END, event["title"])

          addbutton = tk.Button(calendareventwindow, text = "Add", command = lambda: addEvent(calendar_tab, selecteddate, showCalendar))
          addbutton.pack(pady = 5)
          editbutton = tk.Button(calendareventwindow, text = "Edit", command = lambda: editCalendarEvent(calendareventwindow, selecteddate, calendareventlist, showCalendar))
          editbutton.pack(pady = 5)
          deletebutton = tk.Button(calendareventwindow, text = "Delete", command = lambda: deleteCalendarEvent(selecteddate, calendareventlist, showCalendar))
          deletebutton.pack(pady = 5)
       

    def showCalendar():
    ##this will destroy the current page month we are when we switch to the next so only one month displays at a ti
     for widget in calendargrid.winfo_children():
        widget.destroy()
     
     displayyear = selectedmonth[0]
     displaymonth = selectedmonth[1]

     datafile = Path(__file__).with_name("data.json")
     with open(datafile, "r") as file:
        data = json.load(file)

     monthtitle.config(text = calendar.month_name[displaymonth] + str(displayyear))
##day headings
     daynames = ["Mon", "Tues", "Wed", "Thu", "Fri", "Sat", "Sun"]
     for col in range(7):
        datelabel = tk.Label(calendargrid, text = daynames[col])
        datelabel.grid(row = 0, column = col, padx = 5, pady = 5)

     monthweeks = calendar.monthcalendar(displayyear, displaymonth)
     for row in range(len(monthweeks)):
        for col in range(7):
           day = monthweeks[row][col]
           if day != 0:
              selecteddate = str(displayyear) + "-" + str(displaymonth) + "-" + str(day)
              buttontext = str(day)
              for event in data["events"]:
                 if event["date"] == selecteddate:
                    buttontext = buttontext + "\n" + event["title"] + "\n" + event["time"]           
              datebutton = tk.Button(calendargrid, text = buttontext, command = lambda date = selecteddate: selectEvent(date))
              datebutton.grid(row = row + 1, column = col, sticky = "nsew", padx = 3, pady = 3)
    
    for col in range(7):
       calendargrid.grid_columnconfigure(col, weight = 1)
    for row in range(1, 7):
       calendargrid.grid_rowconfigure(row, weight = 1)

    def goForwardMonth():
        selectedmonth[1] += 1
        if selectedmonth[1] == 13:
            selectedmonth[1] = 1
            selectedmonth[0] += 1
        showCalendar()

    def goBackMonth():
        selectedmonth[1] -= 1
        if selectedmonth[1] == 0:
            selectedmonth[1] = 12
            selectedmonth[0] -= 1
        showCalendar()

    monthbuttons = tk.Frame(monthlycalendar)
    monthbuttons.pack(pady = 10)

    backbutton = tk.Button(monthbuttons, text = "Previous", width = 10, command = goBackMonth)
    backbutton.pack(side = "left", padx = 5)
    forwardbutton = tk.Button(monthbuttons, text = "Next", width = 10, command = goForwardMonth)
    forwardbutton.pack(side = "left", padx = 5)

    showCalendar()   



