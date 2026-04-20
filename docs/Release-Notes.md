# Release Notes

## v1.0.0

- Initial release of Screenshot Capture Utility
- Added system tray controls for start/stop and interval selection
- Implemented automatic screenshot capture with timestamped filenames
- Added persistent interval configuration using `config.json`
- Added logging support via `app.log`
- Built executable support via PyInstaller

## v1.0.1

- Fixed tray menu startup issue caused by missing `ScreenshotManager.get_status()`
- Added event logging and improved diagnostics
- Added custom interval dialog styling and centering
- Improved tray dialog thread handling to avoid crashes
