import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime
from pathlib import Path

datafile = Path(__file__).with_name("data.json")

##The notifications listbox, set when the tab is built so new notifications can refresh it
_list = None


def loadData():
    with open(datafile, "r") as file:
        return json.load(file)


def saveData(data):
    with open(datafile, "w") as file:
        json.dump(data, file)


def showAlert(title, message):
    ##Small pop-up in the bottom-right corner of the screen. Click it to close, or it closes itself after 8 seconds
    root = tk._default_root
    if root is None:
        return

    background = "#333333"
    popup = tk.Toplevel(root)
    popup.overrideredirect(True)
    popup.attributes("-topmost", True)
    popup.configure(bg=background)

    tk.Label(popup, text=title, font=("Arial", 11, "bold"), bg=background, fg="white").pack(anchor="w", padx=15, pady=(10, 0))
    tk.Label(popup, text=message, font=("Arial", 11), bg=background, fg="white", wraplength=280, justify="left").pack(anchor="w", padx=15, pady=(2, 10))

    popup.update_idletasks()
    x = popup.winfo_screenwidth() - popup.winfo_reqwidth() - 20
    y = popup.winfo_screenheight() - popup.winfo_reqheight() - 60
    popup.geometry("+" + str(x) + "+" + str(y))

    def close(event=None):
        try:
            popup.destroy()
        except tk.TclError:
            pass

    popup.bind("<Button-1>", close)
    for child in popup.winfo_children():
        child.bind("<Button-1>", close)
    popup.after(8000, close)


def addNotification(message):
    ##Saves a notification to data.json and refreshes the Notifications tab
    data = loadData()
    data.setdefault("notifications", []).append({
        "message": message,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    saveData(data)
    if _list is not None:
        refreshNotifications(_list)


def refreshNotifications(listbox):
    ##Newest notification at the top
    data = loadData()
    listbox.delete(0, tk.END)
    for n in reversed(data.get("notifications", [])):
        listbox.insert(tk.END, n["time"] + "  -  " + n["message"])


def viewNotifications(notifications_tab):
    global _list
    tk.Label(notifications_tab, text="notifications", font=("Arial", 12, "bold")).pack(pady=15)

    notifications_list = tk.Listbox(notifications_tab, font=("Arial", 12), selectmode=tk.SINGLE, exportselection=False)
    notifications_list.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    _list = notifications_list
    refreshNotifications(notifications_list)

    def deleteSelected():
        selection = notifications_list.curselection()
        if not selection:
            messagebox.showwarning("Nothing selected", "Please select a notification to delete.", parent=notifications_tab)
            return
        data = loadData()
        notes = data.get("notifications", [])
        ##The list shows newest first, so flip the position to find it in the file
        notes.pop(len(notes) - 1 - selection[0])
        saveData(data)
        refreshNotifications(notifications_list)

    def clearAll():
        if not messagebox.askyesno("Clear all", "Delete all notifications?", parent=notifications_tab):
            return
        data = loadData()
        data["notifications"] = []
        saveData(data)
        refreshNotifications(notifications_list)

    buttons = tk.Frame(notifications_tab)
    buttons.pack(pady=10)
    tk.Button(buttons, text="Delete", width=10, command=deleteSelected).pack(side="left", padx=5)
    tk.Button(buttons, text="Clear All", width=10, command=clearAll).pack(side="left", padx=5)
