import os
from pathlib import Path

def create_or_update_file(file_path, content):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created or updated file: {file_path}")

# Define the structure and content of files to be created or updated
files_to_create = {
    'utils/sandbox.py': '''
import logging
import sys
from RestrictedPython import compile_restricted, safe_globals

class Sandbox:
    def __init__(self, config, error_handler):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = config
        self.error_handler = error_handler
        self.enabled = self.config.get('sandboxing', {}).get('enabled', True)

    def run(self, code):
        if not self.enabled:
            self.logger.warning("Sandboxing is disabled. Running code without sandboxing.")
            exec(code)
            return
        try:
            self.logger.debug("Running code in sandbox.")
            # Compile the code using RestrictedPython
            compiled_code = compile_restricted(code, '<string>', 'exec')
            exec(compiled_code, safe_globals, {})
        except Exception as e:
            self.logger.exception("Unexpected error in sandbox: %s", e)
            self.error_handler.handle(e)
''',
    'utils/screen_capture.py': '''
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
''',
    'utils/user_interface.py': '''
import logging
import tkinter as tk
from tkinter import scrolledtext

class UserInterface:
    def __init__(self, config, live_agent):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = config
        self.live_agent = live_agent
        self.root = tk.Tk()
        self.root.title("AI Assistant Live Agent")
        self.setup_ui()

    def setup_ui(self):
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=20)
        self.chat_display.pack(padx=10, pady=10)

        self.input_field = tk.Entry(self.root, width=50)
        self.input_field.pack(side=tk.LEFT, padx=10)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=5)

    def send_message(self):
        user_input = self.input_field.get()
        self.chat_display.insert(tk.END, f"You: {user_input}\n")
        self.input_field.delete(0, tk.END)

        response = self.live_agent.process_input(user_input)
        self.chat_display.insert(tk.END, f"AI: {response}\n\n")
        self.chat_display.see(tk.END)

    def run(self):
        self.root.mainloop()
''',
    'utils/resource_manager.py': '''
import psutil
import logging

class ResourceManager:
    def __init__(self, config):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.cpu_limit = config.get('resource_limits', {}).get('cpu_usage', 80)
        self.memory_limit = config.get('resource_limits', {}).get('memory_usage', 80)

    def check_resources(self):
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        self.logger.debug(f"CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage}%")
        if cpu_usage > self.cpu_limit or memory_usage > self.memory_limit:
            return False
        return True
''',
    'models/model_base.py': '''
import logging
from abc import ABC, abstractmethod

class ModelBase(ABC):
    def __init__(self, config, error_handler):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = config
        self.error_handler = error_handler

    @abstractmethod
    def run(self):
        pass
''',
    'models/gpt_interface.py': '''
import logging
from models.model_base import ModelBase
import openai

class GPTInterface(ModelBase):
    def __init__(self, config, error_handler):
        super().__init__(config, error_handler)
        self.api_key = self.config.get('openai_api_key')
        openai.api_key = self.api_key

    def generate_plan(self, text):
        try:
            self.logger.debug("Generating plan using GPT model...")
            response = openai.Completion.create(
                engine="gpt-4",
                prompt=f"Create a detailed plan based on the following input:\n\n{text}",
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.7,
            )
            plan = response.choices[0].text.strip()
            self.logger.debug(f"Generated plan: {plan}")
            return plan
        except Exception as e:
            self.logger.exception("Error generating plan with GPT: %s", e)
            self.error_handler.handle(e)
            return None

    def generate_response(self, prompt):
        try:
            self.logger.debug("Generating response using GPT model...")
            response = openai.Completion.create(
                engine="gpt-3.5-turbo",
                prompt=prompt,
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.7,
            )
            generated_text = response.choices[0].text.strip()
            self.logger.debug(f"Generated response: {generated_text}")
            return generated_text
        except Exception as e:
            self.logger.exception("Error generating response with GPT: %s", e)
            self.error_handler.handle(e)
            return None
''',
    'models/whisper_interface.py': '''
import logging
from models.model_base import ModelBase
import openai

class WhisperInterface(ModelBase):
    def __init__(self, config, error_handler):
        super().__init__(config, error_handler)
        self.api_key = self.config.get('openai_api_key')
        openai.api_key = self.api_key

    def transcribe(self, audio_data):
        try:
            self.logger.debug("Transcribing audio using Whisper model...")
            # Simulate sending audio data to Whisper API
            response = openai.Audio.transcribe(
                file=audio_data,
                model="whisper-1"
            )
            transcription = response['text']
            self.logger.debug(f"Transcription result: {transcription}")
            return transcription
        except Exception as e:
            self.logger.exception("Error transcribing audio with Whisper: %s", e)
            self.error_handler.handle(e)
            return ""
''',
    'tests/test_voice_processor.py': '''
import unittest
from agents.voice_processor import VoiceProcessor
from utils.error_handler import ErrorHandler
from config.config_loader import ConfigLoader

class TestVoiceProcessor(unittest.TestCase):
    def setUp(self):
        config_loader = ConfigLoader()
        self.config = config_loader.config
        self.error_handler = ErrorHandler(self.config)
        self.voice_processor = VoiceProcessor(self.config, self.error_handler)

    def test_process_voice(self):
        audio_data = self.voice_processor.process_voice()
        self.assertIsNotNone(audio_data)

if __name__ == '__main__':
    unittest.main()
''',
    'tests/test_sandbox.py': '''
import unittest
from utils.sandbox import Sandbox
from utils.error_handler import ErrorHandler
from config.config_loader import ConfigLoader

class TestSandbox(unittest.TestCase):
    def setUp(self):
        config_loader = ConfigLoader()
        self.config = config_loader.config
        self.error_handler = ErrorHandler(self.config)
        self.sandbox = Sandbox(self.config, self.error_handler)

    def test_sandbox_enabled(self):
        code = "x = 5\ny = 10\nresult = x + y"
        self.sandbox.run(code)
        # No exception should be raised

    def test_sandbox_restricted_code(self):
        code = "import os\nos.system('echo Hello World')"
        with self.assertRaises(Exception):
            self.sandbox.run(code)

if __name__ == '__main__':
    unittest.main()
''',
    '.github/workflows/ci.yml': '''
name: Continuous Integration

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run Tests
      run: |
        pytest --cov=ai_assistant tests/
    - name: Upload Coverage to Codecov
      uses: codecov/codecov-action@v2
      with:
        token: ${{ secrets.CODECOV_TOKEN }}
''',
    'tools_database/tools_usage.json': '''
{
    "tools": []
}
'''
}

def create_project_structure():
    base_path = Path('ai_assistant')
    for file_path, content in files_to_create.items():
        full_path = base_path / file_path
        create_or_update_file(full_path, content)

if __name__ == '__main__':
    create_project_structure()
    print("Third batch of AI Assistant project files have been created or updated.")