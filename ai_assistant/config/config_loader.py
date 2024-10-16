import yaml
import logging
import os
from dotenv import load_dotenv

class ConfigLoader:
    def __init__(self, config_path='config/settings.yaml'):
        self.logger = logging.getLogger(self.__class__.__name__)
        load_dotenv()  # This loads the variables from .env file
        self.config = self.load_config(config_path)

    def load_config(self, path):
        if not os.path.exists(path):
            self.logger.error(f"Configuration file not found at {path}")
            raise FileNotFoundError(f"Configuration file not found at {path}")
        with open(path, 'r') as file:
            try:
                config = yaml.safe_load(file)
                self.logger.debug(f"Configuration loaded: {config}")
                # Replace environment variables
                config['openai_api_key'] = os.getenv('OPENAI_API_KEY')
                return config
            except yaml.YAMLError as exc:
                self.logger.error(f"Error parsing YAML file: {exc}")
                raise exc
