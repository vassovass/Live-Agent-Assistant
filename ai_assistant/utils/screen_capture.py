
import logging
import os
from datetime import datetime

try:
    from PIL import Image
    import mss
except ImportError:
    raise ImportError("Pillow and mss are required for screen capture. Please install them using 'pip install Pillow mss'.")

class ScreenCapture:
    def __init__(self, config):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = config
        self.enabled = self.config.get('screen_capture', {}).get('enabled', False)
        self.capture_interval = self.config.get('screen_capture', {}).get('capture_interval', 5)
        self.capture_dir = 'data/screenshots'
        os.makedirs(self.capture_dir, exist_ok=True)
        self.sct = mss.mss()

    def capture_screen(self):
        if not self.enabled:
            self.logger.info("ScreenCapture is disabled in configuration.")
            return
        try:
            self.logger.debug("Capturing screen...")
            screenshot = self.sct.grab(self.sct.monitors[1])
            img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_path = os.path.join(self.capture_dir, f'screenshot_{timestamp}.png')
            img.save(file_path)
            self.logger.debug(f"Screenshot saved to {file_path}")
        except Exception as e:
            self.logger.exception("Error capturing screen: %s", e)
            raise e
