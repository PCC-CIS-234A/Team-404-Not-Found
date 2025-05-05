# CIS 234A Food Insecurity Notification System

## Team 404 - Team Not Found

### Sprint 1 Final Submission

#### Feature: Send Notification with Templates, Validation, and Attachments

## Developer: Sayan Tajul

### For the final phase of Sprint 1, I developed and refined the Send Notification feature. This includes:

### Template Integration:
- Created a dropdown menu allowing the user to select predefined notification templates.
- Implemented dynamic loading of template subject and message content from our SQL database upon selection.

### Input Validation:
- Added validation rules to ensure notifications have a meaningful subject (at least 5 characters) and message body (at least 10 characters).
- Provided user-friendly warning messages if input validation fails.

### Attachments:
- Integrated functionality for users to add multiple file attachments to notifications.
- Implemented a graphical interface (GUI) showing attached files clearly.
- Developed functionality allowing easy addition and removal of file attachments through intuitive buttons.

### Email Sending (SMTP):
- Configured and tested the Gmail SMTP service for secure email sending.
- Successfully implemented email notifications with attachments to subscribers.

### Notification Logging:
- Set up and tested the logging of sent notifications into the database.
- Ensured accurate records of notification subjects, messages, sender details, timestamps, and subscriber counts.

### Enhanced User Interface:
- Refined the GUI to improve clarity and usability.
- Aligned the layout for better aesthetics, adhering to the team's chosen PCC color scheme.

### GitHub Integration:
- Corrected branch conflicts and pushed a clean, final version of the code to the branch `sayan_send_notification`.
- Ensured that previous unwanted commits were overwritten cleanly with the final correct version.

### Final Thoughts:
- This sprint improved the functionality and robustness of our notification system significantly, providing a user-friendly tool for managing and sending critical communications effectively. 
- The next sprint will likely enhance logging details, user management, and introduce further performance improvements based on testing feedback.

Thank you,

**Sayan Tajul**  
*CIS 234A Team 404 - Team Not Found*
