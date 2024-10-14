

import logging
from abc import ABC, abstractmethod

class AgentBase(ABC):
    def __init__(self, config, error_handler):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = config
        self.error_handler = error_handler

    @abstractmethod
    def run(self):
        pass
