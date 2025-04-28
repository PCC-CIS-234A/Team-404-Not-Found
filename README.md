# Story 2 – Send Notification (Sprint 1 Part 2)

## Developer:
Sayan Tajul

## Description:
This branch contains the updated Sprint 1 Part 2 implementation for the Send Notification feature for Team 404 – Team Not Found.

## Features Implemented:
- **Template Dropdown:**  
  Users can select a prewritten template from a dropdown menu. Template subject and message fields auto-populate based on the selected template. Templates are pulled dynamically from the database.

- **Validation:**  
  Input validation added to ensure that:
  - Subject must be at least 5 characters.
  - Message must be at least 10 characters.
  - Warning popups notify users if validation fails.

- **Attach/Remove Files:**  
  Users can attach files related to their notification. Selected files are visually shown in a listbox. Users can also select and remove any attached file before sending.

- **Review Before Sending:**  
  A review confirmation popup displays the subject and message before the notification is finalized and saved to the database.

- **Cancel Button:**  
  Clears the subject and message fields instantly if needed.

- **Database Connectivity:**  
  Program connects to a remote SQL Server database using PyODBC. Notifications are stored into the 'notifications' table if sending is confirmed.

- **GUI Updates for Professional Layout:**  
  - High DPI scaling enabled for better visuals on high-resolution monitors.
  - Window size and fonts adjusted for better user experience.
  - Organized button layout following a user-friendly flow.

## Architecture:
- Follows **N-Tier Architecture**:
  - **GUI Layer:** Tkinter interface (`send_notification.py`)
  - **Logic Layer:** Template logic for database communication (`template_logic.py`)
  - **Data Layer:** SQL Server database connection and operations.

## Branch Information:
- **Branch Name:** `Sayan_Send_Notification`
- Based on story 2 assignment for Sprint 1.
- This branch is over 90% completed.
- Code compiles, runs without errors, and fully connects to the database.

## Remaining Tasks:
- Prepare and practice presentation for final Sprint 1 review.
- Minor UI polish if needed after feedback.

---

# Thank you for reviewing this Sprint 1 Part 2 update!
