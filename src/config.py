"""Configuration settings for Screenshot Capture Utility"""
import os
import sys
import json
from pathlib import Path

# Base directory - handle both development and executable contexts
if getattr(sys, 'frozen', False):
    # Running as executable
    BASE_DIR = Path(sys.executable).parent
else:
    # Running as script
    BASE_DIR = Path(__file__).parent.parent

# Screenshot settings
SCREENSHOT_INTERVAL = 10  # seconds (default)
SCREENSHOT_DIR = BASE_DIR / "screenshots"
SCREENSHOT_FORMAT = "png"
SCREENSHOT_NAMING = "screenshot_{timestamp}.png"  # timestamp will be replaced

# Configuration file
CONFIG_FILE = BASE_DIR / "config.json"

# Ensure screenshot directory exists
SCREENSHOT_DIR.mkdir(exist_ok=True)


def load_config():
    """Load configuration from file"""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return config.get('interval', SCREENSHOT_INTERVAL)
        except Exception as e:
            print(f"Error loading config: {e}")
    return SCREENSHOT_INTERVAL


def save_config(interval):
    """Save configuration to file"""
    try:
        config = {'interval': interval}
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"Error saving config: {e}")


def get_current_interval():
    """Get the current screenshot interval"""
    return load_config()


def set_interval(interval):
    """Set the screenshot interval"""
    if interval < 1:
        interval = 1  # Minimum 1 second
    save_config(interval)
    return interval

# Application settings
APP_NAME = "Screenshot Capture"
APP_VERSION = "1.0.0"
ENABLE_LOGGING = True
LOG_FILE = BASE_DIR / "app.log"
