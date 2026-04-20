# Architecture

## Project Structure

```
screen/
├── src/
│   ├── config.py              # Configuration and file paths
│   ├── logger.py              # Logging configuration
│   ├── screenshot_manager.py  # Screenshot capture engine
│   └── tray_manager.py        # System tray UI and dialog logic
├── main.py                    # Application launcher
├── main.spec                  # PyInstaller build spec
├── requirements.txt           # Dependencies
├── screenshots/               # Saved screenshots
└── docs/                      # Wiki documentation
```

## Component Overview

### `main.py`

- Initializes logging
- Creates `ScreenshotManager`
- Creates and starts `TrayManager`
- Keeps the process alive while the tray icon is active

### `src/config.py`

- Calculates `BASE_DIR` for script vs executable usage
- Defines screenshot settings and storage paths
- Loads and saves interval settings from `config.json`

### `src/logger.py`

- Configures a rotating log to `app.log`
- Uses `logging` with timestamps and log levels
- Limits file size to 5 MB with backups

### `src/screenshot_manager.py`

- Manages background screenshot capture in a daemon thread
- Handles start/stop and interval updates
- Saves screenshots using Pillow
- Provides status metadata for tray display

### `src/tray_manager.py`

- Builds the system tray icon and menu using pystray
- Handles tray actions: start, stop, open folder, change interval
- Displays a custom dialog for interval input
- Logs tray events and errors

## Runtime Flow

1. `main.py` starts and initializes `ScreenshotManager`
2. `TrayManager` creates a tray icon and menu
3. The app runs in the background while `tray_manager.app_running` is `True`
4. User actions from the tray invoke screenshot management or configuration changes
5. `app.log` captures events and exception traces

## Threading Model

- `ScreenshotManager` runs screenshot capture in a separate daemon thread
- The custom interval dialog is launched in its own thread to avoid conflicts with pystray

## Build Process

- Uses `PyInstaller` and `main.spec`
- Produces a single executable: `dist/ScreenshotCapture.exe`
- Includes source dependencies and runtime hooks for Tkinter and pystray
