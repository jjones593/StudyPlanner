import tkinter as tk
from tkinter import messagebox
import json
from pathlib import Path
 
datafile = Path(__file__).with_name("data.json")
 
 
def editCustomNote(mainwindow, customnotes_list):
    selection = customnotes_list.curselection()
    if not selection:
        messagebox.showwarning("No note selected", "Please select a note to edit.", parent=mainwindow)
        return
    index = selection[0]

    with open(datafile, "r") as file:
        data = json.load(file)
    note = data["notes"][index]

    window = tk.Toplevel(mainwindow)
    window.title("Edit Note")
    window.geometry("400x350")
    window.transient(mainwindow)
    window.grab_set()
 
    tk.Label(window, text="Title:", font=("Arial", 12)).pack(anchor="w", padx=20, pady=(15, 0))
    title_entry = tk.Entry(window, font=("Arial", 12))
    title_entry.insert(0, note["title"])
    title_entry.pack(fill="x", padx=20, pady=5)
 
    tk.Label(window, text="Note:", font=("Arial", 12)).pack(anchor="w", padx=20, pady=(10, 0))
    note_text = tk.Text(window, font=("Arial", 12), height=8, wrap="word")
    note_text.insert("1.0", note["content"])
    note_text.pack(fill="both", expand=True, padx=20, pady=5)
 
    def saveChanges():
        title = title_entry.get().strip()
        content = note_text.get("1.0", tk.END).strip()
 
        if not title:
            messagebox.showwarning("Missing title", "Please enter a title for your note.", parent=window)
            return

        with open(datafile, "r") as file:
            data = json.load(file)
 
        data["notes"][index] = {"title": title, "content": content}
 
        with open(datafile, "w") as file:
            json.dump(data, file, indent=5)

        customnotes_list.delete(index)
        customnotes_list.insert(index, title)
        customnotes_list.selection_set(index)
        window.destroy()
 
    buttons = tk.Frame(window)
    buttons.pack(pady=10)
    tk.Button(buttons, text="Save", width=10, command=saveChanges).pack(side="left", padx=5)
    tk.Button(buttons, text="Cancel", width=10, command=window.destroy).pack(side="left", padx=5)
