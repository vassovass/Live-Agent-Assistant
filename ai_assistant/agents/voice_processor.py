
import logging
from agents.agent_base import AgentBase
from utils.error_handler import ErrorHandler
import sounddevice as sd
import numpy as np

class VoiceProcessor(AgentBase):
    def __init__(self, config, error_handler):
        super().__init__(config, error_handler)
        self.enabled = self.config.get('agents', {}).get('voice_processor', {}).get('enabled', False)
        self.model_name = self.config.get('agents', {}).get('voice_processor', {}).get('model', 'RealtimeAPI')
        self.sample_rate = self.config.get('audio', {}).get('sample_rate', 44100)
        self.channels = self.config.get('audio', {}).get('channels', 2)

    def process_voice(self):
        if not self.enabled:
            self.logger.info("VoiceProcessor is disabled in configuration.")
            return None
        try:
            self.logger.debug("Starting voice processing...")
            audio_data = self._capture_audio()
            return audio_data
        except Exception as e:
            self.logger.exception("Error in process_voice: %s", e)
            self.error_handler.handle(e)
            return None

    def _capture_audio(self):
        self.logger.debug("Capturing audio data...")
        try:
            duration = 5  # seconds
            recording = sd.rec(int(duration * self.sample_rate), samplerate=self.sample_rate, channels=self.channels, dtype='float64')
            sd.wait()
            return recording
        except Exception as e:
            self.logger.exception("Error capturing audio: %s", e)
            raise e
