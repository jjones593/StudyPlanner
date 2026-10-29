import tkinter as tk
from tkinter import messagebox
import json
from pathlib import Path
 
datafile = Path(__file__).with_name("data.json")
 
def deleteCustomNote(mainwindow, customnotes_list):
    selection = customnotes_list.curselection()
    if not selection:
        messagebox.showwarning("No note selected", "Please select a note to delete.", parent=mainwindow)
        return
    index = selection[0]

    title = customnotes_list.get(index)
    if not messagebox.askyesno("Delete note", f'Are you sure you want to delete "{title}"?', parent=mainwindow):
        return

    with open(datafile, "r") as file:
        data = json.load(file)
 
    data["notes"].pop(index)
 
    with open(datafile, "w") as file:
        json.dump(data, file, indent=5)

    customnotes_list.delete(index)
