<!-- Workspace-specific instructions for the Screenshot Capture Utility project -->

## Project Overview

This is a Python-based background screenshot capture utility that:
- Captures screenshots every 10 seconds
- Runs silently with system tray control
- Allows users to start/stop capture anytime
- Saves timestamped screenshots to a local folder

## Key Technologies

- **Language**: Python 3.7+
- **Screenshot Capture**: PIL/Pillow
- **System Tray**: pystray
- **Threading**: Python threading module

## Project Structure

- `src/config.py` - Global configuration and settings
- `src/screenshot_manager.py` - Core screenshot capture logic (threaded)
- `src/tray_manager.py` - System tray icon and menu management  
- `main.py` - Application entry point
- `screenshots/` - Output directory for captured images

## Running the Project

1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `python main.py`
3. Use system tray icon to control capture

## Development Guidelines

- Keep screenshot capture in a separate thread to avoid blocking UI
- All file operations should use absolute paths from config.py
- Error handling should log but not crash the application
- System tray menu should reflect current capture state

## Building for Production

Use PyInstaller to create a standalone .exe:
```
pyinstaller --onefile --windowed main.py
```

The executable will run in the background on Windows startup.
