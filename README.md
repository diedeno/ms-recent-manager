[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)

# ms-recent-manager

## Introduction
The MuseScore Recent Files Manager is a user-friendly application designed to help you manage the list of recent files displayed in MuseScore. With this tool, you can:

- View the list of recent scores.
- Remove specific scores from the list (without deleting the actual files).
- Search for specific scores by filename or path.
- Sort the list by filename or file path.
- Backup the recent files list before making changes.

This application does not modify or delete the actual score files; it only updates the recent files list used by MuseScore.

---

## Getting Started

### Launching the Application

    Save the script as ms-recent-manager.py or ms-recent-manager.pyw (on Windows, use .pyw to suppress the terminal).
    Run the script:
        Windows: Double-click the .pyw file.
        macOS/Linux: Run python3 musicxml_merger_gui.py in the terminal.


---

## Features

### Viewing Recent Files
The main table displays the following columns:
1. **Filename**: The name of the score file.
2. **Path**: The full path to the score file on your system.
3. **Remove**: A button to remove the file from the recent list.

### Removing a File from the Recent List
1. Locate the file you want to remove in the table.
2. Click the "X" button in the **Remove** column for that file.
3. Confirm the removal in the dialog box that appears. The file will be removed from the list.

> **Note:** Removing a file only updates the recent files list; it does not delete the actual file from your computer.

### Searching for Files
1. Enter a search term in the **Search** box at the top of the window.
   - You can search by filename or path.
   - The table will update dynamically to show only the files that match your query.
2. To clear the search, erase the text in the search box. The full list will reappear.

### Sorting Files
1. Click the **Filename** or **Path** column headers to sort the list alphabetically.
2. Click the same header again to toggle between ascending and descending order.

### Backing Up the Recent Files List
1. Click the **Backup** button at the bottom of the window.
2. The application will create a backup of the recent files JSON file in the same directory, with a timestamp appended to its name.

### Saving Changes
1. After making changes, click the **Save** button at the bottom of the window.
2. The changes will be saved to the recent files JSON file used by MuseScore.
3. MuseScore will reflect the updated list the next time it is launched.

### Exiting the Application
1. Click the **Exit** button at the bottom of the window to close the application.

---

## Safety Information
- **Non-Destructive Changes**: This application does not delete or modify actual score files on your computer. Only the recent files list is updated.
- **Backup Recommended**: Always use the **Backup** feature before making significant changes to the list, to ensure you can restore the original state if needed.

---

## Troubleshooting

### Problem: "Remove" button doesn't work.
- Ensure you are clicking the X sign in the **Remove** column.
- Verify that the recent files JSON file is accessible and not locked by another program.

### Problem: Search doesn't filter results.
- Ensure you are entering the correct search terms (case-insensitive).
- Clear the search box to reset the list and try again.

### Problem: Changes are not reflected in MuseScore.
- Ensure you click **Save** after making changes.
- Restart MuseScore to reload the recent files list.

---

