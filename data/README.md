# Sprint 2 – Send Notification (Part 2)

**Developer:** Sayan Tajul  
**Course:** CIS 234A  
**Team:** 404 – Team Not Found  
**Branch:** `sayan_send_notification`

---

## Overview

This feature finalizes the "Send Notification" system with fully integrated database-backed tags, rich text formatting, attachment handling, and refined PCC-themed UI. The system now delivers a professional notification experience using a Tkinter GUI, Gmail SMTP for email delivery, and SQL Server for subscriber and template management. 

---

## New Features & Enhancements (Part 2)

### PCC-Themed UI & Styling
- `theme.py` centralizes all visual styles: colors, fonts, and layout consistency
- Consistent white backgrounds, PCC Blue buttons, and Helvetica font styles
- Section headers like **Template** are now wrapped in styled `LabelFrame` boxes for improved readability

### Modular Architecture Finalized (N-Tier)
- **GUI Layer**: `send_notification.py`, `template_creator.py`
- **Logic Layer**: `notification_logic.py`, `template_logic.py`
- **Data Layer**: `database_access.py`
- **Styling Layer**: `theme.py` (new)
- **Testing Layer**: `test_notification_logic.py`

### Template Selection Improvements
- Dropdown menu for selecting templates is centered inside a `LabelFrame`
- “Template” caption is centered above the dropdown
- Auto-loads subject and message from DB when template is selected

### Rich Text Formatting
- Message box supports:
  - **Bold**, *Italic*, and _Underline_ via HTML-style tags
  - Inline color styling (e.g., `<span style="color:red">text</span>`)
- Buttons dynamically wrap selected message text in appropriate formatting

### Attachments Enhanced
- Files (PDF, PNG, JPG, DOCX, etc.) can be attached via file dialog
- Attachment list is displayed in a dedicated `Listbox`
- Remove button updates both the list and internal tracking state

### Email & Tag Logic
- Tags auto-populate from the `dbo.tags` table
- Tags like `{{first_name}}` and `{{date}}` are auto-replaced per recipient
- Active focus tracking ensures tags go where the user is typing (subject or message)

---

## Completed Deliverables (Part 2)

- [x] Added `theme.py` with centralized styling and PCC branding
- [x] Redesigned Template dropdown using `LabelFrame` for clarity
- [x] Rich-text options (bold, italic, underline, color) now functional
- [x] Attachments preview and removal finalized
- [x] Code cleaned and formatted according to **PEP 8**
- [x] High DPI support for Windows (`SetProcessDpiAwareness`)
- [x] Resolved path, import, and N-Tier separation issues

---

## Project Structure
project/
├── data/

│ ├── database_access.py # DB connection and SQL queries

│

├── gui/

│ ├── send_notification.py # GUI for sending notifications

│ ├── template_creator.py # GUI for building templates

│ └── config.ini # Secure Gmail credentials

│

├── logic/

│ ├── notification_logic.py # Email sending, tag processing

│ ├── tag_logic.py # Optional legacy tag popup (not used in final)

│ ├── template_logic.py # Template loading from SQL

│ ├── theme.py # Centralized fonts/colors for UI

│

├── tests/

│ └── test_notification_logic.py # Unit tests for email and logic


---

## Unit Testing Summary

- ✅ `validate_email()` regex validation
- ✅ Tag placeholder replacement with `process_tags()`
- ✅ File attachment simulation and name formatting
- ✅ Subject/message validation edge cases
- ✅ Mocked DB inserts and tag fetch using `unittest.mock`

---

## Security Notes

- `config.ini` securely stores `sender_email` and `app_password` for Gmail SMTP.
- File excluded from GitHub version control.
- In production, migrate credentials to environment variables or a secure vault.

---

##  Remaining Improvements (Post-Sprint)

- [ ] Add rich-text preview and photos before sending (HTML renderer or browser-based window)
- [ ] Export sent notification logs for review maybe.
- [ ] Finalize `template_creator.py` with DB insert functionality
- [ ] Consolidate tag logic (remove legacy popup system if unused)

---

## Author

**Sayan Tajul**  
_CIS 234A – Team 404: Team Not Found_

> Thank you for reviewing my Sprint 2 Part 2 submission. I look forward to your feedback!
