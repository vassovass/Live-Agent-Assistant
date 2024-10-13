
#!/usr/bin/env python3
"""
Entry point of the AI Assistant application.
"""

import logging
import sys
from config.config_loader import ConfigLoader
from agents.voice_processor import VoiceProcessor
from agents.transcriber import Transcriber
from agents.planner import Planner
from agents.executor import Executor
from agents.live_agent import LiveAgent
from utils.error_handler import ErrorHandler
from utils.logger import setup_logging
from utils.user_interface import UserInterface

def main():
    try:
        # Setup logging
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Starting AI Assistant...")

        # Load configuration
        config_loader = ConfigLoader()
        config = config_loader.config

        # Initialize error handler
        error_handler = ErrorHandler(config)

        # Initialize agents
        voice_processor = VoiceProcessor(config, error_handler)
        transcriber = Transcriber(config, error_handler)
        planner = Planner(config, error_handler)
        executor = Executor(config, error_handler)
        live_agent = LiveAgent(config, error_handler)

        # Initialize and run user interface
        ui = UserInterface(config, live_agent)
        ui.run()

    except Exception as e:
        logger.exception("An unhandled exception occurred: %s", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
