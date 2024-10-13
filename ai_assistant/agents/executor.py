
import logging
from agents.agent_base import AgentBase
from utils.error_handler import ErrorHandler
from utils.sandbox import Sandbox

class Executor(AgentBase):
    def __init__(self, config, error_handler):
        super().__init__(config, error_handler)
        self.enabled = self.config.get('agents', {}).get('executor', {}).get('enabled', False)
        self.sandbox = Sandbox(config, error_handler)

    def execute_plan(self, plan):
        if not self.enabled:
            self.logger.info("Executor is disabled in configuration.")
            return
        try:
            self.logger.debug("Executing plan...")
            # Execute the plan within a sandbox
            self.sandbox.run(plan)
        except Exception as e:
            self.logger.exception("Error in execute_plan: %s", e)
            self.error_handler.handle(e)
