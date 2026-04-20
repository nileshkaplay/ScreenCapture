"""Main application entry point"""
import sys
import time
import os

# Add src directory to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from screenshot_manager import ScreenshotManager
from tray_manager import TrayManager
from config import APP_NAME, APP_VERSION
from logger import logger


def main():
    """Main application function"""
    logger.info(f"{APP_NAME} v{APP_VERSION} started")
    print(f"{APP_NAME} v{APP_VERSION} started")
    
    # Create screenshot manager
    screenshot_manager = ScreenshotManager()
    
    try:
        # Create and start tray manager
        tray_manager = TrayManager(screenshot_manager)
        tray_manager.start()
        
        # Keep the application running
        while tray_manager.app_running:
            time.sleep(1)
        
        print("Application closing...")
        
    except KeyboardInterrupt:
        logger.info("Interrupt received, shutting down...")
        print("\nInterrupt received, shutting down...")
        screenshot_manager.stop()
    except Exception as e:
        logger.exception("Error in main application")
        print(f"Error in main application: {e}")
        screenshot_manager.stop()
    finally:
        logger.info("Application stopped")
        print("Application stopped")


if __name__ == "__main__":
    main()
