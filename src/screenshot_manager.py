"""Screenshot capture module"""
import os
import threading
import time
from datetime import datetime
from pathlib import Path

try:
    from PIL import ImageGrab
except ImportError:
    ImageGrab = None

from config import SCREENSHOT_DIR, SCREENSHOT_FORMAT, SCREENSHOT_NAMING, get_current_interval
from logger import logger


class ScreenshotManager:
    """Manages screenshot capture operations"""
    
    def __init__(self):
        self.interval = get_current_interval()
        self.is_running = False
        self.capture_thread = None
        self.screenshot_count = 0
        self.interval_lock = threading.Lock()
        
    def start(self):
        """Start capturing screenshots"""
        if self.is_running:
            logger.warning("Screenshot capture is already running")
            return False
        
        self.is_running = True
        self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.capture_thread.start()
        logger.info(f"Screenshot capture started (interval: {self.interval}s)")
        return True
    
    def stop(self):
        """Stop capturing screenshots"""
        if not self.is_running:
            logger.warning("Screenshot capture is not running")
            return False
        
        self.is_running = False
        if self.capture_thread:
            self.capture_thread.join(timeout=2)
        logger.info(f"Screenshot capture stopped. Total screenshots: {self.screenshot_count}")
        return True
    
    def set_interval(self, new_interval):
        """Change the capture interval and reset the timer"""
        with self.interval_lock:
            self.interval = new_interval
            # Reset the capture timer by restarting if currently running
            if self.is_running and self.capture_thread and self.capture_thread.is_alive():
                # Stop current thread
                self.is_running = False
                self.capture_thread.join(timeout=2)
                # Restart with new interval
                self.is_running = True
                self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
                self.capture_thread.start()
                logger.info(f"Screenshot interval changed to {new_interval} seconds (capture restarted)")
            else:
                logger.info(f"Screenshot interval changed to {new_interval} seconds")
        return True
    
    def get_interval(self):
        """Get current interval"""
        with self.interval_lock:
            return self.interval
        
    def _capture_loop(self):
        """Main capture loop - runs in separate thread"""
        while self.is_running:
            try:
                self._capture_screenshot()
                # Get current interval safely
                with self.interval_lock:
                    current_interval = self.interval
                time.sleep(current_interval)
            except Exception as e:
                logger.exception(f"Error capturing screenshot: {e}")
                # Continue capturing even if one fails
                time.sleep(1)
    
    def _capture_screenshot(self):
        """Capture a single screenshot"""
        if ImageGrab is None:
            logger.error("PIL/Pillow not installed. Cannot capture screenshot.")
            return
        
        try:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = SCREENSHOT_NAMING.replace("{timestamp}", timestamp)
            filepath = SCREENSHOT_DIR / filename
            
            # Capture screenshot
            screenshot = ImageGrab.grab()
            
            # Save screenshot
            screenshot.save(filepath, SCREENSHOT_FORMAT.upper())
            self.screenshot_count += 1
            logger.info(f"Screenshot saved: {filename}")
            
        except Exception as e:
            logger.exception(f"Failed to capture/save screenshot: {e}")
    
    def get_status(self):
        """Get current status"""
        with self.interval_lock:
            current_interval = self.interval
        return {
            "running": self.is_running,
            "interval": current_interval,
            "total_screenshots": self.screenshot_count,
            "screenshot_dir": str(SCREENSHOT_DIR)
        }
