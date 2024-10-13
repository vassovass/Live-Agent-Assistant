
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
