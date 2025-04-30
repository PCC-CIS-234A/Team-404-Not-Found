# Story 2 – Send Notification (Sprint 1 Part 2)

## Developer:
Sayan Tajul

## Overview:
The `sayan_send_notification` branch has the completed Send Notification feature for Team 404 - Team Not Found within Sprint 1 Part 2.

This feature uses a Tkinter GUI. It links to a distant SQL Server through PyODBC. The design uses N-Tier architecture. All GitHub conflicts received resolution. The folder structure received cleaning and proper committing.

---

## Features Implemented:

### ✅ Template Dropdown
- The program obtains stored templates from the SQL Server database.
- The program puts information into the Subject plus Message areas after a person makes a choice.

### ✅ Validation
- The subject requires a minimum of five characters.
- Messages require ten characters at a minimum.
- For incomplete fields, the system shows popups to notify users.

### ✅ File Attach & Remove
- Users pick files for notification attachments. 
- The attachments display in a listbox. 
- Before submission users can take out files.

### ✅ Review Confirmation
- A confirmation window displays the topic plus text to the user.
- It stops unintentional sends.

### ✅ Cancel Button
- The system empties the input boxes and removes any loaded documents.

### ✅ Database Connectivity
- PyODBC permits a remote SQL Server connection.
- If a notifications table is absent, the system constructs one.
- The system puts every validated notification into that table, attaching a time record.

### ✅ High-Quality GUI Layout
- DPI awareness permits clear pictures on screens with high resolution. 
- Window size adjusts to 1400x1000 plus appears at the center. 
- PCC brand colors are in operation. 
- The arrangement of buttons and inputs uses a design that is easy for the user.

---

## Folder & Architecture (N-Tier Structure):
The project is structured as follows:

project/ ├── gui/ │ ├── send_notification.py │ └── logviewermenu.py ├── logic/ │ └── template_logic.py ├── data/ │ └── notifications.db

yaml
Copy code

- **GUI Layer** → `gui/send_notification.py`
- **Logic Layer** → `logic/template_logic.py`
- **Data Layer** → `data/notifications.db`

---

## Git & Branch Workflow:
- Branch: `sayan_send_notification`
- All code cleaned, committed, and pushed to this branch
- Git conflicts resolved and force-pushed via rebase
- Project is now fully clean and ready for final Sprint 1 presentation

---

## Completed Milestones:
- [x] Connected to SQL Server database
- [x] Used GitHub to track version history and changes
- [x] Resolved Git rebase conflict and force-pushed clean changes
- [x] Committed to correct branch (sayan_send_notification)
- [x] Final code tested and verified
- [x] Final structure zipped and submitted to D2L

---

## Remaining:
- Final Sprint 1 in-class presentation (Zoom)
- Optional UI refinement if suggested by instructor

---

## Author:
Sayan Tajul  
CIS 234A – Team 404: Team Not Found

---

Thank you for reviewing my Sprint 1 Part 2 project!
