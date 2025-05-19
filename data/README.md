# Sprint 2 – Send Notification (Part 1)

**Developer:** Sayan Tajul  
**Course:** CIS 234A  
**Team:** 404 – Team Not Found  
**Branch:** `sayan_send_notification`

---

## Overview

This feature delivers a complete "Send Notification" experience with a refined user interface, integrated templates, rich tag insertion, and full N-Tier architecture separation. The system enables users to dynamically build email notifications with placeholders, preview them, attach files, and deliver them using Gmail SMTP — all with validation and confirmation steps.

---

## New Features & Highlights

### Dynamic Tag Support (From DB)
- All tags (`{{tag_name}}`) now load from the SQL `dbo.tags` table.
- Tags can be inserted directly into both the subject and message at the **exact cursor position**.
- Dropdown reflects database values like `{Time}`, `{Location}`, etc.
- Tags are inserted in `{tag}` format for consistency and easy templating.

### Focus Tracking
- The active field (subject or message) is tracked with `active_widget`.
- Tag inserts behave intuitively based on cursor focus, improving UX.

### Updated N-Tier Architecture
- GUI: `send_notification.py`, `template_creator.py` (Tkinter-based)
- Logic: `notification_logic.py`, `template_logic.py`, `tag_logic.py` *(optional)*
- Data: `database_access.py`
- Tests: `test_notification_logic.py`

### Email Features
- Uses secure Gmail SMTP via `config.ini`
- Sends HTML emails with formatting (line breaks, bold, etc.)
- File attachment support (PDF, PNG, JPG, etc.)
- Placeholder tags like `{{first_name}}`, `{{date}}` are auto-replaced per recipient

### Validation
- Verifies subject/message are not empty and meet length requirements
- Ensures email format validity
- Prompts for confirmation before sending

### Unit Testing (5+ Cases)
- `validate_email()` testing
- Tag replacement test with `process_tags()`
- File attachment type test
- DB insert mocked with `unittest.mock`
- Missing field error handling

---

## Project Structure

project/
├── data/
│ ├── database_access.py # DB connection + fetch/insert logic
│ ├── notifications.db # SQL Server (or SQLite backup)
│ └── README.md # (optional) DB documentation
│
├── gui/
│ ├── send_notification.py # Notification sender GUI
│ ├── template_creator.py # Create new templates (with tag insert)
│ └── config.ini # Securely stores Gmail credentials
│
├── logic/
│ ├── notification_logic.py # Email sending, tag processing
│ ├── tag_logic.py # Popup-based tag UI (optional legacy)
│ └── template_logic.py # DB template loading
│
├── tests/
│ └── test_notification_logic.py # Unit tests with mocks & validation


- **GUI Layer**: Tkinter UI logic
- **Logic Layer**: Business rules, email sending, tag formatting
- **Data Layer**: All SQL operations, queries, and connection
- **Tests Layer**: Ensures correctness of logic and behaviors

---

## Sprint 2 - Completed Deliverables

- [x] Refactored into full N-Tier architecture
- [x] Tag dropdown populated from `dbo.tags`
- [x] Cursor-aware tag insertion in both Entry and Text widgets
- [x] Tag logic fallback (popup UI kept in `tag_logic.py`)
- [x] Subject/message validation + confirmation dialogs
- [x] HTML email support with Gmail SMTP + attachments
- [x] All tag logic and dynamic tag replacement in subject/message
- [x] Unit tests with `unittest` and `mock`
- [x] Final code follows **PEP 8** standards and is cleanly modularized

---

## Remaining Tasks

- [ ] Save template logic with full DB support in `template_creator.py`
- [ ] Polish edge-case validation (e.g., empty tag insertions)
- [ ] Prepare for Sprint 2 part 2.
- [ ] Merge teammate features into main (e.g., login/auth, logs)

---

## Security Notes

- App password and sender email are stored securely in `config.ini` (excluded from GitHub).
- DB credentials should be further protected using `.env` or vault solution in production.

---

## 🙋‍♂️ Author:
**Sayan Tajul**  
_CIS 234A – Team 404: Team Not Found_

> Thank you for reviewing my Sprint 2 implementation. Looking forward to your feedback!
