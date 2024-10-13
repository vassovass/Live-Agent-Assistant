
import logging
from agents.agent_base import AgentBase
from utils.error_handler import ErrorHandler
from models.gpt_interface import GPTInterface

class Planner(AgentBase):
    def __init__(self, config, error_handler):
        super().__init__(config, error_handler)
        self.enabled = self.config.get('agents', {}).get('planner', {}).get('enabled', False)
        self.model = GPTInterface(config, error_handler)

    def create_plan(self, text):
        if not self.enabled:
            self.logger.info("Planner is disabled in configuration.")
            return None
        try:
            self.logger.debug("Creating plan based on transcribed text...")
            plan = self.model.generate_plan(text)
            self.logger.debug(f"Generated plan: {plan}")
            return plan
        except Exception as e:
            self.logger.exception("Error in create_plan: %s", e)
            self.error_handler.handle(e)
            return None
