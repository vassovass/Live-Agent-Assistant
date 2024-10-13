
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
