# CIS 234A - Food Insecurity Notification System  
**Team 404 Not Found**  
**Sprint 2 – Send Notification Module by Sayan Tajul**

## Overview

This project is part of a team-based software development assignment for CIS 234A at Portland Community College. The system is designed to send personalized email notifications to students regarding food pantry updates and closures. My feature for Sprint 2 focuses on building a robust and user-friendly notification sender interface that supports email templates, dynamic tags, HTML formatting, and file attachments.

---

## Features Completed in Sprint 2

- **HTML Rich Text Formatting:**
  - Buttons for Bold, Italic, Underline
  - Dropdown for applying text color (e.g., red, blue, green, etc.)
- **Tag Insertion:**
  - Tags such as `{{name}}`, `{{date}}`, and `{{campus_location}}` can be inserted and replaced dynamically
  - Tag values are retrieved from the database or prompted from the user
- **Template Integration:**
  - Predefined templates can be selected and auto-fill the subject and message fields
- **File Attachments:**
  - Users can attach `.pdf`, `.jpg`, and `.png` files
  - Attachments are validated and recorded in the database
- **Database Logging:**
  - Notifications are logged with subject, message, sender, and attachment details
- **N-Tier Architecture:**
  - Code is separated into `gui/`, `logic/`, and `data/` layers for maintainability
- **Unit Testing:**
  - Unit test class included with test cases for validation, tag replacement, and database mocking

---

## Project Structure

gui/

├── send_notification.py # Main GUI window for composing and sending emails

├── template_creator.py # GUI for creating/editing templates

├── config.ini # Stores email sender credentials

logic/

├── notification_logic.py # Handles sending emails, formatting, and validation

├── tag_logic.py # Handles tag replacement

├── template_logic.py # Fetches templates from database

data/

├── database_access.py # Database connection and queries

├── notifications.db # Local SQLite DB (for initial testing)

tests/

├── test_notification_logic.py # Unit test class for backend logic

README.md # Project overview and instructions


---

## How It Works

1. The user launches `send_notification.py`.
2. They select a template or write their own subject and message.
3. Tags can be inserted using the dropdown.
4. The user can format parts of the message using formatting buttons.
5. File attachments can be added if needed.
6. On clicking "Send Notification", the system:
   - Validates the message
   - Replaces tags with actual values
   - Sends the HTML-formatted email to all subscribers
   - Logs the message and attachments in the database

---

## Getting Started

### Requirements

- Python 3.10+
- `tkinter` (included with standard Python)
- Microsoft SQL Server or SQLite (for local testing)
- SMTP email credentials stored in `config.ini`

### How to Run

```bash
cd gui
python send_notification.py
Sprint 2 Notes
This version reflects all improvements made during Sprint 2. It replaces older logic with a fully functional HTML message composer, including a tag-driven dynamic messaging engine and improved modular code architecture. The UI is designed for clarity and follows the PCC color scheme.

Let me know if you'd like me to tailor it further (e.g., for the master branch instead of the feature branch), or if you're ready to copy this into your GitHub `README.md`.

Author
Sayan Tajul – Spring 2025
PCC CIS 234A – Team 404 Not Found


