# Story 2 – Send Notification (Sprint 1 Final)
## Developer:
Sayan Tajul

## Overview:
The `sayan_send_notification` branch is updated for the final submission of Sprint 1. This update enhances the Send Notification functionality, providing robust validation, clearer GUI interactions, improved database logging, and seamless template integration.
---
## New Updates & Enhancements:
### Improved Database Integration
- Notifications accurately log subscriber counts.
- Dynamic retrieval of subscriber emails from SQL Server for accurate tracking.
### Enhanced Logging & Debugging
Added detailed debug statements for:
- Subscribers list
- Subscriber counts
- Sender verification
### Template Loading Enhancement
- Fixed dynamic loading of subject and message fields.
- Improved error handling when fetching templates.
### GUI Enhancements
- GUI dimensions adjusted (1600x1000) for improved user interaction.
- File attachment buttons aligned clearly.
- Listbox readability enhanced for attached files.
### Email Sending via Gmail SMTP
- Enhanced SMTP email sending with better debugging and error handling.
### Confirmation & Error Handling
- Confirmation dialog displays notification content clearly before sending.
- Robust validation to prevent incomplete or accidental submissions.
### Clear Cancel and Reset Functionality
- Cancel button effectively resets all inputs and attachments.
---
## Updated Folder & Architecture (N-Tier Structure):
project/
├── gui/
│ ├── send_notification.py
│ └── logviewermenu.py
├── logic/
│ └── template_logic.py
├── data/
│ └── notifications.db

- **GUI Layer:** `gui/send_notification.py`
- **Logic Layer:** `logic/template_logic.py`
- **Data Layer:** `data/notifications.db`
---
## Git & Branch Workflow:
- **Branch:** `sayan_send_notification`
- Latest changes committed and pushed.
- Repository cleaned and structured clearly.
---
## Completed Updates:
- [x] Accurate subscriber counting integration
- [x] Enhanced logging and debugging
- [x] Improved email functionality via SMTP
- [x] Clear GUI layout and interactions
- [x] Comprehensive testing and validation
---
## Remaining Tasks:
- Sprint 1 final Zoom presentation
- Any additional professor-recommended adjustments
---
## Author:
**Sayan Tajul**  
*CIS 234A – Team 404: Team Not Found*
Thank you for reviewing my updated Sprint 1 project!
