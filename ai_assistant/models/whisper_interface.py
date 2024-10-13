
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
