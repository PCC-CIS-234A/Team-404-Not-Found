# Story 2 – Send Notification (Sprint 2 Final)
## Developer:
Sayan Tajul

## Overview:
This is the submission update for Sprint 2 Part 1 of the `sayan_send_notification` feature branch. The Send Notification functionality is now fully enhanced with dynamic tag support, user-friendly tag prompts, email formatting improvements, and UI polish. This version supports dynamic message customization using template tags that are auto-detected and filled in by the user via a popup interface.

---

## 🔧 New Features & Enhancements:

### Dynamic Tag Recognition and Prompting
- Automatically detects all `{{tag_name}}` placeholders in the subject and message.
- Opens a centralized popup window prompting the user to fill in missing tag values.
- Uses **user-friendly descriptions** instead of raw tag names (e.g., `{{event_name}}` → _"What is the name of the event?"_).

### Improved GUI Behavior
- Tag input popup window is **centered on the screen** and fixed at a readable size (500x400).
- Duplicate popups were eliminated with a clean and consistent design.
- Readable layout for subject/message, file attachments, and action buttons.

### Template Integration with Error Handling
- Dynamic loading of templates populates both subject and message fields.
- Error handling for database/template issues is displayed via message boxes.

### Enhanced Email Sending Logic
- Emails sent via Gmail SMTP with support for:
  - Dynamic content based on user input
  - File attachments
  - Clean formatting and tag replacement

### Robust Input Validation & Confirmation
- Validates subject and message length before sending.
- Confirms final message with user before proceeding.

### Debug Logs for Developers
- Helpful print/debug messages for:
  - Subscriber data
  - Sender verification
  - Database logging and attachments

---

## Folder Structure (N-Tier Architecture):
```
project/
├── .venv/                              # Virtual environment (hidden in version control)
│
├── data/
│   ├── database_access.py              # Database connection and access logic
│   ├── notifications.db                # SQLite or SQL Server database file
│   └── README.md                       # Documentation related to the data layer
│
├── gui/
│   ├── config.ini                      # Email credentials stored securely
│   ├── send_notification.py           # Main GUI application for sending notifications
│   └── template_creator.py            # Optional: Tool for creating new templates
│
├── logic/
│   ├── notification_logic.py          # Email-sending logic (SMTP, attachments, etc.)
│   ├── tag_logic.py                   # Handles dynamic tag prompting and mapping
│   └── template_logic.py              # Template retrieval and processing logic
│
├── External Libraries/                # PyCharm's reference folder (auto-managed)
└── Scratches and Consoles/            # PyCharm's temp/test area (auto-managed)

```

- **GUI Layer:** Handles user interface and Tkinter components.
- **Logic Layer:** Encapsulates business logic, tag processing, and email sending.
- **Data Layer:** Handles database connectivity and queries (SQL Server + local backup).

---

## Completed in Sprint 2 part 1:
- [x] Popup UI for tag entry with centralized window
- [x] Friendly prompt labels for over 12+ common tag types
- [x] Tag auto-detection and replacement
- [x] Popup validation and cleanup
- [x] Template handling separated into `template_logic.py`
- [x] SMTP email logic handled cleanly with attachments
- [x] N-Tier separation and refactoring complete

---

## Remaining Tasks:
- Polish any UI elements based on final professor feedback
- Document backup plan if SMTP fails
- Sprint 2 Zoom walkthrough presentation

---

## Author:
**Sayan Tajul**  
*CIS 234A – Team 404: Team Not Found*

Thank you for reviewing my Sprint 2 Part 1 implementation! Screenshots and demos are available upon request.
