# Screenshot Capture Utility

A lightweight background utility that automatically captures screenshots at regular intervals (default: every 10 seconds). The application runs with a system tray icon for easy control and management.

## Features

- **Background Execution**: Runs silently in the background
- **Automatic Capture**: Takes screenshots at configurable intervals (default: 10 seconds)
- **System Tray Control**: Access start/stop controls from the system tray
- **Screenshot Management**: View screenshot count and open screenshots folder directly
- **Easy Start/Stop**: Click tray icon to start or stop capture
- **Timestamped Files**: Screenshots are automatically named with timestamps

## Project Structure

```
screen/
├── src/
│   ├── config.py              # Configuration settings
│   ├── screenshot_manager.py  # Screenshot capture logic
│   └── tray_manager.py        # System tray interface
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── screenshots/               # Output directory for captured images
└── README.md                  # This file
```

## Requirements

- Python 3.7+
- Windows OS (for system tray support)
- PIL/Pillow (for screenshot capture)
- pystray (for system tray icon)

## Installation

1. Clone or download the project
2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

```bash
python main.py
```

The application will:
1. Start with a system tray icon
2. Display a camera-like icon in the system tray
3. Right-click the tray icon to see options

### System Tray Menu Options

- **Start Capture**: Start automatic screenshot capture
- **Stop Capture**: Stop screenshot capture
- **Interval: Xs**: Change the screenshot capture interval (5s, 10s, 30s, 60s, or Custom)
- **Screenshots (count)**: Shows number of captured screenshots
- **Open Screenshots Folder**: Opens the screenshots directory in Windows Explorer
- **Quit**: Exit the application

## Screenshot Location

When you run the executable (`ScreenshotCapture.exe`), screenshots are automatically saved in a `screenshots` folder located in the **same directory as the executable**.

For example:
- If you place `ScreenshotCapture.exe` in `C:\MyTools\`, screenshots will be saved in `C:\MyTools\screenshots\`
- If you place it on your Desktop, screenshots will be saved in `Desktop\screenshots\`

The application will automatically create the `screenshots` folder if it doesn't exist.

## Changing Screenshot Interval

You can change the screenshot capture interval through the system tray menu:

1. Right-click the tray icon
2. Hover over "Interval: Xs" 
3. Choose from preset intervals (5s, 10s, 30s, 60s) or select "Custom..." to enter your own interval
4. For custom intervals, a dialog will open where you can:
   - Type the desired interval in seconds (minimum 1)
   - Press Enter or click OK to confirm
   - Press Escape or click Cancel to close without changes
   - The text field is fully editable with the current value pre-selected
5. The new interval takes effect immediately and is saved for future sessions

**Note:** The minimum interval is 1 second. Invalid input will show an error message. The dialog handles focus conflicts gracefully in system tray environments.

## Configuration

The application saves your interval preference in a `config.json` file in the same directory as the executable.

Edit [src/config.py](src/config.py) to customize:

- `SCREENSHOT_INTERVAL`: Time between screenshots in seconds (default: 10, configurable via tray menu)
- `SCREENSHOT_DIR`: Directory where screenshots are saved (relative to executable location, default: ./screenshots)
- `SCREENSHOT_FORMAT`: Image format (default: png)
- `SCREENSHOT_NAMING`: Filename pattern (default: screenshot_{timestamp}.png)

## Building an Executable

To create a standalone .exe file for Windows:

1. Install PyInstaller:
   ```
   pip install pyinstaller
   ```

2. Build the executable:
   ```
   pyinstaller --onefile --windowed main.py
   ```

3. Or use the provided spec file (recommended):
   ```
   pyinstaller main.spec
   ```

4. The executable will be in the `dist/` folder as `ScreenshotCapture.exe`

**Note:** The spec file includes the `src` directory in the path to ensure proper module imports in the executable.

## Troubleshooting

- **Tray icon not appearing**: Ensure pystray is installed and you're using Windows
- **Screenshots not saving**: Check that the `screenshots/` directory has write permissions
- **Application errors or startup failures**: Review `app.log` in the application directory for detailed event and exception traces
- **PIL error**: Make sure Pillow is installed: `pip install pillow`

## Version

- v1.0.0 - Initial release

## License

MIT License
