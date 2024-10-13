
import logging
from agents.agent_base import AgentBase
from utils.error_handler import ErrorHandler
from models.whisper_interface import WhisperInterface

class Transcriber(AgentBase):
    def __init__(self, config, error_handler):
        super().__init__(config, error_handler)
        self.enabled = self.config.get('agents', {}).get('transcriber', {}).get('enabled', False)
        self.model = WhisperInterface(config, error_handler)

    def transcribe_audio(self, audio_data):
        if not self.enabled:
            self.logger.info("Transcriber is disabled in configuration.")
            return ""
        try:
            self.logger.debug("Starting transcription...")
            text = self.model.transcribe(audio_data)
            self.logger.debug(f"Transcribed text: {text}")
            return text
        except Exception as e:
            self.logger.exception("Error in transcribe_audio: %s", e)
            self.error_handler.handle(e)
            return ""
