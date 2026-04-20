# Getting Started

## Overview

Screenshot Capture Utility is a lightweight desktop utility that runs in the background and automatically captures screenshots at configurable intervals. It is controlled through a system tray icon and saves all screenshots to a local folder.

## Requirements

- Python 3.7+
- Windows OS (primary target)
- `pillow`
- `pystray`

## Installation

1. Clone or download the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

Run the application with:

```bash
python main.py
```

The app will launch a tray icon and stay running in the background.

## Configuration

- `src/config.py` contains default settings.
- `config.json` stores the saved interval.
- Screenshots are saved in the `screenshots/` directory.
