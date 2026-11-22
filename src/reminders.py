import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime
from pathlib import Path
from notifications import addNotification, showAlert

datafile = Path(__file__).with_name("data.json")

CHECK_EVERY_MS = 30000  ##how often to look for due reminders (30 seconds)

def loadData():
    with open(datafile, "r") as file:
        return json.load(file)

def saveData(data):
    with open(datafile, "w") as file:
        json.dump(data, file)

def parseTime(text):
    ##Accepts 14:30, 2:30PM or 2:30 PM. Blank means 09:00. Returns "HH:MM" or None if invalid
    if not text:
        return "09:00"
    cleaned = text.upper().replace(" ", "")
    for fmt in ("%H:%M", "%I:%M%p"):
        try:
            return datetime.strptime(cleaned, fmt).strftime("%H:%M")
        except ValueError:
            pass
    return None

def loadReminders():
    ##Returns the data plus the reminders list, sorted by date then time
    data = loadData()
    reminders = data.setdefault("reminders", [])
    reminders.sort(key=lambda r: (r["date"], r["time"]))
    return data, reminders

def refreshReminders(listbox):
    data, reminders = loadReminders()
    listbox.delete(0, tk.END)
    for r in reminders:
        text = r["date"] + "  " + r["time"] + "  -  " + r["title"]
        if r.get("notified"):
            text += "  (sent)"
        listbox.insert(tk.END, text)

def checkReminders(listbox):
    ##Looks for reminders that are due, notifies once, and marks them as sent
    data, reminders = loadReminders()
    now = datetime.now()
    due = []
    for r in reminders:
        if r.get("notified"):
            continue
        try:
            when = datetime.strptime(r["date"] + " " + r["time"], "%Y-%m-%d %H:%M")
        except ValueError:
            continue
        if when <= now:
            r["notified"] = True
            due.append(r)

    if due:
        saveData(data)
        for r in due:
            addNotification("Reminder: " + r["title"])
        refreshReminders(listbox)
        showAlert("Study Planner", "\n".join(r["title"] for r in due))

def reminderWindow(parent, listbox, heading, reminder=None, index=None):
    ##Pop-up used for both adding and editing a reminder
    window = tk.Toplevel(parent)
    window.title(heading)
    window.geometry("350x300")
    window.transient(parent.winfo_toplevel())
    window.grab_set()

    tk.Label(window, text="Date (YYYY-MM-DD):", font=("Arial", 12)).pack(anchor="w", padx=20, pady=(15, 0))
    date_entry = tk.Entry(window, font=("Arial", 12))
    date_entry.insert(0, reminder["date"] if reminder else datetime.now().strftime("%Y-%m-%d"))
    date_entry.pack(fill="x", padx=20, pady=5)

    tk.Label(window, text="Time (e.g. 14:30 or 2:30PM, blank = 9:00):", font=("Arial", 12)).pack(anchor="w", padx=20, pady=(10, 0))
    time_entry = tk.Entry(window, font=("Arial", 12))
    if reminder:
        time_entry.insert(0, reminder["time"])
    time_entry.pack(fill="x", padx=20, pady=5)

    tk.Label(window, text="Reminder:", font=("Arial", 12)).pack(anchor="w", padx=20, pady=(10, 0))
    title_entry = tk.Entry(window, font=("Arial", 12))
    if reminder:
        title_entry.insert(0, reminder["title"])
    title_entry.pack(fill="x", padx=20, pady=5)

    def save():
        date_text = date_entry.get().strip()
        time_text = parseTime(time_entry.get().strip())
        title = title_entry.get().strip()

        try:
            datetime.strptime(date_text, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Invalid date", "Enter the date like 2026-11-05.", parent=window)
            return
        if time_text is None:
            messagebox.showwarning("Invalid time", "Enter the time like 14:30 or 2:30PM.", parent=window)
            return
        if not title:
            messagebox.showwarning("Missing reminder", "Please enter what you want to be reminded of.", parent=window)
            return

        data, reminders = loadReminders()
        ##If the date or time changed (or it's new), it should notify again
        notified = False
        if reminder and reminder["date"] == date_text and reminder["time"] == time_text:
            notified = reminder.get("notified", False)
        newReminder = {"title": title, "date": date_text, "time": time_text, "notified": notified}

        if index is None:
            reminders.append(newReminder)
        else:
            reminders[index] = newReminder
        saveData(data)

        refreshReminders(listbox)
        window.destroy()

    buttons = tk.Frame(window)
    buttons.pack(pady=15)
    tk.Button(buttons, text="Save", width=10, command=save).pack(side="left", padx=5)
    tk.Button(buttons, text="Cancel", width=10, command=window.destroy).pack(side="left", padx=5)

def viewReminders(reminders_tab):
    ##Builds everything on the Reminders tab and starts the checker
    tk.Label(reminders_tab, text="reminders", font=("Arial", 12, "bold")).pack(pady=15)

    reminders_list = tk.Listbox(reminders_tab, font=("Arial", 12), selectmode=tk.SINGLE, exportselection=False)
    reminders_list.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    refreshReminders(reminders_list)

    def addReminder():
        reminderWindow(reminders_tab, reminders_list, "Add Reminder")

    def editReminder():
        selection = reminders_list.curselection()
        if not selection:
            messagebox.showwarning("No reminder selected", "Please select a reminder to edit.", parent=reminders_tab)
            return
        index = selection[0]
        data, reminders = loadReminders()
        reminderWindow(reminders_tab, reminders_list, "Edit Reminder", reminders[index], index)

    def deleteReminder():
        selection = reminders_list.curselection()
        if not selection:
            messagebox.showwarning("No reminder selected", "Please select a reminder to delete.", parent=reminders_tab)
            return
        if not messagebox.askyesno("Delete reminder", "Are you sure you want to delete this reminder?", parent=reminders_tab):
            return
        data, reminders = loadReminders()
        reminders.pop(selection[0])
        saveData(data)
        refreshReminders(reminders_list)

    buttons = tk.Frame(reminders_tab)
    buttons.pack(pady=10)
    tk.Button(buttons, text="Add", width=10, command=addReminder).pack(side="left", padx=5)
    tk.Button(buttons, text="Edit", width=10, command=editReminder).pack(side="left", padx=5)
    tk.Button(buttons, text="Delete", width=10, command=deleteReminder).pack(side="left", padx=5)

    ##Check for due reminders shortly after startup, then every 30 seconds while the app is open
    def loop():
        try:
            checkReminders(reminders_list)
        except Exception as error:
            print("Reminder check failed:", error)
        reminders_tab.after(CHECK_EVERY_MS, loop)

    reminders_tab.after(1000, loop)
