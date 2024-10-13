
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
