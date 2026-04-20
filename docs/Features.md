# Features

## Core Features

- **Background Execution**
  - Runs silently in the system tray
  - Does not interrupt the user

- **Automatic Screenshot Capture**
  - Captures screenshots at a configurable interval
  - Default interval is 10 seconds
  - Saved as PNG files with timestamped names

- **System Tray Interface**
  - Start and stop capture from tray menu
  - Open screenshot folder directly
  - View screenshot count
  - Change interval using preset and custom options

- **Custom Interval Support**
  - Custom dialog for interval entry
  - Input validation with user-friendly error messages
  - Changes persist through `config.json`

- **Logging and Diagnostics**
  - Writes events to `app.log`
  - Logs startup, shutdown, errors, interval changes, and tray actions

## User Experience Improvements

- Modern, centered custom dialog
- Always-on-top dialog behavior
- Styled input and buttons for better usability
- Tray menu updates reflect current capture state
