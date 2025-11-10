#!/usr/bin/python3

import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


"""
MuseScore recent files manager
Copyright (c) 2025 Diego Denolf (graffesmusic)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""


# Application Info
VERSION = "1.1"
LAST_MODIFIED = "20251110"
LICENSE = "GPLv3"

# Determine JSON File Path Based on OS
def get_json_file_path():
    if os.name == 'nt':  # Windows
        return os.path.expandvars(r'%localappdata%\\MuseScore\\MuseScore4\\recent_files.json')
    elif os.name == 'posix':
        if "darwin" in os.sys.platform:  # macOS
            return os.path.expanduser('~/Library/Application Support/MuseScore/MuseScore4/recent_files.json')
        else:  # Linux
            return os.path.expanduser('~/.local/share/MuseScore/MuseScore4/recent_files.json')
    else:
        raise Exception("Unsupported OS")

json_file_path = get_json_file_path()

# Load JSON Data
if os.path.exists(json_file_path):
    with open(json_file_path, "r") as file:
        data = json.load(file)
else:
    data = []

# Prepare filtered_data as a list of dictionaries
filtered_data = [
    {
        "path": item["path"] if isinstance(item, dict) else item,  # Use the path from dict or the string itself
        "filename": item["displayName"] if isinstance(item, dict) else os.path.basename(item),  # Use displayName for cloud scores
        "original_index": idx
    }
    for idx, item in enumerate(data)
]

# Ensure filtered_data always stays in sync with data
def rebuild_filtered_data():
    """
    Rebuilds the `filtered_data` list based on the current `data`.
    """
    global filtered_data
    filtered_data = [
        {
            "path": item["path"] if isinstance(item, dict) else item,
            "filename": item["displayName"] if isinstance(item, dict) else os.path.basename(item),
            "original_index": idx,
        }
        for idx, item in enumerate(data)
    ]

# Define how to display rows
def get_row_values(rf_data):
    return rf_data["filename"], rf_data["path"], "❌"

def save_json():
    """
    Save the updated recent files list back to the JSON file, preserving its original structure.
    """
    with open(json_file_path, "w") as file:
        # Write the original `data` list directly to preserve its structure
        json.dump(data, file, indent=2)
    messagebox.showinfo("Save", "Changes have been saved.")


# Tkinter App Setup
root = tk.Tk()
root.title("MuseScore recent files manager")
root.geometry("900x600")

# Refresh Treeview with Updated Data
def refresh_treeview():
    """
    Refresh the Treeview widget with the current filtered_data.
    """
    for row in tree.get_children():
        tree.delete(row)

    for index, rf_data in enumerate(filtered_data):
        values = get_row_values(rf_data)
        tree.insert("", "end", iid=index, values=values)

# Handle Delete Click
def handle_delete_click(event):
    """
    Handles clicks on the Treeview, specifically the 'Delete' column.
    """
    # Identify the row and column that were clicked
    item_id = tree.identify_row(event.y)
    column_id = tree.identify_column(event.x)

    # Ensure we are clicking on the "Delete" column (typically the third column: "#3")
    if item_id and column_id == "#3":  # "#3" is the 'Delete' column
        delete_entry(int(item_id))  # Call delete_entry with the row index

# Define the delete_entry function
def delete_entry(index):
    """
    Deletes the entry at the given index after confirmation.
    """
    filename = filtered_data[index]["filename"]  # Extract the filename
    if messagebox.askyesno("Remove", f"Are you sure you want to remove '{filename}' from the recent files list?"):
        # Get the original entry from `data` and remove it
        original_index = filtered_data[index]["original_index"]
        del data[original_index]  # Remove from the original `data` list

        # Rebuild filtered_data to ensure indices are correct
        rebuild_filtered_data()

        # Refresh the Treeview
        refresh_treeview()


# Search Functionality
def search_treeview(query):
    """
    Filters the Treeview based on the search query.
    """
    global filtered_data
    query = query.lower()

    # Filter based on the query matching the path or filename
    filtered_data = [
        {
            "path": item,
            "filename": os.path.basename(item),
            "original_index": idx,
        }
        for idx, item in enumerate(data)
        if query in item.lower() or query in os.path.basename(item).lower()
    ]

    refresh_treeview()


# Sorting Functionality
sort_order = {}

def sort_treeview(column):
    global filtered_data
    reverse = sort_order.get(column, False)  # Get current sort order, default to False
    sort_order[column] = not reverse         # Toggle sort order for next use

    # Map column names to their sorting logic
    column_map = {
        "Filename": lambda x: x.get("filename", ""),
        "Path": lambda x: x.get("path", ""),
    }

    # Sort filtered_data based on the selected column
    if column in column_map:
        filtered_data.sort(key=column_map[column], reverse=reverse)
        refresh_treeview()
    else:
        print(f"Unknown column: {column}")  # Debugging fallback

# Backup Functionality
def backup_json():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_path = f"{json_file_path}_{timestamp}.bak"
    shutil.copy(json_file_path, backup_path)
    messagebox.showinfo("Backup", f"Backup created at {backup_path}")


def show_about():
        about = tk.Toplevel(root)
        about.title("About MuseScore Recentfiles editor")
        about.geometry("400x300")
        about.resizable(False, False)

        tk.Label(about, text="MuseScore Recentfiles editor", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(about, text=f"Version {VERSION} |  Last Modified: {LAST_MODIFIED}", font=("Arial", 11)).pack(pady=2)
        tk.Label(about, text="© 2025 Diego Denolf", font=("Arial", 10)).pack(pady=2)
        
        msg = (
            "Manage the list of recent files displayed in MuseScore.\n" 
            "This application does not modify or delete the actual score files; it only updates the recent files list used by MuseScore.\n\n"
            
            "Licensed under the GNU GPL v3."
        )
        tk.Label(about, text=msg, wraplength=360, justify="left").pack(padx=15, pady=10)

        tk.Button(about, text="Close", command=about.destroy).pack(pady=5)

# Create GUI Components
frame = ttk.Frame(root)
frame.pack(fill="both", expand=True, padx=10, pady=10)

tk.Label(root, text="Scores are only removed from the recent files list and are not deleted from the filesystem.", fg = "green", font = "Helvetica").pack()

tree = ttk.Treeview(frame, columns=("Filename", "Path", "Remove"), show="headings")
tree.heading("Filename", text="Filename", command=lambda: sort_treeview("Filename"))
tree.heading("Path", text="Path", command=lambda: sort_treeview("Path"))
tree.heading("Remove", text="Remove")

tree.column("Filename", width=200)
tree.column("Path", width=500)
tree.column("Remove", width=50, anchor="center")

tree.bind("<Button-1>", handle_delete_click)

tree.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Search Box
search_frame = ttk.Frame(root)
search_frame.pack(fill="x", pady=5)

search_label = ttk.Label(search_frame, text="Search:")
search_label.pack(side="left", padx=5)

search_entry = ttk.Entry(search_frame)
search_entry.pack(side="left", fill="x", expand=True, padx=5)

search_entry.bind("<KeyRelease>", lambda _: search_treeview(search_entry.get()))

# Button Panel
button_frame = ttk.Frame(root)
button_frame.pack(fill="x", pady=5)

backup_button = ttk.Button(button_frame, text="Backup", command=backup_json)
backup_button.pack(side="left", padx=5)

save_button = ttk.Button(button_frame, text="Save", command=save_json)
save_button.pack(side="left", padx=5)

exit_button = ttk.Button(button_frame, text="Exit", command=root.quit)
exit_button.pack(side="right", padx=5)

about_button = ttk.Button(button_frame, text="About", command=show_about)
about_button.pack(side="right", padx=5)

# Initialize Treeview
refresh_treeview()
root.mainloop()

