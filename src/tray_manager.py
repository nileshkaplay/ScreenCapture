"""System tray interface for screenshot capture utility"""
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageDraw
import pystray

from config import APP_NAME, APP_VERSION, SCREENSHOT_DIR, set_interval
from logger import logger


class TrayManager:
    """Manages system tray icon and menu"""
    
    def __init__(self, screenshot_manager):
        self.screenshot_manager = screenshot_manager
        self.icon = None
        self.app_running = True
        
    def _create_image(self, width=64, height=64):
        """Create a simple image for the tray icon"""
        # Create a new image with a slightly transparent background
        image = Image.new("RGBA", (width, height), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw a simple camera icon representation
        draw.rectangle([16, 16, 48, 48], outline="white", width=2)
        draw.polygon([(32, 20), (36, 28), (28, 28)], fill="white")
        
        return image
    
    def _on_quit(self, icon, item):
        """Handle quit action"""
        self.app_running = False
        self.screenshot_manager.stop()
        icon.stop()
    
    def _on_start(self, icon, item):
        """Handle start action"""
        logger.info("Tray action: Start capture")
        self.screenshot_manager.start()
        self._update_menu(icon)
    
    def _on_stop(self, icon, item):
        """Handle stop action"""
        logger.info("Tray action: Stop capture")
        self.screenshot_manager.stop()
        self._update_menu(icon)
    
    def _on_show_folder(self, icon, item):
        """Open screenshots folder in explorer"""
        logger.info("Tray action: Open screenshots folder")
        import os
        import subprocess
        try:
            subprocess.Popen(f'explorer "{SCREENSHOT_DIR}"')
        except Exception as e:
            logger.exception(f"Could not open folder: {e}")
    
    def _on_set_interval(self, icon, item, interval):
        """Handle interval change"""
        logger.info(f"Tray action: Set interval to {interval} seconds")
        set_interval(interval)
        self.screenshot_manager.set_interval(interval)
        self._update_menu(icon)
    
    def _on_custom_interval(self, icon, item):
        """Handle custom interval input - run in separate thread"""
        logger.info("Tray action: Custom interval dialog requested")
        
        # Run dialog in a separate thread to avoid conflicts with pystray thread
        def show_dialog():
            try:
                # Create a root window (required for Tkinter dialogs)
                root = tk.Tk()
                root.withdraw()  # Hide the root window
                
                # Create a dialog window as child of root
                dialog = tk.Toplevel(root)
                dialog.title("Set Screenshot Interval")
                dialog.geometry("350x160")  # Slightly larger for better appearance
                dialog.resizable(False, False)
                dialog.attributes("-topmost", True)  # Always on top
                dialog.configure(bg='#f0f0f0')  # Light gray background
                
                # Center the dialog on screen
                dialog.update_idletasks()
                screen_width = dialog.winfo_screenwidth()
                screen_height = dialog.winfo_screenheight()
                window_width = 350
                window_height = 160
                x = (screen_width - window_width) // 2
                y = (screen_height - window_height) // 2
                dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
                
                # Get current interval before widgets are created
                current_interval = self.screenshot_manager.get_interval()
                
                # Main frame with padding
                main_frame = tk.Frame(dialog, bg='#f0f0f0', padx=20, pady=10)
                main_frame.pack(fill=tk.BOTH, expand=True)
                
                # Title label
                title_label = tk.Label(main_frame, text="Set Screenshot Interval", 
                                     font=('Segoe UI', 12, 'bold'), bg='#f0f0f0', fg='#333333')
                title_label.pack(pady=(0, 10))
                
                # Instruction label
                instr_label = tk.Label(main_frame, text="Enter interval in seconds (minimum 1):", 
                                     font=('Segoe UI', 9), bg='#f0f0f0', fg='#666666')
                instr_label.pack(pady=(0, 8))
                
                # Entry field with better styling
                entry_var = tk.StringVar(value=str(current_interval))
                entry = tk.Entry(main_frame, textvariable=entry_var, width=25, justify='center', 
                               font=('Segoe UI', 11), relief=tk.FLAT, bd=2, 
                               highlightbackground='#cccccc', highlightcolor='#0078d4', 
                               highlightthickness=1)
                entry.pack(pady=(0, 15))
                entry.select_range(0, tk.END)  # Select all text
                
                # Result variable
                result = {'value': None}
                
                def on_ok():
                    try:
                        value = int(entry_var.get())
                        if value >= 1:
                            result['value'] = value
                            dialog.destroy()
                        else:
                            messagebox.showerror("Invalid Input", "Interval must be at least 1 second.", parent=dialog)
                    except ValueError:
                        messagebox.showerror("Invalid Input", "Please enter a valid number.", parent=dialog)
                
                def on_cancel():
                    dialog.destroy()
                
                # Button frame
                button_frame = tk.Frame(main_frame, bg='#f0f0f0')
                button_frame.pack(pady=(5, 0))
                
                # Style buttons
                button_style = {'font': ('Segoe UI', 9), 'relief': tk.FLAT, 'bd': 1, 'cursor': 'hand2'}
                
                ok_button = tk.Button(button_frame, text="OK", command=on_ok, width=10, 
                                    bg='#0078d4', fg='white', activebackground='#106ebe', 
                                    activeforeground='white', **button_style)
                ok_button.pack(side=tk.LEFT, padx=(0, 10))
                
                cancel_button = tk.Button(button_frame, text="Cancel", command=on_cancel, width=10, 
                                        bg='#f3f2f1', fg='#323130', activebackground='#edebe9', 
                                        activeforeground='#323130', **button_style)
                cancel_button.pack(side=tk.LEFT)
                
                # Bind Enter key to OK and Escape to Cancel
                dialog.bind('<Return>', lambda e: on_ok())
                dialog.bind('<Escape>', lambda e: on_cancel())
                
                # Set focus and raise window
                entry.focus_set()
                dialog.lift()
                dialog.attributes("-topmost", True)
                
                # Add a subtle border effect
                dialog.after(100, lambda: dialog.focus_force())
                
                # Wait for dialog to close
                root.wait_window(dialog)
                
                # Process result
                if result['value'] is not None:
                    logger.info(f"Tray action: Set interval to {result['value']} seconds (custom)")
                    set_interval(result['value'])
                    self.screenshot_manager.set_interval(result['value'])
                    self._update_menu(icon)
                else:
                    logger.info("Tray action: Custom interval cancelled")
                
            except Exception as e:
                logger.exception(f"Error in custom interval dialog: {e}")
            finally:
                try:
                    root.destroy()
                except:
                    pass
        
        # Start dialog in a separate daemon thread
        dialog_thread = threading.Thread(target=show_dialog, daemon=True)
        dialog_thread.start()
    
    def _update_menu(self, icon):
        """Update menu based on current state"""
        status = self.screenshot_manager.get_status()
        is_running = status["running"]
        
        menu_items = []
        
        # Add status
        status_text = "● Running" if is_running else "○ Stopped"
        menu_items.append(pystray.MenuItem(status_text, lambda icon, item: None, enabled=False))
        menu_items.append(pystray.MenuItem("-", None))
        
        # Add start/stop button
        if is_running:
            menu_items.append(pystray.MenuItem("Stop Capture", self._on_stop))
        else:
            menu_items.append(pystray.MenuItem("Start Capture", self._on_start))
        
        menu_items.append(pystray.MenuItem("-", None))
        
        # Add utilities
        menu_items.append(pystray.MenuItem(
            f"Screenshots ({status['total_screenshots']})",
            lambda icon, item: None,
            enabled=False
        ))
        menu_items.append(pystray.MenuItem("Open Screenshots Folder", self._on_show_folder))
        menu_items.append(pystray.MenuItem("-", None))
        
        # Add interval submenu
        current_interval = status["interval"]
        interval_menu = pystray.Menu(
            pystray.MenuItem("5 seconds", lambda icon, item: self._on_set_interval(icon, item, 5)),
            pystray.MenuItem("10 seconds", lambda icon, item: self._on_set_interval(icon, item, 10)),
            pystray.MenuItem("30 seconds", lambda icon, item: self._on_set_interval(icon, item, 30)),
            pystray.MenuItem("60 seconds", lambda icon, item: self._on_set_interval(icon, item, 60)),
            pystray.MenuItem("-", None),
            pystray.MenuItem("Custom...", self._on_custom_interval)
        )
        menu_items.append(pystray.MenuItem(f"Interval: {current_interval}s", interval_menu))
        menu_items.append(pystray.MenuItem("-", None))
        
        # Add quit
        menu_items.append(pystray.MenuItem("Quit", self._on_quit))
        
        icon.menu = pystray.Menu(*menu_items)
    
    def start(self):
        """Start the system tray icon"""
        try:
            image = self._create_image()
            self.icon = pystray.Icon(
                APP_NAME,
                image,
                APP_NAME,
                menu=pystray.Menu()
            )
            
            # Initial menu update
            self._update_menu(self.icon)
            
            # Run icon in a separate thread so it doesn't block
            tray_thread = threading.Thread(target=self.icon.run, daemon=True)
            tray_thread.start()
            
            logger.info("System tray icon started")
            return True
        except Exception as e:
            logger.exception(f"Error starting system tray: {e}")
            return False
    
    def stop(self):
        """Stop the system tray icon"""
        if self.icon:
            try:
                self.icon.stop()
            except Exception as e:
                logger.exception(f"Error stopping tray icon: {e}")
