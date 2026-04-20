# Troubleshooting

## Common Issues

### Tray icon does not appear

- Ensure `pystray` is installed.
- Confirm you are running on Windows.
- Check `app.log` for startup errors.

### Screenshots are not saved

- Confirm the `screenshots/` folder exists.
- Verify write permissions in the project directory.
- Check `app.log` for errors from `ScreenshotManager`.

### Custom dialog crashes or fails to open

- The dialog runs in a dedicated thread to avoid pystray conflicts.
- If a crash occurs, inspect `app.log` for exception details.
- Ensure `tkinter` is available in your Python installation.

### Interval changes do not apply

- Custom values are saved to `config.json`.
- The tray menu refreshes after interval changes.
- If the interval is invalid, an error message is shown.

## Log File

- Application logs are written to `app.log`.
- Look for timestamps, log levels, and exception traces.
- Key logged events:
  - App startup and shutdown
  - Tray actions
  - Interval changes
  - Screenshot capture errors

## Debugging Steps

1. Run the app from a terminal:
   ```bash
   python main.py
   ```
2. Confirm the tray icon appears.
3. Open `app.log` for any error messages.
4. Verify `config.json` contains the configured interval.
5. If needed, rebuild using PyInstaller:
   ```bash
   .venv\Scripts\pyinstaller main.spec
   ```
